"""Two finite explicit placement tables. No search, optimization or native calls."""
import json,csv,math,sys,itertools
from shapely.geometry import box
from shapely.ops import unary_union
from shapely.affinity import rotate,translate
from placement_common import P,G,groups,classes,region,groupbounds,body,geometry,physical
from reserve import reserve
label=sys.argv[1]
assert label in ('A','B')
reserve('refinement'+label,1,'Explicit coordinate table + geometry and pin-adjacency check')
if not (P/('PLACEMENT_'+label+'.json')).exists():reserve('formalCandidates',1,'Formal pure-placement '+label)
positions={}
def put_group(name,left,bottom,turn=0):
    refs=groups[name]
    original=unary_union([geometry(r)for r in refs]);bounds=rotate(original,turn,origin=(0,0)).bounds
    dx,dy=left-bounds[0],bottom-bounds[1]
    a=math.radians(turn)
    for r in refs:
        g=G[r];x,y=g['xMm'],g['yMm']
        positions[r]=(x*math.cos(a)-y*math.sin(a)+dx,x*math.sin(a)+y*math.cos(a)+dy,(g['rotation']+turn)%360)
def put(ref,x,y,angle=0):positions[ref]=(x,y,angle)

# A follows native contact-side signal flow; B aligns two principal columns
# and three bands. Both remove old copper as a constraint, and reposition
# all C-class parts into new explicit rows, not unchanged20 small islands.
if label=='A':
    table={'TIA':(7,46,0),'ROW':(7,24,0),'REFERENCE':(31,55,0),'ADC':(29,18,90),
      'MCU':(55,4,0),'POWER5':(7,4,0),'POWER3':(23,4,0),'LDO':(38,4,0),
      'MUX':(31,44,0),'U13':(68,4,0),'U14':(77,4,0),'U15':(77,16,0),
      'U11':(55,54,0),'U12':(62,50,0),'J2':(.5,34,0),'J1':(2,4,0),
      'J3':(85,24,0),'J4':(85,56,0)}
else:
    table={'TIA':(7,54,0),'ROW':(7,28,0),'REFERENCE':(30,58,0),'ADC':(29,20,90),
      'MCU':(52,0,0),'POWER5':(7,0,0),'POWER3':(23,0,0),'LDO':(39,0,0),
      'MUX':(30,47,0),'U13':(65,0,0),'U14':(65,11,0),'U15':(75,6,0),
      'U11':(55,58,0),'U12':(63,54,0),'J2':(.5,39,0),'J1':(2,0,0),
      'J3':(79,24,0),'J4':(79,54,0)}
for n,args in table.items():put_group(n,*args)
# Two regular power-control passive rows below their local power IC.
for u,x in [('U9',8),('U10',24)]:
    rs=[r for r in G if r.startswith(u+'_') and r not in positions]
    ordinary=[r for r in rs if not r.endswith('_BLEED')]
    for i,r in enumerate(ordinary):
        y=(-1-(i//4)*3.0) if label=='A' else (8+(i//4)*3.0)
        put(r,x+(i%4)*3.0,y,0)
    # BLEED uses a larger native resistor body than the0603 controls.
    put(u+'_BLEED',x+6,(12 if label=='A' else 16),0)

# Repeated supervisor divider rows above their two capacitor/IC clusters.
for u,x in [('U11',54),('U12',64)]:
    rs=[r for r in G if r.startswith(u+'_') and r not in positions]
    for i,r in enumerate(rs):put(r,x+(i%3)*3,72+(i//3)*3,0)

# Debug/USART passive pairs follow corresponding real connector pad y.
for j in ('J3','J4'):
    gj=G[j];pj=positions[j]
    dx,dy=pj[0]-gj['xMm'],pj[1]-gj['yMm']
    for r in G:
        if r in positions or '_'+j+'_' not in r:continue
        n=r.rsplit('_',1)[1]
        pad=next(p for p in gj['pads'] if p['number']==n)
        x=pj[0]-(3.5 if r.startswith('R_') else 7.5)
        put(r,x,pad['yMm']+dy,0 if r.startswith('R_') else 90)

mx,my,_=table['MUX']
for i in range(4):put('R_SEL_PD'+str(i),mx+9+(i%2)*3,my+2+(i//2)*3,0)
other={'A':{'C_MCU_BULK':(64,18,0),'C_PWR':(3,-1,0),'C_RST':(83,16,0),
 'R_ADC_RESET_PD':(64,27,0),'R_CS_PU':(64,24,0),'R_ENABLE_PD':(69,18,0),'R_HW_PD':(72,18,0),'R_RST':(83,19,0)},
 'B':{'C_MCU_BULK':(59,15,0),'C_PWR':(3,10,0),'C_RST':(79,15,0),
 'R_ADC_RESET_PD':(64,27,0),'R_CS_PU':(62,16,0),'R_ENABLE_PD':(69,23,0),'R_HW_PD':(72,23,0),'R_RST':(79,18,0)}}
for r,pos in other[label].items():put(r,*pos)
assert set(positions)==set(G),str(set(G)-set(positions))

bodies={r:body(r,positions[r])for r in G}
phys={r:physical(r,positions[r])for r in G}
overlaps=[];pad_envelope_overlaps=[]
refs=sorted(G)
for i,r in enumerate(refs):
    for s in refs[i+1:]:
        area=bodies[r].intersection(bodies[s]).area
        if area>1e-8:overlaps.append({'a':r,'b':s,'areaMm2':area})
        if groups.get(r)==groups.get(s):continue
        if phys[r].intersection(phys[s]).area>1e-8:pad_envelope_overlaps.append({'a':r,'b':s})

def newpad(r,p):
    g=G[r];x,y,a=positions[r];t=math.radians(a-g['rotation'])
    u,v=p['xMm']-g['xMm'],p['yMm']-g['yMm']
    return(x+u*math.cos(t)-v*math.sin(t),y+u*math.sin(t)+v*math.cos(t))
pairs=[]
for n,rs in groups.items():
    if classes[rs[0]]!='A' or n=='J2':continue
    ics=[r for r in rs if r.startswith('U')and'_'not in r]
    passives=[r for r in rs if r.startswith(('R','C'))]
    for r in passives:
        for p in G[r]['pads']:
            if not p['net'] or p['net']=='GND':continue
            possible=[(ic,q)for ic in ics for q in G[ic]['pads']if q['net']==p['net']]
            if not possible:continue
            ic,q=min(possible,key=lambda iq:math.hypot(iq[1]['xMm']-p['xMm'],iq[1]['yMm']-p['yMm']))
            d0=math.hypot(q['xMm']-p['xMm'],q['yMm']-p['yMm'])
            pp,qq=newpad(r,p),newpad(ic,q)
            d1=math.hypot(qq[0]-pp[0],qq[1]-pp[1])
            pairs.append({'group':n,'icRef':ic,'icPad':q['number'],'passiveRef':r,'passivePad':p['number'],'net':p['net'],'beforeMm':d0,'afterMm':d1,'deltaMm':d1-d0})
assert pairs and max(p['deltaMm']for p in pairs)<1e-8

# FFC local +y maps towards left in these90degree-native candidates.
j=positions['J2'];mouthx=j[0]-5.5
cable=box(mouthx-10,j[1]-8.7,mouthx,j[1]+8.7)
opening=box(j[0]-7.5,j[1]-8.7,j[0]+.3,j[1]+8.7)
keepout_collisions=[]
for r in G:
    if r=='J2':continue
    if bodies[r].intersection(cable).area>1e-8 or bodies[r].intersection(opening).area>1e-8:keepout_collisions.append(r)

natural=unary_union(list(bodies.values()));bb=natural.bounds
physicalbb=unary_union(list(phys.values())).bounds
width,height=bb[2]-bb[0],bb[3]-bb[1]
cells=[]
for iy in range(4):
    for ix in range(4):
        cell=box(bb[0]+ix*width/4,bb[1]+iy*height/4,bb[0]+(ix+1)*width/4,bb[1]+(iy+1)*height/4)
        cells.append({'ix':ix,'iy':iy,'cellAreaMm2':cell.area,'bodyUnionAreaMm2':natural.intersection(cell).area,'bodyAreaFraction':natural.intersection(cell).area/cell.area})
fractions=[v['bodyAreaFraction']for v in cells];mean=sum(fractions)/16
cv=(sum((v-mean)**2 for v in fractions)/16)**.5/mean
regionareas={n:sum(bodies[r].area for r in G if region(r)==n)for n in sorted({region(r)for r in G})}
metrics={'candidate':label,'status':'OFFLINE_PLACEMENT_NOT_NATIVE_NOT_ROUTED','components':176,
 'naturalBodyBoundingBoxMm':bb,'physicalPadAndBodyBoundingBoxMm':physicalbb,
 'naturalWidthMm':width,'naturalHeightMm':height,'bodyProjectedUnionAreaMm2':natural.area,'bodyAreaOverNaturalBBox':natural.area/(width*height),
 'regionBodyAreaMm2':regionareas,'regionBodyAreaShare':{n:v/sum(regionareas.values())for n,v in regionareas.items()},
 'regionAreaDefinition':'Body projected area by electrical functional membership / sum of all body areas. Not drawn rectangle area; no assertion that bounding-box regions are disjoint.',
 'bodyOverlapPairs':overlaps,'conservativePadEnvelopeOverlapPairs':pad_envelope_overlaps,
 'criticalPairs':len(pairs),'maxCriticalDistanceDeltaMm':max(p['deltaMm']for p in pairs),'FFC2DKeepoutBodyCollisions':keepout_collisions,
 'FFCBody':'Official-dimension conservative planning envelope; nominal exact body/actuator registration not manufacturer-certified.',
 'FFCOpeningHeightReferenceMm':3.95,'verticalChassisClearance':'NOT_APPLICABLE_TO_BARE_PLACEMENT; exact enclosing chassis not specified',
 'mechanicalEnvelopeMm':unary_union([natural,cable,opening]).bounds,
 'recommendedBoardEnvelopeMm':[physicalbb[0]-3,physicalbb[1]-3,physicalbb[2]+3,physicalbb[3]+3],
 'boardEnvelopeStatus':'PROPOSAL_ONLY; 3mm policy margin. Cable access area outside proposed board, not board material; connector side access/chassis/fab remain pending.',
 'grid4x4':cells,'gridCoefficientOfVariation':cv,
 'peripheryBlankDefinition':'Largest empty raster rectangle inside natural bbox, 1mm geometric sample; not copper/keepout or fabrication clearance.',
 'CADOperations':0}
# Simple finite1mm sampling metric; no placement search or optimization.
nx,ny=math.ceil(width),math.ceil(height);hist=[0]*nx;largest=0
from shapely.geometry import Point
for yy in range(ny):
    for xx in range(nx):
        point=Point(bb[0]+xx+.5,bb[1]+yy+.5)
        hist[xx]=hist[xx]+1 if not natural.covers(point) else 0
    stack=[]
    for xx,h in enumerate(hist+[0]):
        begin=xx
        while stack and stack[-1][1]>h:
            index,oldh=stack.pop();largest=max(largest,(xx-index)*oldh);begin=index
        stack.append((begin,h))
metrics['largestEmptyRasterRectangleAreaMm2']=largest

rows=[]
for r in sorted(G):
    x,y,a=positions[r]
    rows.append({'Designator':r,'X_mm':x,'Y_mm':y,'Rotation':a,'Layer':G[r]['layer'],'Function block':region(r),'Constraint class':classes[r],'Body source':G[r]['bodySource'],'Notes':G[r]['bodyStatus']+'; no native placement/routing performed'})
with(P/('PLACEMENT_'+label+'.csv')).open('w',encoding='utf-8-sig',newline='')as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
with(P/('KEY_PIN_DISTANCES_'+label+'.csv')).open('w',encoding='utf-8-sig',newline='')as f:
    w=csv.DictWriter(f,fieldnames=list(pairs[0]));w.writeheader();w.writerows(pairs)
out={'positions':positions,'metrics':metrics,'regionMembership':{r:region(r)for r in G},'constraintClass':classes}
(P/('PLACEMENT_'+label+'.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
b=json.loads((P/'EXECUTION_BUDGET.json').read_text(encoding='utf-8-sig'));passno=b['actual']['refinement'+label]
(P/('GEOMETRY_'+label+'_PASS_'+str(passno)+'.json')).write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'candidate':label,'bbox':[width,height],'bodyOverlapPairs':overlaps,'padProxyOverlaps':pad_envelope_overlaps,'criticalPairs':len(pairs),'distanceDeltaMm':metrics['maxCriticalDistanceDeltaMm'],'FFCkeepoutCollisions':keepout_collisions,'pass':passno}))
