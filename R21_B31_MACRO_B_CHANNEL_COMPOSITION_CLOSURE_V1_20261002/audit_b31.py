from b31_core import *
from audit_core import rigid_reuse,identity_digest
from scipy.optimize import milp,LinearConstraint,Bounds
from scipy.sparse import lil_matrix
from construct_b31 import roles,channel_frame
import hashlib
def csvout(n,rows):
 with (P/n).open('w',encoding='utf8',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def channel_audit(pos):
 out=[]
 for f,ic in [('TIA','U2'),('ROW','U1')]:
  samples={};missing=[]
  for i in range(4):
   a,s=channel_frame(ic,i,pos)
   for role,r in roles(f,i).items():
    if r not in pos:missing.append(r);continue
    centre=(np.array(pos[r][:2])-a)*s
    expected=(90 if s[1]<0 else 270) if role in ['HF','RF','CF'] else (0 if s[0]>0 else 180) if role in ['ISO','CLAMP'] else (180 if s[0]>0 else 0)
    samples.setdefault(role,[]).append({'channel':i,'ref':r,'canonicalCentreMm':centre.tolist(),'rotation':pos[r][2],'expectedRotation':expected,'anglePass':pos[r][2]%360==expected})
  rr=[]
  for role,ss in samples.items():
   dev=max(np.linalg.norm(np.array(x['canonicalCentreMm'])-ss[0]['canonicalCentreMm']) for x in ss)
   rr.append({'role':role,'channels':ss,'maxCanonicalCentreDeltaMm':float(dev),'pass':len(ss)==4 and dev<=1e-5 and all(x['anglePass'] for x in ss)})
  out.append({'family':f,'expectedRoleRefs':sum(len(roles(f,i)) for i in range(4)),'missingRefs':missing,'roles':rr,'pass':not missing and len(rr)==len(roles(f,0)) and all(x['pass'] for x in rr),'meaning':'same complete functional-role centres in mirrored actual output/sense-pin midpoint frames, role-dependent inward orientation; rotations realizable; no claim every 3-pin clamp rail pad is exact mirror, no routing qualification'})
 return out
def reuse_bound(a,b):
 refs=sorted(a);n=len(refs);bad=[(i,j) for i,j in itertools.combinations(range(n),2) if abs(math.dist(a[refs[i]][:2],a[refs[j]][:2])-math.dist(b[refs[i]][:2],b[refs[j]][:2]))>1+1e-8]
 mat=lil_matrix((len(bad),n))
 for k,(i,j) in enumerate(bad):mat[k,i]=mat[k,j]=1
 res=milp(-np.ones(n),integrality=np.ones(n),bounds=Bounds(np.zeros(n),np.ones(n)),constraints=LinearConstraint(mat.tocsr(),np.full(len(bad),-np.inf),np.ones(len(bad))),options={'time_limit':3})
 ub=math.floor(-float(res.mip_dual_bound)+1e-7) if res.mip_dual_bound is not None else n
 return {'upperBoundCount':ub,'upperBoundFraction':ub/n,'solverStatus':int(res.status),'valid':res.mip_dual_bound is not None,'pass':res.mip_dual_bound is not None and ub/n<=.7}
def run():
 pos=json.loads((P/'PLACEMENT_B31.json').read_text())['positions'];old=json.loads((P/'PLACEMENT_B22.json').read_text())['positions'];a3=json.loads((P/'PLACEMENT_B3.json').read_text())['positions']
 assert set(pos)==set(G)
 sh={r:physical(r,v) for r,v in pos.items()};bh={r:body(r,v) for r,v in pos.items()};coll=[];bcoll=[];gap=999;paircount=0
 for a,b in itertools.combinations(sorted(pos),2):
  paircount+=1;gap=min(gap,sh[a].distance(sh[b]))
  if sh[a].intersection(sh[b]).area>1e-8:coll.append([a,b])
  if bh[a].intersection(bh[b]).area>1e-8:bcoll.append([a,b])
 kr=[]
 for q in keys:
  d=math.dist(pt(pos,q['ic'],q['icPad']),pt(pos,q['passive'],q['passivePad']));kr.append(q|{'actualMm':d,'deltaMm':d-q['limit'],'pass':d<=q['limit']+1e-6,'icNet':pd(q['ic'],q['icPad'])['net'],'passiveNet':pd(q['passive'],q['passivePad'])['net']})
 csvout('KEY_PIN_DISTANCE_B31.csv',kr)
 ap=[]
 for r in sorted(G):
  for p in G[r]['pads']:
   x,y=newpad(r,p,pos[r]);ap.append({'ref':r,'pad':p['number'],'net':p['net'],'X_mm':x,'Y_mm':y,'emptyType':'J2_MECHANICAL' if r=='J2' and p['number'].startswith('MP') else 'ORDINARY_NC' if not p['net'] else ''})
 csvout('ALL_552_PIN_MAP_B31.csv',ap);csvout('PLACEMENT_B31.csv',[{'Designator':r,'X_mm':pos[r][0],'Y_mm':pos[r][1],'Rotation':pos[r][2],'Function':family(r)} for r in sorted(pos)])
 channels=channel_audit(pos);save('CHANNEL_CELL_REPEATABILITY.json',channels)
 reuse=[]
 for f in ['TIA','ROW','ADC','BIAS_MUX','POWER','DIGITAL']:
  rr=[r for r in pos if family(r)==f];reuse.append({'family':f,'refs':rr,**reuse_bound({r:old[r] for r in rr},{r:pos[r] for r in rr})})
 save('OLD_BLOCK_RIGID_REUSE_AUDIT.json',reuse)
 edges=[]
 def add(lane,a,ap,b,bp):
  assert pd(a,ap)['net']==pd(b,bp)['net'] and pd(a,ap)['net']
  before=math.dist(pt(old,a,ap),pt(old,b,bp));after=math.dist(pt(pos,a,ap),pt(pos,b,bp));failed=math.dist(pt(a3,a,ap),pt(a3,b,bp));edges.append({'lane':lane,'fromRef':a,'fromPad':ap,'toRef':b,'toPad':bp,'net':pd(a,ap)['net'],'B22Mm':before,'B3AMm':failed,'B31Mm':after,'deltaVsB22Mm':after-before,'deltaVsB3AMm':after-failed})
 for i,op in enumerate([1,7,8,14]):
  add('TIA_CH'+str(i),'U2',op,'R_TIA_ISO'+str(i),1);add('TIA_CH'+str(i),'R_TIA_ISO'+str(i),2,'R_ADC'+str(i),1);add('TIA_CH'+str(i),'R_ADC'+str(i),2,'C_ADC'+str(i),1);add('TIA_CH'+str(i),'C_ADC'+str(i),1,'U5',[16,18,21,23][i]);add('ROW_CH'+str(i),'U1',op,'R_ISO'+str(i),1);add('ROW_CH'+str(i),'R_ISO'+str(i),2,'J2',i+1)
 for u,m in [(1,14),(36,13),(37,12),(38,11)]:add('SPI','U5',u,'U7',m)
 add('POWER','J1',1,'U9',5);add('POWER','U9',6,'U8',1);add('POWER','U8',5,'U10',5)
 csvout('REPRESENTATIVE_SIGNAL_EDGE_COMPARISON.csv',edges)
 bb=unary_union(list(bh.values())).bounds;comp={'bodyBBoxMm':list(bb),'bodyWidthHeightMm':[bb[2]-bb[0],bb[3]-bb[1]],'physicalBBox':bbox(pos),'largestSampledInternalEmptyRectangle':empty_rectangle(sh.values()),'macroEdges':macro_audit({r:pos[r] for r in json.loads((P/'MACRO_SELECTION.json').read_text())['positions']})['edges'],'selectedRepresentative31EdgeSumMm':sum(e['B31Mm'] for e in edges),'B3A31EdgeSumMm':sum(e['B3AMm'] for e in edges),'B2231EdgeSumMm':sum(e['B22Mm'] for e in edges),'increasedVsB22':[e for e in edges if e['deltaVsB22Mm']>1e-6]};save('MACRO_COMPOSITION_AUDIT.json',comp)
 pfile=json.loads((P/('PLACEMENT_PASS_'+str(json.loads((P/'PLACEMENT_B31.json').read_text())['pass'])+'.json')).read_text());keep=box(*pfile['J2PlanningKeepoutBounds']);kc=[r for r in sh if r!='J2' and sh[r].intersection(keep).area>1e-8]
 hashes=[{'path':v['path'],'sha256':hashlib.sha256(Path(v['path']).read_bytes()).hexdigest(),'pass':hashlib.sha256(Path(v['path']).read_bytes()).hexdigest()==v['sha256']} for v in json.loads((P/'INPUT_MANIFEST.json').read_text())];save('FROZEN_INPUT_HASH_VERIFICATION.json',hashes)
 rowedges=[e for e in edges if e['lane'].startswith('ROW') and e['toRef']=='J2'];powerin=next(e for e in edges if e['fromRef']=='J1')
 # Specific engineering threshold: any four ROW-to-J2 edges <=+5mm vsB22; zero is better. Not a new electrical requirement.
 rowok=all(e['deltaVsB22Mm']<=5+1e-6 for e in rowedges);pwrok=powerin['deltaVsB22Mm']<=1e-6
 count={'parts':len(pos),'pads':len(ap),'assignedPins':sum(bool(p['net']) for p in ap),'nets':len({p['net'] for p in ap if p['net']}),'ordinaryNC':sum(p['emptyType']=='ORDINARY_NC' for p in ap),'mechanicalEmpty':sum(p['emptyType']=='J2_MECHANICAL' for p in ap)}
 summary=count|{'allPairCount':paircount,'bodyCollisionPairs':bcoll,'physicalProxyCollisionPairs':coll,'minimumPhysicalGapMm':gap,'keyCount':len(kr),'keyFailures':[x for x in kr if not x['pass']],'channelPass':all(x['pass'] for x in channels),'keyMaxDeltaMm':max(x['deltaMm'] for x in kr),'noOldRigidReuse':all(x['pass'] for x in reuse),'J2PlanningKeepoutCollisions':kc,'rowChainPass':rowok,'rowChainThresholdVsB22Mm':5,'rowChainActual':rowedges,'powerInputPassNoIncrease':pwrok,'powerInputActual':powerin,'frozenInputsPass':all(x['pass'] for x in hashes),'identityDigest':identity_digest(G),'geometryPass':not(coll or bcoll or kc) and all(x['pass'] for x in kr),'CAD_RELEASED':False,'nativeDRCPerformed':False,'actuatorExactMechanicalQualified':False}
 summary['candidateFinalHardGate']=count=={'parts':176,'pads':552,'assignedPins':514,'nets':107,'ordinaryNC':36,'mechanicalEmpty':2} and summary['geometryPass'] and summary['channelPass'] and summary['noOldRigidReuse'] and rowok and pwrok and summary['frozenInputsPass']
 save('FULL_GEOMETRY_AND_IDENTITY_AUDIT.json',summary);print(json.dumps(summary))
if __name__=='__main__':run()
