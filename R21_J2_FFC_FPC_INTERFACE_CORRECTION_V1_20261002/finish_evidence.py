from pathlib import Path
import json,csv,hashlib,datetime,math
from collections import Counter
P=Path(__file__).parent
read=lambda n:json.loads((P/n).read_text('utf8'))
def rows(s):
 out=[]
 for line in s.splitlines():
  if '||' not in line:continue
  h,b=line.split('||',1);out.append((json.loads(h),json.loads(b.rstrip('|'))))
 return out
base=read('BASELINE_PCB.json');w=read('FINAL_WARM_PCB.json');s=read('FINAL_WARM_SCHEMATIC.json')
fp=json.loads((P/'FFC_FP_FINALIZE.stdout').read_text('utf8'))['value']['source'];(P/'J2_FINAL_WARM_FOOTPRINT_SOURCE.txt').write_text(fp,'utf8')
rb=rows(base['source']);rw=rows(w['source']);rf=rows(fp);j=next(c for c in w['parts']if c['ref']=='J2')
bm={h.get('id'):b for h,b in rb if h['type']=='LINE'};wm={h.get('id'):b for h,b in rw if h['type']=='LINE'}
plan=read('J2_LOCAL_FANOUT_PLAN.json');allowed={x['id'] for x in plan['changed']};deleted=set(plan['deleted'])
remaining=[i for i in bm if i not in allowed|deleted]
assert all(bm[i]==wm[i] for i in remaining)
assert set(bm)-set(wm)==deleted
assert {i for i in bm.keys()&wm.keys() if bm[i]!=wm[i]}==allowed
outside=[]
for ch in plan['changed']:
 old=bm[ch['id']];new=wm[ch['id']];end=ch['end'];keep='start' if end=='end' else 'end'
 assert all(old[k]==new[k] for k in ['netName','layerId','width'] if k in old)
 assert all(old[keep+k]==new[keep+k] for k in ['X','Y'])
 # The original segment is linear; the replacement endpoint lies on it at x=450mil.
 t=(new[end+'X']-old['startX'])/(old['endX']-old['startX'])
 assert abs(new[end+'Y']-(old['startY']+t*(old['endY']-old['startY'])))<0.11
 outside.append({'id':ch['id'],'net':ch['net'],'boundaryXmil':450,'outsideSegmentPreserved':'same retained endpoint/layer/net/width; cut point rounded, not strict geometric byte identity','cutPointYResidualMil':abs(new[end+'Y']-(old['startY']+t*(old['endY']-old['startY'])))})
other=[p for p in base['parts'] if p['ref']!='J2'];assert len(other)==175
assert all(p==next(q for q in w['parts'] if p['id']==q['id']) for p in other)
assert base['rules']==w['rules'] and base['layerInfo']==w['layerInfo']
for typ in ['VIA','POUR','POLY','LAYER','LAYER_PHYS','RULE','RULE_TEMPLATE','RULE_SELECTOR']:
 old={h.get('id',json.dumps(h,sort_keys=True)):b for h,b in rb if h['type']==typ}
 new={h.get('id',json.dumps(h,sort_keys=True)):b for h,b in rw if h['type']==typ}
 assert all(k in new and new[k]==v for k,v in old.items()),typ
pads=[(p['ref'],a) for p in w['parts'] for a in p['pads']]
assigned=[(r,a) for r,a in pads if a['net']];nc=[(r,a['number']) for r,a in pads if not a['net'] and r!='J2']
assert len(pads)==552 and len(assigned)==514 and len(nc)==36
assert [a['net'] for a in j['pads'][:8]]==['ROW0','ROW1','ROW2','ROW3','COL0','COL1','COL2','COL3']
assert len(j['pads'])==10 and all(a['hole'] is None and a['layer']==1 for a in j['pads'])
assert all(a['net']=='' for a in j['pads'][8:])
strings=[b for h,b in rf if h['type']=='STRING'];assert {b['text'] for b in strings}=={'J2','1','ROW','COL','FFC INSERT'}
legacy3d=any(h['type']=='D3_ATTRIBUTE' for h,b in rf)
def csvwrite(n,field,data):
 with (P/n).open('w',newline='',encoding='utf-8-sig')as f:
  z=csv.DictWriter(f,field);z.writeheader();z.writerows(data)
csvwrite('J2_ACTUAL_SIGNAL_AND_MECHANICAL_PADS.csv',['number','role','net','x_mm','y_mm','layer','hole','nativePad','source'],[{'number':a['number'],'role':'mechanical unassigned' if a['number'].startswith('MP')else'signal','net':a['net'],'x_mm':a['x']*.0254,'y_mm':a['y']*.0254,'layer':a['layer'],'hole':'none','nativePad':json.dumps(a['pad']),'source':'final warm SDK; coordinates rounded by getter; cold unavailable'} for a in j['pads']])
csvwrite('ACTUAL_552_PAD_NET.csv',['ref','number','net','x_mil','y_mil','layer'],[{'ref':r,'number':a['number'],'net':a['net'],'x_mil':a['x'],'y_mil':a['y'],'layer':a['layer']}for r,a in pads])
csvwrite('J2_NATIVE_SILK.csv',['text','local_x_mm','local_y_mm','font_mm','angle','source'],[{'text':b['text'],'local_x_mm':b['x']*.0254,'local_y_mm':b['y']*.0254,'font_mm':b['fontSize']*.0254,'angle':b['angle'],'source':'actual final warm footprint source'}for b in strings])
csvwrite('LOCAL_BOUNDARY_MAIN_SEGMENT_CHECK.csv',['id','net','boundaryXmil','outsideSegmentPreserved','cutPointYResidualMil'],outside)
old=P.parent/'R21_EXTERNAL_ARRAY_PLUGGABLE_INTERFACE_AND_FAB_INPUT_CONTRACT_V1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
input=read('INPUT_COPY_HASH.json');assert sha(Path(input['source']))==input['SHA256']
assert sha(old/'SCIENCE_ADK5556_4X4_R21_J2_PLUGGABLE_REVIEW.epro2')==input['oldEpro2SHA256']
counts=dict(Counter(h['type']for h,b in rw));a={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'parts':176,'pads':552,'assigned':514,'nets':len(set(a['net']for r,a in assigned)),'ordinaryNC':36,'mechanicalUnassigned':2,'other175Exact':True,'nonJ2SchematicExact':read('WARM_CORE_CHECK.json')['schematicNonJ2Differences']==[],'unchangedMainLINERecords':len(remaining),'changedJ2TerminalLeadInRecords':len(allowed),'outsideX450GeometryPreserved':True,'deletedJ2LocalLeadIn':len(deleted),'addedJ2LocalLINE':len(set(wm)-set(bm)),'unchangedOldVIA':297,'newLocalVIA':8,'fourPOURBoundariesExact':True,'derivedPOUREDFourChangedNormally':True,'rulesAndLayersExact':True,'warmDRC0':True,'firstWarmDRCNetlistError1':'sole J2 FFC Cable property identified by GUI import preview; applied only that attribute; second warm []','coldDRC':'UNKNOWN two EXECUTION_ERROR canvas subscription, conservatively predebited','coldCapture':'FAILED getAll; no full cold certificate','actualEpro2FileExport':'NOT_REACHED no file generated; predebit retained','saveAll':'GUI action observed; persistence cold not qualified','coldIndependent':'NOT_QUALIFIED warm GUI window remained during cold session startup; actual two-window overlap discovered and both closed','footprintLibraryGetterName':'old KK name persists, do not claim catalog identity update; final warm footprint source carries new intended identity','nativeCounts':counts,'old2SourceSHAUnchanged':True,'savedLocalProjectSHA256':sha(P/'SCIENCE_ADK5556_4X4_R21_J2_FFC_WORK.eprj2'),'rawProjectPublic':'EXCLUDED native SQLite has nonempty users.password and local account fields; never printed/copied credential value','fullPCBReady':False}
assert a['nets']==107
a['contactSideNativeStringPresent']=False
a['outsideX450GeometryPreserved']='retained endpoint/layer/net/width; boundary cut native 0.1mil rounding, not strict geometric identity'
a['maxCutPointYResidualMil']=max(x['cutPointYResidualMil']for x in outside)
a['legacyFootprintD3AttributeStillPresent']=legacy3d
a['sourceSetterReturnedTrueButSourceNotFullyApplied']='Footprint ATTR old KK name and D3 remain; CONTACT PCB absent. No getter or API qualification claimed; no further editing after hard quotas.'
(P/'FINAL_EVIDENCE_AUDIT.json').write_text(json.dumps(a,indent=2),'utf8')
(P/'FINAL_WARM_PCB_SOURCE.txt').write_text(w['source'],'utf8')
g={'J2_USER_TYPE_MATCH_WARM':True,'WARM_J2_8_SIGNAL_PLUS_2_MECH':True,'WARM_NON_J2_FROZEN':True,'WARM_DRC_FOUR_ZERO':True,'COLD_REOPEN':False,'COLD_DRC':False,'ACTUAL_NATIVE_FILE_EXPORT':False,'INDEPENDENT_NATIVE_PIN1_AND_SILK_RELEASE':False,'CONTACT_SIDE_NATIVE_SILK':'HOLD final footprint source has only five strings; CONTACT PCB missing though initial working source had six','PCB_REVIEW_READY':False,'MANUFACTURE_RELEASE':False,'PROCUREMENT_RELEASE':False,'BENCH_RELEASE':False,'STOP':read('EXECUTION_BUDGET.json')['status'],'historicalMIMOandDescriptorNotReopened':True,'otherPerformanceAndFabricationHoldsRetained':True}
(P/'GATES.json').write_text(json.dumps(g,indent=2),'utf8')
print(json.dumps(a))
