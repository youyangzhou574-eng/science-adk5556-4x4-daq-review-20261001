from placement_geometry import *
import csv,itertools,numpy as np
from shapely.prepared import prep
reserve('placementRefinement','Only remaining B2 third round: finite upper-MUX rigid translations and associated four pulls')
baseline=json.loads((P/'PLACEMENT_B2.json').read_text());old=baseline['positions'];positions={r:tuple(v)for r,v in old.items()}
movable=groups['MUX']+['R_SEL_PD0','R_SEL_PD1','R_SEL_PD2','R_SEL_PD3'];fixed=set(G)-set(movable)
fixedphys=unary_union([physical(r,old[r])for r in fixed]);fixedbody=unary_union([body(r,old[r])for r in fixed]);bb=baseline['metrics']['naturalBBoxMm'];leftband=box(bb[0],56,38.5,bb[3])
j=old['J2'];keepout=unary_union([box(j[0]-15.5,j[1]-8.7,j[0]-5.5,j[1]+8.7),box(j[0]-7.5,j[1]-8.7,j[0]+.3,j[1]+8.7)])
anchor=old['U4'];trials=[];best=None
for dx in(-44,-40,-36,-32,-28,-24,-20):
    for dy in(-3,-2,-1,0):
        p={r:(old[r][0]+dx,old[r][1]+dy,old[r][2])for r in movable}
        shapes={r:physical(r,p[r])for r in movable}
        collision=any(q.intersection(fixedphys).area>1e-8 or q.intersection(keepout).area>1e-8 for q in shapes.values())or any(shapes[r].intersection(shapes[s]).area>1e-8 for r,s in itertools.combinations(movable,2))
        bounds=unary_union([fixedphys]+list(shapes.values())).bounds
        if collision or bounds[0]<bb[0]-.25:trials.append({'dx':dx,'dy':dy,'status':'REJECT_COLLISION_OR_LEFT_EXTENT'});continue
        nat=unary_union([fixedbody]+[body(r,p[r])for r in movable]);nb=nat.bounds
        # Bounded evaluation of the specified left top band, not a new optimizer.
        mask=np.array([[nat.intersects(box(.5+x,56+y,1.5+x,57+y))for x in range(38)]for y in range(7)],dtype=int)
        hist=[0]*38;largest=0
        for row in mask:
            for x in range(38):hist[x]=hist[x]+1 if not row[x]else 0
            stack=[]
            for x,h in enumerate(hist+[0]):
                start=x
                while stack and stack[-1][1]>h:
                    ix,hh=stack.pop();largest=max(largest,(x-ix)*hh);start=ix
                stack.append((start,h))
        # Primary: top-left continuity. Keep total footprint within old extent.
        score=largest+max(0,nb[3]-bb[3])*20+abs(dx+32)*.05
        trials.append({'dx':dx,'dy':dy,'status':'VALID','topLeftEmptyFullCellRectMm2':largest,'topLeftOccupiedCells':int(mask.sum()),'score':score})
        if best is None or score<best[0]:best=(score,p,dx,dy)
assert best is not None,'No valid bounded local movement; do not add a fourth round'
positions.update(best[1]);bodies={r:body(r,positions[r])for r in G};shapes={r:physical(r,positions[r])for r in G}
def audit(sh):
    out=[]
    for r,s in itertools.combinations(sorted(G),2):
        area=sh[r].intersection(sh[s]).area
        if area>1e-8:out.append({'a':r,'b':s,'areaMm2':area})
    return out
bodycoll=audit(bodies);physicalcoll=audit(shapes);keepcoll=[r for r in fixed if r!='J2'and shapes[r].intersection(keepout).area>1e-8]
assert not bodycoll and not physicalcoll and not keepcoll
assert all(tuple(positions[r])==tuple(old[r])for r in fixed)
rows=list(csv.DictReader((P/'KEY_PIN_DISTANCE_B2.csv').open(encoding='utf-8-sig')))
for row in rows:
    r,s=row['icRef'],row['passiveRef'];rp=next(p for p in G[r]['pads']if p['number']==str(row['icPad']));sp=next(p for p in G[s]['pads']if p['number']==str(row['passivePad']));dist=math.dist(newpad(r,rp,positions[r]),newpad(s,sp,positions[s]));row['B21Mm']=dist;row['B21MinusB2Mm']=dist-float(row['B2Mm'])
assert len(rows)==94 and max(abs(float(row['B21MinusB2Mm']))for row in rows)<1e-8
nat=unary_union(list(bodies.values()));newbb=nat.bounds;w,h=newbb[2]-newbb[0],newbb[3]-newbb[1]
grid=[]
for y in range(math.ceil(h)):
    grid.append([int(nat.intersects(box(newbb[0]+x,newbb[1]+y,min(newbb[0]+x+1,newbb[2]),min(newbb[1]+y+1,newbb[3]))))for x in range(math.ceil(w))])
hist=[0]*int(w);largest=0
for y in range(int(h)):
    for x in range(int(w)):hist[x]=hist[x]+1 if not grid[y][x]else 0
    stack=[]
    for x,hh in enumerate(hist+[0]):
        begin=x
        while stack and stack[-1][1]>hh:
            ix,oh=stack.pop();largest=max(largest,(x-ix)*oh);begin=ix
        stack.append((begin,hh))
fractions=[]
for y in range(4):
    for x in range(4):
        cell=box(newbb[0]+x*w/4,newbb[1]+y*h/4,newbb[0]+(x+1)*w/4,newbb[1]+(y+1)*h/4);fractions.append(nat.intersection(cell).area/cell.area)
avg=sum(fractions)/16;cv=(sum((v-avg)**2 for v in fractions)/16)**.5/avg
metrics={'components':176,'pads':552,'naturalBBoxMm':newbb,'naturalWidthMm':w,'naturalHeightMm':h,'bodyFraction':nat.area/(w*h),'gridCV':cv,'largestEmptyFullCellRectangleAreaMm2':largest,'topLeftBandBeforeEmptyRectMm2':266,'topLeftBandAfterEmptyRectMm2':min(t['topLeftEmptyFullCellRectMm2']for t in trials if t['status']=='VALID'),'movedRefs':sorted(movable),'movedCount':len(movable),'fixedCount':len(fixed),'selectedTranslation':[best[2],best[3]],'rotationChange':0,'bodyOverlapPairs':bodycoll,'physicalProxyOverlapPairs':physicalcoll,'distinctPairsExaminedEach':15400,'criticalPairs':94,'maxCriticalDeltaVsB2Mm':max(abs(float(r['B21MinusB2Mm']))for r in rows),'FFCPlanningKeepoutCollisions':keepcoll,'FFCExactSweepHOLD':True,'CAD':0}
out={'positions':positions,'metrics':metrics,'regions':regions,'classes':classes,'finiteTrials':trials}
(P/'PLACEMENT_B21.json').write_text(json.dumps(out,indent=2),encoding='utf8')
with(P/'PLACEMENT_B21.csv').open('w',encoding='utf-8-sig',newline='')as f:
    writer=csv.DictWriter(f,fieldnames=['Designator','X_mm','Y_mm','Rotation','Layer','Function','Constraint','ChangedFromB2']);writer.writeheader();writer.writerows([dict(Designator=r,X_mm=positions[r][0],Y_mm=positions[r][1],Rotation=positions[r][2],Layer=G[r]['layer'],Function=regions[r],Constraint=classes[r],ChangedFromB2=r in movable)for r in sorted(G)])
with(P/'KEY_PIN_DISTANCE_B21.csv').open('w',encoding='utf-8-sig',newline='')as f:writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
(P/'FROZEN_AND_MOVED_REGISTER.json').write_text(json.dumps({'fixedRefs':sorted(fixed),'movedRefs':sorted(movable),'allowedScope':'MUX rigid2 + four associated C-class pulls only; Bias and Digital remain fixed','selectedDelta':[best[2],best[3]],'noRotation':True},indent=2),encoding='utf8')
print(json.dumps(metrics))
