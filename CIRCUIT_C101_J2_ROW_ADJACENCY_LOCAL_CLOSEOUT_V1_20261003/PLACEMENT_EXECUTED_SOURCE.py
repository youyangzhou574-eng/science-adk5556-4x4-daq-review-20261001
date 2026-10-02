from floorplan_core import *
import csv,hashlib,traceback,copy
base=json.loads((P/'BASELINE_P1_FULL_PLACEMENT.json').read_text(encoding='utf-8'));before=base['positions'];assert len(before)==101
budget=json.loads((P/'EXECUTION_BUDGET.json').read_text());assert budget['spent']['placement']==0
reserve('candidate',1,'One localROW correction of accepted completeP1; no new globalcandidate')
reserve('placement',1,'One purposeful literalROW macro change and three permitted VEXcompanions, no greedysearch/retry')
(P/'PLACEMENT_EXECUTED_SOURCE.py').write_bytes(Path(__file__).read_bytes())
adjust={
 'U4':[11.735,20.5,90],
 'U1':[11.735,26.1,0],
 'C_MUX':[6.5,19.5,180],
 'C_ROW_OP':[10.5,23.8,0],
 'R_SEL_PD0':[15,17.25,0],
 'R_SEL_PD1':[7.5,16.9,0],
 'R_ENABLE_PD':[17,18,90],
 'RD_TOP':[14.3,25.6,90],
 'RD_B1':[14.1,28.35,0],
 'C_DIV':[12.5,29.5,180]}
ps=copy.deepcopy(before);ps.update(adjust);changed=sorted(r for r in ps if ps[r]!=before[r]);assert set(changed)==set(adjust)
outline=box(0,0,50,50);exclusions=[(r,box(*v))for r,v in base['edgeReserves'].items()]
try:
 assert set(ps)==set(G)==set(ID)
 geo=allpairs(ps);assert geo['pairs']==5050 and not geo['physicalProxyCollisions']and not geo['bodyCollisions'],geo
 assert geo['minimumProxyGapMm']>=.20-1e-9,geo
 outside=[r for r,v in ps.items()if not outline.covers(shape(r,v))]
 intrusions=[[r,owner]for r,v in ps.items()for owner,rect in base['edgeReserves'].items()if r!=owner and shape(r,v).intersects(box(*rect))]
 assert not outside and not intrusions,(outside,intrusions)
 rows=[]
 for i in range(4):
  pins=[q['number']for q in G['U4']['pads']if q['net']=='ROW'+str(i)];assert len(pins)==2
  for n in pins:
   old=dist(pad('J2',i+1,before['J2']),pad('U4',n,before['U4']));new=dist(pad('J2',i+1,ps['J2']),pad('U4',n,ps['U4']))
   rows.append({'ROW':i,'J2pin':i+1,'U4pin':n,'beforeMm':old,'afterMm':new,'deltaMm':new-old,'nonIncreasing':new<=old+1e-9})
 assert len(rows)==8 and all(q['nonIncreasing']for q in rows)
 imbalance=[]
 for i in range(4):
  rr=[q for q in rows if q['ROW']==i];old=abs(rr[0]['beforeMm']-rr[1]['beforeMm']);new=abs(rr[0]['afterMm']-rr[1]['afterMm']);imbalance.append({'ROW':i,'beforeAbsDifferenceMm':old,'afterAbsDifferenceMm':new,'deltaMm':new-old})
 compact=[]
 for a,ap,b,bp,label in [('U1',1,'U4',8,'ROW_DRV'),('U1',4,'U4',9,'ROW_FB')]:
  assert net(a,ap)==net(b,bp)==label
  old=dist(pad(a,ap,before[a]),pad(b,bp,before[b]));new=dist(pad(a,ap,ps[a]),pad(b,bp,ps[b]));compact.append({'net':label,'beforeMm':old,'afterMm':new,'deltaMm':new-old})
 # Conservative desk compactness criterion: neither existing driver/FBproxy grows. Pro gave no electricalmm gate.
 assert all(q['deltaMm']<=1e-9 for q in compact),compact
 assert ps['U4'][1]<=29.0 and ps['J2']==before['J2']
 assert all(ps[r]==before[r]for r in ps if r not in adjust)
 actual=list(csv.DictReader((P/'FINAL_COLD_CAPTURE_ALL_PINS.csv').open(encoding='utf-8-sig')))
 for q in actual:
  an=q['actualNet']or None;assert net(q['ref'],q['pin'])==an and (q['NC'].lower()=='true')==(an is None)
 assert len(actual)==363
 for q in json.loads((P/'INPUT_SHA_REGISTER.json').read_text()):
  assert hashlib.sha256((P/q['copy']).read_bytes()).hexdigest()==q['sha256']and hashlib.sha256(Path(q['source']).read_bytes()).hexdigest()==q['sha256']
 def writecsv(name,rr):
  with(P/name).open('w',encoding='utf-8',newline='')as f:
   w=csv.DictWriter(f,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
 writecsv('EIGHT_ROW_DRIVE_SENSE_BEFORE_AFTER.csv',rows)
 writecsv('FOUR_ROW_DRIVE_SENSE_IMBALANCE.csv',imbalance)
 writecsv('ROW_DRIVER_AND_FEEDBACK_BEFORE_AFTER.csv',compact)
 changes=[{'ref':r,'oldX':before[r][0],'oldY':before[r][1],'oldRotation':before[r][2],'newX':ps[r][0],'newY':ps[r][1],'newRotation':ps[r][2],'role':'explicitPermittedVEXCompanion'if r in ['RD_TOP','RD_B1','C_DIV']else'approvedROWMacro'}for r in changed]
 writecsv('TEN_ALLOWED_COMPONENT_CHANGES.csv',changes)
 writecsv('ALL101_LOCAL_FINAL_PLACEMENT.csv',[{'ref':r,'xMm':v[0],'yMm':v[1],'rotation':v[2],'changed':r in adjust}for r,v in sorted(ps.items())])
 audit={'all101Placed':True,'actualSignalPins':363,'connected':323,'nets':54,'NC':40,'identityAndInputSHAUnchanged':True,'boardPlanningMm':[50,50],'all5050Geometry':geo,'outside':outside,'reserveIntrusions':intrusions,'changedParts':changed,'frozenOther91':True,'J2PinSideDefinitionUnchanged':True,'U4OnROWSide':True,'ROWCOLBoundaryYmm':29.0,'all8RowPathsNonIncreasing':True,'all4ImbalanceReduced':all(q['deltaMm']<=0 for q in imbalance),'rowAmpDriverFeedbackBothNonIncreasing':True,'rowMacroPurposefulLiteralChangeNotGreedy':True,'ADC_TIA_16Bank_RFCF_RADC_CADC_Frozen':True,'J2ExactMechanicalQualified':False,'nativeOperations':0}
 # Record very small nonintrusion margin without presenting it as mechanicalqualification.
 audit['minimumNonOwnerReserveGapMm']=min(shape(r,v).distance(rect)for r,v in ps.items()for owner,rect in exclusions if owner!=r)
 final={**base,'candidate':'P1_ROW_LOCAL','positions':ps,'geometryAudit':geo,'localChange':adjust,'baselineCommit':'055c73356a4d124ccd58867c7206d6b0353daf5e','noGlobalPlacementOptimization':True}
 (P/'LOCAL_FINAL_FULL101_PLACEMENT.json').write_text(json.dumps(final,indent=2),encoding='utf-8')
 (P/'FULL_LOCAL_AUDIT.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
 gates={'OFFLINE_FULL101_REVIEW_READY':True,'ALL_MACRO_LAYOUT_INTENTS_ACCEPTED':True,'J2_PIN_SIDE_ROW_ADJACENCY_HOLD':False,'NATIVE_PLACEMENT_ELIGIBLE':True,'CAD_RELEASED':False,'PCB_ROUTING_RELEASED':False,'FFC_MECHANICAL_QUALIFIED':False,'ERC_DETAIL_HOLD':True,'LEGACY_ANNOTATION_HOLD':True,'MLCC_CEFF_HOLD':True,'SYSTEM_PERFORMANCE_ACCEPTED':False,'BENCH_RELEASED':False,'MANUFACTURE_RELEASED':False,'USER_VISUAL_ACCEPTANCE':'PENDING'}
 (P/'GATES.json').write_text(json.dumps(gates,indent=2),encoding='utf-8')
 budget=json.loads((P/'EXECUTION_BUDGET.json').read_text());budget['coordinateSTOP']=True;budget['phase']='LOCAL_COORDINATE_ONE_ATTEMPT_COMPLETE_ONLY_APPROVED_IMAGE_REMAINING';(P/'EXECUTION_BUDGET.json').write_text(json.dumps(budget,indent=2),encoding='utf-8')
 print(json.dumps({'all101':True,'changed':len(changed),'minGap':geo['minimumProxyGapMm'],'reserveGap':audit['minimumNonOwnerReserveGapMm'],'eight':rows,'compact':compact,'imbalance':imbalance}))
except Exception as e:
 (P/'ONE_ATTEMPT_FAILED_PROPOSAL.json').write_text(json.dumps({'positions':ps,'adjust':adjust,'error':str(e)},indent=2),encoding='utf-8');(P/'ONE_ATTEMPT_FAILURE.log').write_text(traceback.format_exc(),encoding='utf-8')
 budget=json.loads((P/'EXECUTION_BUDGET.json').read_text());budget.update(STOP=True,coordinateSTOP=True,STOPReason='ONE_LOCAL_ATTEMPT_NOT_QUALIFIED_NO_RETRY',STOPUTC=datetime.datetime.now(datetime.timezone.utc).isoformat());(P/'EXECUTION_BUDGET.json').write_text(json.dumps(budget,indent=2),encoding='utf-8');raise
