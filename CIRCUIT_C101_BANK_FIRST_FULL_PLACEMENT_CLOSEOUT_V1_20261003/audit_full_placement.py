from floorplan_core import *
import csv,hashlib,statistics,shutil
O=P.parent/'CIRCUIT_C101_OFFLINE_PCB_FLOORPLAN_AND_PLACEMENT_REVIEW_V1'
register=json.loads((P/'INPUT_SHA_REGISTER.json').read_text(encoding='utf-8'))
for name in ['FINAL_COLD_CAPTURE_ALL_PINS.csv','FINAL_COLD_CAPTURE_ACTUAL_BOM.csv','DRAWING_ANNOTATION_ADDENDUM.md']:
 if not (P/name).exists():
  data=(O/name).read_bytes();(P/name).write_bytes(data);register.append({'source':str(O/name),'copy':name,'size':len(data),'sha256':hashlib.sha256(data).hexdigest()})
(P/'INPUT_SHA_REGISTER.json').write_text(json.dumps(register,indent=2),encoding='utf-8')
integrity=[{'file':q['copy'],'copySHAUnchanged':hashlib.sha256((P/q['copy']).read_bytes()).hexdigest()==q['sha256'],'sourceSHAUnchanged':hashlib.sha256(Path(q['source']).read_bytes()).hexdigest()==q['sha256']}for q in register]
assert all(q['copySHAUnchanged']and q['sourceSHAUnchanged']for q in integrity)
actual=list(csv.DictReader((P/'FINAL_COLD_CAPTURE_ALL_PINS.csv').open(encoding='utf-8-sig')))
pinrows=[]
for q in actual:
 r,n=q['ref'],q['pin'];v=actualpin(r,n);nc=q['NC'].lower()=='true';an=q['actualNet']or None
 ok=v['net']==an and nc==(an is None)
 pinrows.append({'ref':r,'pin':n,'actualNet':an,'geometryNet':v['net'],'NC':nc,'match':ok})
assert len(pinrows)==363 and all(q['match']for q in pinrows)
assert {r:{q['number']for q in g['pads']}for r,g in G.items()}=={r:{str(q['number'])for q in v['pins']}for r,v in ID.items()}
d=json.loads((P/'P1_FULL_PLACEMENT.json').read_text());ps=d['positions'];assert set(ps)==set(G)==set(ID)and len(ps)==101
geo=allpairs(ps);assert geo['pairs']==5050 and not geo['bodyCollisions']and not geo['physicalProxyCollisions']
W,H=d['boardPlanningMm'];outline=box(0,0,W,H)
bound=[r for r,v in ps.items()if not outline.covers(shape(r,v))]
intrusions=[[r,owner]for r,v in ps.items()for owner,rect in d['edgeReserves'].items()if owner!=r and shape(r,v).intersects(box(*rect))]
assert not bound and not intrusions
targets=json.loads((P/'FUNCTIONAL_TARGET_REGISTER.json').read_text());edges=[]
for r,es in targets.items():
 for a,owner,n,kind in es:
  assert net(r,a)==net(owner,n) and net(r,a) is not None
  edges.append({'ref':r,'pad':a,'owner':owner,'ownerPin':n,'kind':kind,'net':net(r,a),'distanceMm':dist(pad(r,a,ps[r]),pad(owner,n,ps[owner]))})
bankrows=[];bankgates=[]
for label,b in d['banks'].items():
 previous_max=0
 for tierno,tier in enumerate(b['tiers']):
  values=[]
  for r in tier:
   primary=[e for e in edges if e['ref']==r and e['kind']=='primary']
   assert all(e['owner']=='U5' and e['ownerPin']==b['pin']for e in primary)
   v=min(e['distanceMm']for e in primary);values.append(v)
   bankrows.append({'bank':label,'ref':r,'tier':tierno,'U5pin':b['pin'],'value':ID[r]['props']['Value'],'primaryDistanceMm':v,'order':d['placementOrder'].index(r)})
  bankgates.append({'bank':label,'tier':tierno,'tierNotCloserThanPrevious':min(values)>=previous_max-1e-9})
  previous_max=max(values)
assert len(bankrows)==16 and all(x['tierNotCloserThanPrevious']for x in bankgates)
assert max(x['order']for x in bankrows)<d['placementOrder'].index('U2')
channelrows=[]
for i,out,minus,ain in [(0,1,2,16),(1,7,6,18),(2,8,9,21),(3,14,13,23)]:
 vals={}
 for typ in ['RF','CF','R_ADC']:
  r=typ+str(i);es=[e for e in edges if e['ref']==r and e['kind']=='primary'];assert len(es)==2
  vals[typ+'twoLeadStubSumMm']=sum(e['distanceMm']for e in es)
 c=next(e['distanceMm']for e in edges if e['ref']=='C_ADC'+str(i)and e['kind']=='primary')
 channelrows.append({'channel':i,'TIAoutPin':out,'TIAminusPin':minus,'ADCpin':ain,**vals,'C_ADCPrimaryStubMm':c})
# Actual five digital interface chains cross explicit series resistors; never claim MCU and external J pins same-net.
digital=[]
for icpin,r,j,jpin in [(24,'R_J3_3','J3',3),(25,'R_J3_4','J3',4),(6,'R_J3_5','J3',5),(19,'R_J4_3','J4',3),(21,'R_J4_4','J4',4)]:
 internal=next(q for q in G[r]['pads']if q['net']==net('U7',icpin));external=next(q for q in G[r]['pads']if q['net']==net(j,jpin));assert internal['number']!=external['number']
 a=dist(pad('U7',icpin,ps['U7']),pad(r,internal['number'],ps[r]));bb=dist(pad(r,external['number'],ps[r]),pad(j,jpin,ps[j]));span=dist(pad(r,internal['number'],ps[r]),pad(r,external['number'],ps[r]))
 digital.append({'U7pin':icpin,'R':r,'J':j,'Jpin':jpin,'internalNet':internal['net'],'externalNet':external['net'],'MCUtoRstubMm':a,'RspanMm':span,'RtoJstubMm':bb,'totalIncludingResistorSpanMm':a+bb+span})
def writecsv(name,rows):
 with(P/name).open('w',encoding='utf-8',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
writecsv('ALL363_ACTUAL_PIN_GEOMETRY_IDENTITY_AUDIT.csv',pinrows)
writecsv('ALL_FUNCTIONAL_172_SAME_NET_PROXY_EDGES.csv',edges)
writecsv('ADC16_BANK_PRIORITY_AND_PIN_DISTANCES.csv',bankrows)
writecsv('FOUR_TIA_ADC_CHANNEL_PROXY_DISTANCES.csv',channelrows)
writecsv('FIVE_DIGITAL_SERIES_INTERFACE_CHAINS.csv',digital)
old=list(csv.DictReader((O/'CANDIDATE_COMPARISON.csv').open(encoding='utf-8')))
newmean=statistics.mean(x['R_ADCtwoLeadStubSumMm']for x in channelrows);newmax=max(x['R_ADCtwoLeadStubSumMm']for x in channelrows)
compare=[{'version':x['candidate']+'_OLD_PARTIAL','placed':x['placed'],'meanTIA_RADC_ADCStubMm':x['meanTIA_RADC_ADCPinStubSumMm'],'maxTIA_RADC_ADCStubMm':x['maxTIA_RADC_ADCPinStubSumMm'],'maxRF_CFStubMm':x['maxRF_CFtwoLeadStubSumMm']}for x in old]
compare.append({'version':'P1_FULL_BANK_FIRST_ATTEMPT2','placed':101,'meanTIA_RADC_ADCStubMm':newmean,'maxTIA_RADC_ADCStubMm':newmax,'maxRF_CFStubMm':max(x[k]for x in channelrows for k in ['RFtwoLeadStubSumMm','CFtwoLeadStubSumMm'])})
writecsv('BEFORE_AFTER_PARTIAL_VS_FULL_PROXY_COMPARISON.csv',compare)
# Meaning of basic repetition: exact fourRF/CF center2+2 template + paired ADCcaps; R_ADC legalfanout differs, not exact completechannel mirror.
repeat={'fourRFFeedbackStubSpreadMm':max(x['RFtwoLeadStubSumMm']for x in channelrows)-min(x['RFtwoLeadStubSumMm']for x in channelrows),'fourCFFeedbackStubSpreadMm':max(x['CFtwoLeadStubSumMm']for x in channelrows)-min(x['CFtwoLeadStubSumMm']for x in channelrows),'ADCcapsPairedTopBottom':ps['C_ADC0'][:2]==[27,30] and ps['C_ADC3'][:2]==[27,20]and ps['C_ADC1'][:2]==[25.5,30]and ps['C_ADC2'][:2]==[25.5,20],'completeChannelExactMirrorClaimed':False,'R_ADCfanoutPositionsDifferent':True}
rowpins=[(q['number'],q['net'])for q in G['U4']['pads']]
row={'ROW0to3':{str(i):{'J2pin':str(i+1),'net':net('J2',i+1),'MUXpins':[n for n,nn in rowpins if nn=='ROW'+str(i)]}for i in range(4)},'driveFeedbackNetPins':[(q['number'],q['net'])for r in ['U1','U4']for q in G[r]['pads']if q['net']in['ROW_DRV','ROW_FB','ROW_COM','VEXC']],'staticConnectivityOnly':True}
assert all(q['MUXpins']for q in row['ROW0to3'].values())
a={'all101Placed':True,'all101InsidePlanningOutline':not bound,'all5050BodyAndPhysicalProxyNoOverlap':True,'minimumPhysicalProxyGapMm':geo['minimumProxyGapMm'],'all363ActualPinNetIdentityUnchanged':True,'connectedPins':sum(not q['NC']for q in pinrows),'NCpins':sum(q['NC']for q in pinrows),'netCount':len({q['actualNet']for q in pinrows if q['actualNet']}),'edgeReserveIntrusions':intrusions,'allADC16BankCapsPresent':True,'ADCbankBeforeTIAAndAllLowerPriority':True,'bankTierProximityOrder':bankgates,'fourChannelRepeat':repeat,'ROWDriveSenseConnectivity':row,'inputSHAIntegrity':integrity,'nativeDRCClaimed':False,'nativeCADReleased':False,'P2ReasonNotExecuted':'P1 full101/5050/16caps and keyproxy improvement closes offline objective; no mandatory second candidate','J2ExactActuatorHOLD':True,'J134FinalMechanicalHOLD':True}
assert a['connectedPins']==323 and a['NCpins']==40 and a['netCount']==54
(P/'FULL_OFFLINE_AUDIT.json').write_text(json.dumps(a,indent=2),encoding='utf-8')
g={'C_SCHEMATIC_ACCEPTED_WITH_ADDENDUM':True,'OFFLINE_FULL101_REVIEW_READY':True,'ALL101_PLACED':True,'ALL5050_PROXY_GEOMETRY_PASS':True,'ALL363_IDENTITY_PASS':True,'ADC16_BANK_PRIORITY_PASS':True,'USER_VISUAL_ACCEPTANCE':'PENDING','CAD_RELEASED':False,'PCB_ROUTING_RELEASED':False,'BENCH_RELEASED':False,'MANUFACTURE_RELEASED':False,'ERC_DETAIL_HOLD':True,'LEGACY_ANNOTATION_HOLD':True,'FFC_MECHANICAL_HOLD':True,'MLCC_CEFF_HOLD':True,'FULL_MATRIX_DYNAMIC_PERFORMANCE_HOLD':True,'DRAWING_STANDALONE_RELEASE':False}
(P/'GATES.json').write_text(json.dumps(g,indent=2),encoding='utf-8')
print(json.dumps({'all101':True,'all363':True,'all5050':True,'bank16':True,'meanTIA_ADCstub':newmean,'maxTIA_ADCstub':newmax,'repeat':repeat,'P2NotExecuted':True}))
