from floorplan_core import *
import sys,csv,traceback,hashlib
attempt=int(sys.argv[1]) if len(sys.argv)>1 else 1
assert attempt in (1,2,3,4)
name='P1' if attempt<=3 else 'P2'
b=json.loads((P/'EXECUTION_BUDGET.json').read_text(encoding='utf-8'))
assert b['spent']['placement']==attempt-1,'Sequential attempts only; no hidden replay'
if attempt==1:reserve('candidate',1,'Blank horizontal P1, planning50x50; no old coordinates read')
if attempt==4:reserve('candidate',1,'Conditional P2 single-edge52x50 contingency after P1 evidence')
reserve('placement',1,'Full bank-first placement attempt '+str(attempt)+'; every failure charged')
script=Path(__file__).read_bytes();(P/('ATTEMPT'+str(attempt)+'_EXECUTED_SCRIPT.py')).write_bytes(script)
targets=json.loads((P/'FUNCTIONAL_TARGET_REGISTER.json').read_text(encoding='utf-8'))
W,H=(52,50) if name=='P2' else (50,50)
outline=box(0,0,W,H);placed={};order=[];stages=[]
reserves={'J2':[-10,21,8,37],'J1':[3,-10,13,5.5],'J3':[W-5.5,32,W+10,49],'J4':[W-5.5,14,W+10,27]}
exclusions=[(r,box(*v)) for r,v in reserves.items()]
banks={
 'REFIO':{'pin':'5','tiers':[['C_ADC_REFIO','C_REFIO_B']]},
 'REFCAP':{'pin':'7','tiers':[['C_ADC_REFCAP'],['C_REFCAP_BULKA','C_REFCAP_BULKB']]},
 'AVDD9':{'pin':'9','tiers':[['C_ADCA1'],['C_AVDD9_HF'],['C_AVDD9A','C_AVDD9B']]},
 'AVDD30':{'pin':'30','tiers':[['C_ADCA2'],['C_AVDD30_HF'],['C_AVDD30A','C_AVDD30B']]},
 'DVDD34':{'pin':'34','tiers':[['C_ADCD'],['C_DVDD34A','C_DVDD34B']]}}
bankrefs=[r for v in banks.values() for tier in v['tiers'] for r in tier]
assert len(bankrefs)==len(set(bankrefs))==16
for r,edges in targets.items():
 for a,owner,pin,kind in edges:assert net(r,a)==net(owner,pin) and net(r,a) is not None
rotated={(r,a):rotate(LOCAL_PHYS[r],a,origin=(0,0))for r in G for a in [0,90,180,270]}
existing=[]
def put(r,pos):
 assert r not in placed and legal(r,pos,placed,outline,exclusions),('illegal fixed',r,pos)
 placed[r]=pos;order.append(r);existing.append(shape(r,pos))
def near(r,target=None,angle=None,minimum_primary=0):
 edges=targets.get(r,[])
 if target is None:
  prim=[e for e in edges if e[3]=='primary'];assert prim and all(e[1]in placed for e in edges),(r,'owner missing')
  target=tuple(sum(pad(e[1],e[2],placed[e[1]])[k] for e in prim)/len(prim)for k in [0,1])
 angles=[angle] if angle is not None else [0,90,180,270]
 # Nearpin half-mm grid plus wholeboard1mm lattice. No8.2 radius; all legalboard reachable.
 points={(round(target[0]*2)/2+ix*.5,round(target[1]*2)/2+iy*.5)for ix in range(-22,23)for iy in range(-22,23)}
 points.update((float(x),float(y))for x in range(1,int(W))for y in range(1,int(H)))
 candidates=[]
 for x,y in points:
  if not(.35<x<W-.35 and .35<y<H-.35):continue
  for a in angles:
   pos=[x,y,a]
   distances=[dist(pad(r,e[0],pos),pad(e[1],e[2],placed[e[1]]))for e in edges]
   primary=[d for d,e in zip(distances,edges)if e[3]=='primary']
   if primary and min(primary)<minimum_primary-1e-9:continue
   cost=sum(d*(1 if e[3]=='primary'else .35)for d,e in zip(distances,edges))+.06*dist((x,y),target)
   if not edges:cost=dist((x,y),target)
   candidates.append((cost,x,y,a))
 tree=STRtree(existing)if existing else None
 for cost,x,y,a in sorted(candidates):
  s=translate(rotated[r,a],xoff=x,yoff=y)
  if attempt>=2 and r in bankrefs and s.bounds[0]<29.0-1e-9:continue
  if not outline.buffer(-.35).covers(s):continue
  if any(owner!=r and s.intersects(keep)for owner,keep in exclusions):continue
  if tree is not None and any(s.distance(existing[i])<.20-1e-9 for i in tree.query(s.buffer(.20))):continue
  put(r,[x,y,a]);return
 raise ValueError('No legal full-board location: '+r)
def stage(label):
 stages.append({'stage':label,'placed':len(placed),'refsInOrder':order[:]})
 (P/(name+'_ATTEMPT'+str(attempt)+'_STAGE_PROGRESS.json')).write_text(json.dumps({'stages':stages,'positions':placed},indent=2),encoding='utf-8')
try:
 for r,pos in [('J2',[3.5,29,0]),('J1',[8,2.8,0]),('J3',[W-2.8,40.5,90]),('J4',[W-2.8,20.5,90])]:put(r,pos)
 stage('INTERFACE_EDGE_REGIONS')
 put('U5',[30,25,180])
 # Shared tier sweep: all actual HF/100nF first, then2.2uF, then whole bulk banks.
 tierorder=['C_ADCA1','C_ADCA2','C_ADCD','C_ADC_REFCAP','C_AVDD9_HF','C_AVDD30_HF','C_ADC_REFIO','C_REFIO_B','C_REFCAP_BULKA','C_REFCAP_BULKB','C_AVDD9A','C_AVDD9B','C_AVDD30A','C_AVDD30B','C_DVDD34A','C_DVDD34B']
 minimum={}
 for r in tierorder:
  bank=next(v for v in banks.values()if any(r in t for t in v['tiers']))
  prior=[q for tier in bank['tiers'] for q in tier if q in placed and tier!=bank['tiers'][-1]]
  # Preserve physical primarypin proximity order, without invented absolute length limits.
  lower=0
  for q in prior:
   ee=[e for e in targets[q]if e[3]=='primary'];lower=max(lower,min(dist(pad(q,e[0],placed[q]),pad(e[1],e[2],placed[e[1]]))for e in ee))
  near(r,minimum_primary=lower)
 stage('ADC_U5_AND_ALL16_BANK_CAPS_COMPLETE')
 near('U2',[15.5,25.5] if attempt==1 else [20,25.5],0 if attempt==1 else 180)
 channels={0:[1,2],1:[7,6],2:[8,9],3:[14,13]}
 cx,cy=placed['U2'][:2]
 for i,(out,minus)in channels.items():
  sx=-1 if pad('U2',out,placed['U2'])[0]<cx else 1
  sy=-1 if pad('U2',out,placed['U2'])[1]<cy else 1
  for typ,off in [('RF',4.35),('CF',5.45)]:
   r=typ+str(i);xy=[cx+sx*(3.3 if attempt==1 else 3.175),cy+sy*off]
   a=0 if attempt==1 else min([0,180],key=lambda a:sum(dist(pad(r,e[0],[*xy,a]),pad(e[1],e[2],placed[e[1]]))for e in targets[r]if e[3]=='primary'))
   put(r,[*xy,a])
 near('C_TIA_OP')
 for i in range(4):
  r='C_ADC'+str(i)
  if attempt==1:near(r)
  else:
   # Paired top/bottom AIN fanout cells; keep caps next to ADC, ADCbank remains right.
   xy=[[27,30],[25.5,30],[25.5,20],[27,20]][i]
   a=min([90,270],key=lambda a:sum(dist(pad(r,e[0],[*xy,a]),pad(e[1],e[2],placed[e[1]]))for e in targets[r]))
   put(r,[*xy,a])
 for i in range(4):near('R_ADC'+str(i))
 stage('FOUR_TIA_FEEDBACK_AND_ADC_FILTERS')
 near('U4',[14,37.5],0);near('U1',[21.5,37],0)
 for r in ['C_MUX','C_ROW_OP','R_SEL_PD0','R_SEL_PD1','R_ENABLE_PD','D_FFC_ROW','D_FFC_COL']:near(r)
 stage('ROW_DRIVE_SENSE_AND_FFC_ESD')
 near('U6',[22,32.5],0)
 for r in ['C_REF','C_VCM_OUT','C_DIV','RD_TOP','RD_B1']:near(r)
 stage('REF_VCM_VEXC_COMPLETE')
 power={'U9':[12,8,0],'U8':[26,8,180],'U11':[19,9,0],'U12':[33,9,0]}
 for ic,pos in power.items():near(ic,pos[:2],pos[2])
 # VDD/CT/sense andcaps before resistor/bleed hardware, fullpowerbank aheadMCU.
 powerrefs=[r for r in targets if r not in placed and any(e[1]in power for e in targets[r])]
 for r in sorted(powerrefs,key=lambda r:(0 if r.endswith('VDD_C')or r.endswith('CT_C')or r.endswith('SENSE_C')else 1 if r.startswith('C')or r.endswith('CAP')else 2,r)):near(r)
 stage('POWER_ALL_CAPS_SUPERVISORS_AND_BLEEDS')
 near('U7',[37.5,40],270)
 for r in ['C_MCU1','C_MCU_BULK','R_RST','R_CS_PU','R_ADC_RESET_PD']:near(r)
 for r in sorted(set(G)-set(placed)):near(r)
 stage('ALL101_COMPLETE')
 assert set(placed)==set(G)and len(placed)==101
 audit=allpairs(placed);assert audit['pairs']==5050 and not audit['bodyCollisions']and not audit['physicalProxyCollisions']
 result={'candidate':name,'attempt':attempt,'boardPlanningMm':[W,H],'positions':placed,'placementOrder':order,'stages':stages,'edgeReserves':reserves,'banks':banks,'geometryAudit':audit,'actualNativeOutlineChanged':False,'J2ExactMechanicalHOLD':True,'oldCoordinatesUsed':False}
 (P/(name+'_FULL_PLACEMENT.json')).write_text(json.dumps(result,indent=2),encoding='utf-8')
 with(P/(name+'_FULL_PLACEMENT.csv')).open('w',encoding='utf-8',newline='')as f:
  w=csv.writer(f);w.writerow(['ref','xMm','yMm','rotation']);w.writerows([r,*pos]for r,pos in sorted(placed.items()))
 print(json.dumps({'candidate':name,'attempt':attempt,'placed':len(placed),'audit':audit}))
except Exception as e:
 (P/(name+'_ATTEMPT'+str(attempt)+'_PARTIAL.json')).write_text(json.dumps({'candidate':name,'boardPlanningMm':[W,H],'positions':placed,'stages':stages,'unplaced':sorted(set(G)-set(placed)),'error':str(e)},indent=2),encoding='utf-8')
 (P/('ATTEMPT'+str(attempt)+'_FAILURE.log')).write_text(traceback.format_exc(),encoding='utf-8');raise
