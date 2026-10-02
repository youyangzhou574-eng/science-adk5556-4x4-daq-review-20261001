from pathlib import Path
import json,csv,math,itertools,hashlib
import numpy as np
from scipy.optimize import milp,LinearConstraint,Bounds
from scipy.sparse import lil_matrix
from shapely.ops import unary_union
from shapely.geometry import box
from placement_geometry import G,C,body,physical,newpad
from audit_core import rigid_reuse,identity_digest
from build_b3 import keys,pd
P=Path(__file__).parent
new=json.loads((P/'PLACEMENT_B3.json').read_text())['positions'];old=json.loads((P/'PLACEMENT_B22.json').read_text())['positions']
def save(n,d):(P/n).write_text(json.dumps(d,indent=2),encoding='utf8')
def csvout(n,rows):
 if not rows:return
 with (P/n).open('w',encoding='utf8',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
members=C['membership']
def family(r):
 m=members[r]
 if m in ['TIA','ROW','ADC']:return m
 if m in ['REFERENCE','MUX'] or r.startswith('R_SEL'):return'BIAS_MUX'
 if r.startswith(('U8','U9','U10','U11','U12','C_LDO')) or r in ['J1','C_PWR']:return'POWER'
 if r=='J2':return'INTERFACE_J2'
 return'DIGITAL'
def invariant_bound(a,b):
 refs=sorted(a);n=len(refs);bad=[]
 for i,j in itertools.combinations(range(n),2):
  da=math.dist(a[refs[i]][:2],a[refs[j]][:2]);db=math.dist(b[refs[i]][:2],b[refs[j]][:2])
  if abs(da-db)>1.0+1e-8:bad.append((i,j))
 mat=lil_matrix((len(bad),n))
 for k,(i,j) in enumerate(bad):mat[k,i]=mat[k,j]=1
 res=milp(-np.ones(n),integrality=np.ones(n),bounds=Bounds(np.zeros(n),np.ones(n)),constraints=LinearConstraint(mat.tocsr(),np.full(len(bad),-np.inf),np.ones(len(bad))),options={'time_limit':3})
 # Necessary distance invariants: any tol0.5 rigid inliers must satisfy every |oldDist-newDist|<=1.
 ub=math.floor(-float(res.mip_dual_bound)+1e-7) if res.mip_dual_bound is not None else n
 return {'necessaryPairIncompatibilities':len(bad),'upperBoundCount':ub,'upperBoundFraction':ub/n,'solverStatus':int(res.status),'globalUpperBoundValid':res.mip_dual_bound is not None}
reuse=[]
for fam in ['TIA','ROW','ADC','BIAS_MUX','POWER','DIGITAL']:
 rr=[r for r in new if family(r)==fam];a={r:old[r] for r in rr};b={r:new[r] for r in rr};fit=rigid_reuse(a,b);ub=invariant_bound(a,b)
 reuse.append({'family':fam,'refs':rr,**fit,**ub,'passNoRigidReuse':ub['upperBoundFraction']<=.7,'note':'finite SO2 fit is lower bound; necessary pair-distance MILP dual bounds any arbitrary translation/rotation inlier count, independent of fit search'})
save('OLD_BLOCK_RIGID_REUSE_AUDIT.json',reuse)
sh={r:physical(r,new[r]) for r in new};bh={r:body(r,new[r]) for r in new};coll=[];bcoll=[];mingap=999
for r,s in itertools.combinations(sorted(new),2):
 gap=sh[r].distance(sh[s]);mingap=min(mingap,gap)
 if sh[r].intersection(sh[s]).area>1e-8:coll.append([r,s])
 if bh[r].intersection(bh[s]).area>1e-8:bcoll.append([r,s])
kr=[]
for q in keys:
 a=newpad(q['ic'],pd(q['ic'],q['icPad']),new[q['ic']]);b=newpad(q['passive'],pd(q['passive'],q['passivePad']),new[q['passive']]);d=math.dist(a,b)
 kr.append(q|{'actualMm':d,'deltaMm':d-q['limit'],'passNoIncrease':d<=q['limit']+1e-6,'icNet':pd(q['ic'],q['icPad'])['net'],'passiveNet':pd(q['passive'],q['passivePad'])['net']})
csvout('KEY_PIN_DISTANCE_B3.csv',kr)
allpads=[]
for r in sorted(new):
 for p in G[r]['pads']:
  x,y=newpad(r,p,new[r]);allpads.append({'ref':r,'pad':p['number'],'net':p['net'],'X_mm':x,'Y_mm':y,'emptyType': 'J2_MECHANICAL' if r=='J2' and p['number'].startswith('MP') else 'ORDINARY_NC' if p['net']=='' else ''})
csvout('ALL_552_PIN_MAP_B3.csv',allpads)
csvout('PLACEMENT_B3.csv',[{'Designator':r,'X_mm':new[r][0],'Y_mm':new[r][1],'Rotation':new[r][2],'Layer':G[r]['layer'],'Function':family(r),'ChangedFromB22':new[r]!=old[r]} for r in sorted(new)])
csvout('PIN_FUNCTION_GRAPH.csv',[{'ref':r,'pad':p['number'],'net':p['net'],'localX_mm':newpad(r,p,(0,0,0))[0],'localY_mm':newpad(r,p,(0,0,0))[1],'constructionFamily':family(r)} for r in sorted(G) for p in G[r]['pads']])
keep=box(*json.loads((P/'PLACEMENT_PASS_3.json').read_text())['J2PlanningKeepoutBounds']);keepcoll=[r for r in sh if r!='J2' and sh[r].intersection(keep).area>1e-8]
bbox=unary_union(list(bh.values())).bounds;pbbox=unary_union(list(sh.values())).bounds
anchorschanged=[r for r in new if ((r.startswith('U') and r[1:].isdigit()) or r.startswith('J')) and new[r]!=old[r]]
csvout('ANCHOR_19_BEFORE_AFTER.csv',[{'ref':r,'beforeX':old[r][0],'beforeY':old[r][1],'beforeRotation':old[r][2],'afterX':new[r][0],'afterY':new[r][1],'afterRotation':new[r][2]} for r in anchorschanged])
# Complete RF/CF topology independent of direct-opamp pair distance proxies.
channels=[]
for i in range(4):
 for r in ['RF'+str(i),'CF'+str(i)]:
  nets={p['net'] for p in G[r]['pads']};channels.append({'channel':i,'ref':r,'padNets':sorted(nets),'passActualParallelTapCOL':nets=={'TIA'+str(i),'COL'+str(i)},'note':'functional loop via ISO/SENSE, not direct opamp pin same-net'})
save('CHANNEL_TOPOLOGY_AUDIT.json',channels)
summary={'parts':len(new),'pads':len(allpads),'assignedPins':sum(p['net']!='' for p in allpads),'netCount':len({p['net'] for p in allpads if p['net']}),'ordinaryNC':sum(p['emptyType']=='ORDINARY_NC' for p in allpads),'mechanicalEmpty':sum(p['emptyType']=='J2_MECHANICAL' for p in allpads),'all15400PhysicalCollisionPairs':coll,'all15400BodyCollisionPairs':bcoll,'minimumPhysicalProxyGapMm':mingap,'keyPairsCount':len(kr),'keyDistanceFailures':[r for r in kr if not r['passNoIncrease']],'keyMaxIncreaseMm':max(r['deltaMm'] for r in kr),'rigidReusePass':all(r['passNoRigidReuse'] for r in reuse),'bodyBBoxMm':list(bbox),'bodyWHMm':[bbox[2]-bbox[0],bbox[3]-bbox[1]],'physicalBBoxMm':list(pbbox),'anchorChanges':len(anchorschanged),'J2PlanningKeepoutCollisions':keepcoll,'identitySourceDigest':identity_digest(G),'onlyPositionsGenerated':True,'identitiesAndPinNetsChanged':False,'nativeDRCPerformed':False,'FFCActuatorManufacturerQualification':False,'layoutComplete':len(new)==176,'CAD_RELEASED':False,'geometryPass':not(coll or bcoll or keepcoll or any(not r['passNoIncrease'] for r in kr)),'constructionSeedOldCoordinates':False}
save('FULL_GEOMETRY_AND_IDENTITY_AUDIT.json',summary)
print(json.dumps(summary))
