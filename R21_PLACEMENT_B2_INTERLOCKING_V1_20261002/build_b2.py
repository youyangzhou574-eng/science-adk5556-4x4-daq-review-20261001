import json,math,csv,sys,itertools
import numpy as np
from shapely.geometry import box
from shapely.ops import unary_union
from shapely.affinity import rotate
from shapely.prepared import prep
from placement_geometry import *
passno=reserve('placementRefinement','Bounded skeleton + finite greedy placement + complete pair audits')
positions={};placed_shapes={}
def putgroup(n,left,bottom,turn=0):
    rs=groups[n];bounds=rotate(unary_union([original[r]for r in rs]),turn,origin=(0,0)).bounds
    dx,dy=left-bounds[0],bottom-bounds[1];t=math.radians(turn)
    for r in rs:
        g=G[r];positions[r]=(g['xMm']*math.cos(t)-g['yMm']*math.sin(t)+dx,g['xMm']*math.sin(t)+g['yMm']*math.cos(t)+dy,(g['rotation']+turn)%360)
        placed_shapes[r]=physical(r,positions[r])
# Skeleton anchors only; no six-region rectangles. Local contours interlock.
table={'TIA':(7,32,0),'ROW':(7,10,0),'REFERENCE':(27,37,0),'ADC':(27,11,90),
 'MCU':(51,43,0),'POWER5':(7,0,0),'LDO':(26,0,0),'POWER3':(43,0,0),
 'MUX':(46,33,0),'U13':(54,32,0),'U14':(61,34,0),'U15':(62,28,0),
 'U11':(45,44,0),'U12':(62,4,0),'J2':(.5,23,0),'J1':(1,0,0),'J3':(69,10,0),'J4':(69,45,0)}
if passno>1:
    # Only activated on a documented first-pass issue; retain all previous output.
    fixes=json.loads((P/'SKELETON_CORRECTIONS.json').read_text(encoding='utf8'))if(P/'SKELETON_CORRECTIONS.json').exists()else{}
    table.update({n:tuple(v)for n,v in fixes.items()})
for n,v in table.items():putgroup(n,*v)
def collisions(shapes):
    rs=sorted(shapes);out=[]
    for i,r in enumerate(rs):
        for s in rs[i+1:]:
            if shapes[r].intersection(shapes[s]).area>1e-8:out.append({'a':r,'b':s,'areaMm2':shapes[r].intersection(shapes[s]).area})
    return out
sk=collisions(placed_shapes)
if sk:
    (P/f'PASS_{passno}_SKELETON_FAILURE.json').write_text(json.dumps(sk,indent=2),encoding='utf8');print(json.dumps({'pass':passno,'skeletonCollisions':sk}));sys.exit(2)
j=positions['J2'];cable=box(j[0]-15.5,j[1]-8.7,j[0]-5.5,j[1]+8.7);opening=box(j[0]-7.5,j[1]-8.7,j[0]+.3,j[1]+8.7);keepout=unary_union([cable,opening])
free=[r for r in G if r not in positions]
free.sort(key=lambda r:(-original[r].area,r))
common_power={'GND','V3V3','V5','VCM','V5_IN','V3_LDO'}
def hostof(r):
    if r.startswith(('U9_','U10_','U11_','U12_')):return r.split('_')[0]
    if '_J3_'in r:return'J3'
    if '_J4_'in r:return'J4'
    if r.startswith('R_SEL'):return'U4'
    if r=='C_PWR':return'J1'
    if r in('C_MCU_BULK','R_RST','C_RST','R_CS_PU'):return'U7'
    if r=='R_ADC_RESET_PD':return'U5'
    nets={p['net']for p in G[r]['pads']} - common_power - {''}
    hosts=[s for s in positions if s.startswith('U')and'_'not in s and any(p['net']in nets for p in G[s]['pads'])]
    return hosts[0]if hosts else'U7'
trace=[];grid_step=1.0
for r in free:
    union=unary_union(list(placed_shapes.values()));ob=union.bounds;obarea=(ob[2]-ob[0])*(ob[3]-ob[1]);buffered=union.buffer(.20);occupied=prep(buffered)
    # Finite 1mm occupancy grid covering only current natural drawing canvas.
    xs=np.arange(max(.5,math.ceil(ob[0]*2)/2),ob[2]+.01,grid_step);ys=np.arange(math.ceil(ob[1]*2)/2,ob[3]+.01,grid_step)
    host=hostof(r);hx,hy,_=positions[host]
    empty=[]
    for y in ys:
        for x in xs:
            if not occupied.intersects(box(x-.5,y-.5,x+.5,y+.5))and not keepout.intersects(box(x-.5,y-.5,x+.5,y+.5)):
                dist=math.hypot(x-hx,y-hy);void=min(math.hypot(x-positions[s][0],y-positions[s][1])for s in table if s in positions)
                empty.append((x,y,dist,void))
    # Nearest host candidates + finite large-hole candidates, not global optimization.
    candidates=sorted(empty,key=lambda v:v[2])[:64]+sorted(empty,key=lambda v:v[2]-.8*v[3])[:64]+sorted(empty,key=lambda v:-v[3])[:24]
    unique=list(dict.fromkeys((x,y)for x,y,_,_ in candidates))
    best=None;trials=0
    for x,y in unique:
        for a in(0,90,180,270):
            pos=(float(x),float(y),a);q=physical(r,pos);trials+=1
            if q.intersects(buffered)or q.intersects(keepout):continue
            nb=(min(ob[0],q.bounds[0]),min(ob[1],q.bounds[1]),max(ob[2],q.bounds[2]),max(ob[3],q.bounds[3]));extra=(nb[2]-nb[0])*(nb[3]-nb[1])-obarea
            aspect=abs(math.log((nb[2]-nb[0])/(nb[3]-nb[1])))
            # Favor inside concavities, sensible host adjacency, then grid texture.
            dist=math.hypot(x-hx,y-hy);radius=min(q.distance(z)for z in placed_shapes.values())
            alignment=min(abs(x-positions[s][0])+abs(y-positions[s][1])for s in positions if regions[s]==regions[r])
            score=extra*.15+aspect*8+dist*.45-radius*.65+alignment*.06
            if best is None or score<best[0]:best=(score,pos,q,extra,dist,radius)
    if best is None:
        (P/f'PASS_{passno}_GREEDY_FAILURE.json').write_text(json.dumps({'ref':r,'trialCount':trials,'positions':positions},indent=2),encoding='utf8');print(json.dumps({'pass':passno,'noFiniteCandidate':r,'trials':trials}));sys.exit(3)
    score,pos,q,extra,dist,radius=best;positions[r]=pos;placed_shapes[r]=q
    trace.append({'ref':r,'host':host,'candidateCenters':len(unique),'rotationTrials':trials,'score':score,'position':pos,'bboxAreaAddedMm2':extra,'hostCenterDistanceMm':dist,'localGapMm':radius})
assert set(positions)==set(G)and len(positions)==176
# No exemption whatsoever: audit all 15400 distinct pairs, including same blocks.
bodies={r:body(r,positions[r])for r in G};bodycoll=collisions(bodies);physcoll=collisions(placed_shapes)
pairs=[]
old=json.loads((P/'PLACEMENT_B.json').read_text(encoding='utf8'))
with(P/'KEY_PIN_DISTANCES_B.csv').open(encoding='utf-8-sig')as f:oldpairs=list(csv.DictReader(f))
def addpair(ic,ip,r,rp,why):
    q=next(p for p in G[ic]['pads']if p['number']==str(ip));p=next(p for p in G[r]['pads']if p['number']==str(rp))
    before=math.hypot(q['xMm']-p['xMm'],q['yMm']-p['yMm']);a,b=newpad(ic,q,positions[ic]),newpad(r,p,positions[r]);after=math.dist(a,b)
    pairs.append({'icRef':ic,'icPad':ip,'passiveRef':r,'passivePad':rp,'icNet':q['net'],'passiveNet':p['net'],'association':why,'beforeMm':before,'B2Mm':after,'deltaMm':after-before})
for row in oldpairs:addpair(row['icRef'],row['icPad'],row['passiveRef'],row['passivePad'],'DIRECT_SAME_NET')
for u in('U9','U10'):
    addpair(u,'5',u+'_IN_CAP','1','DIRECT_SAME_NET_POWER_INPUT_CAP');addpair(u,'6',u+'_OUT_CAP','1','DIRECT_SAME_NET_POWER_OUTPUT_CAP')
for i in range(4):
    for r in('RF'+str(i),'CF'+str(i)):
        addpair('U2',[1,7,8,14][i],r,'1','FUNCTIONAL_OUTPUT_VIA_R_TIA_ISO'+str(i))
        addpair('U2',[2,6,9,13][i],r,'2','FUNCTIONAL_INPUT_VIA_R_COL_SENSE'+str(i))
assert len(pairs)==94 and max(abs(p['deltaMm'])for p in pairs)<1e-8
rigidaudit=[]
for n,rs in groups.items():
    if len(rs)<2:continue
    maxdelta=0
    for r,s in itertools.combinations(rs,2):
        before=math.hypot(G[r]['xMm']-G[s]['xMm'],G[r]['yMm']-G[s]['yMm']);after=math.dist(positions[r][:2],positions[s][:2]);maxdelta=max(maxdelta,abs(after-before))
    rigidaudit.append({'block':n,'parts':len(rs),'allComponentCenterPairs':len(rs)*(len(rs)-1)//2,'maxRigidDistanceErrorMm':maxdelta})
assert max(x['maxRigidDistanceErrorMm']for x in rigidaudit)<1e-8
nat=unary_union(list(bodies.values()));bb=nat.bounds;w,h=bb[2]-bb[0],bb[3]-bb[1]
# Exact cell intersections, bounded to bbox; no center-only/outside ceil cells.
nx,ny=math.ceil(w),math.ceil(h);grid=np.zeros((ny,nx),dtype=np.uint8);emptyarea=[]
for y in range(ny):
    for x in range(nx):
        cell=box(bb[0]+x,bb[1]+y,min(bb[0]+x+1,bb[2]),min(bb[1]+y+1,bb[3]));grid[y,x]=nat.intersects(cell)
# Conservative unit-cell blank rectangle excludes partial edge cells.
nxfull,nyfull=int(w),int(h);hist=[0]*nxfull;largest=0;rect=None
for yy in range(nyfull):
    for xx in range(nxfull):hist[xx]=hist[xx]+1 if grid[yy,xx]==0 else 0
    stack=[]
    for xx,hh in enumerate(hist+[0]):
        begin=xx
        while stack and stack[-1][1]>hh:
            ix,oldh=stack.pop();area=(xx-ix)*oldh
            if area>largest:largest=area;rect=[bb[0]+ix,bb[1]+yy-oldh+1,bb[0]+xx,bb[1]+yy+1]
            begin=ix
        stack.append((begin,hh))
cells=[]
for y in range(4):
    for x in range(4):
        cell=box(bb[0]+x*w/4,bb[1]+y*h/4,bb[0]+(x+1)*w/4,bb[1]+(y+1)*h/4);cells.append(nat.intersection(cell).area/cell.area)
mean=sum(cells)/16;cv=(sum((a-mean)**2 for a in cells)/16)**.5/mean
keepcoll=[r for r in G if r!='J2'and placed_shapes[r].intersection(keepout).area>1e-8]
m={'pass':passno,'components':176,'pads':sum(len(g['pads'])for g in G.values()),'naturalBBoxMm':bb,'naturalWidthMm':w,'naturalHeightMm':h,'bodyUnionMm2':nat.area,'bodyFraction':nat.area/(w*h),'aspectRatio':w/h,'bodyOverlapPairs':bodycoll,'physicalProxyOverlapPairs':physcoll,'allDistinctPairsExamined':176*175//2,'criticalPairs':94,'maxCriticalDeltaMm':max(abs(x['deltaMm'])for x in pairs),'FFCPlanningKeepoutCollisions':keepcoll,'FFCExactActuatorSweepHOLD':True,'largestEmptyFullCellRectangleAreaMm2':largest,'largestEmptyRectMm':rect,'gridStepMm':1,'gridMethod':'body-intersection of clipped cells; largest full-cell empty rectangle, not native clearance','grid4x4Fractions':cells,'gridCV':cv,'CAD':0,'status':'OFFLINE_PLACEMENT_COMPLETE'if not(bodycoll or physcoll or keepcoll)else'GEOMETRY_HOLD'}
out={'positions':positions,'metrics':m,'regions':regions,'classes':classes,'skeleton':table,'greedyTrace':trace,'rigidAudit':rigidaudit}
(P/f'PLACEMENT_B2_PASS_{passno}.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');(P/'PLACEMENT_B2.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
for fname,rows in [('PLACEMENT_B2.csv',[{'Designator':r,'X_mm':positions[r][0],'Y_mm':positions[r][1],'Rotation':positions[r][2],'Layer':G[r]['layer'],'Function':regions[r],'Constraint':classes[r],'BodySource':G[r]['bodySource'],'BodyStatus':G[r]['bodyStatus']}for r in sorted(G)]),('KEY_PIN_DISTANCE_B2.csv',pairs),('RIGID_BLOCK_AUDIT.csv',rigidaudit),('GREEDY_CANDIDATE_TRACE.csv',trace)]:
    with(P/fname).open('w',encoding='utf-8-sig',newline='')as f:writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
np.save(P/f'OCCUPANCY_B2_PASS_{passno}.npy',grid)
print(json.dumps(m))
