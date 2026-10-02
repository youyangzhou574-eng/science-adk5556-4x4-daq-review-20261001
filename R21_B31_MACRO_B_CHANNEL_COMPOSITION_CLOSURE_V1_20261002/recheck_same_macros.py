from b31_core import *
for n in ['MACRO_B1_AUDIT.json','MACRO_B2_AUDIT.json','MACRO_SELECTION.json']:
 f=P/n;f.rename(P/(n.replace('.json','_BEFORE_NET_ENDPOINT_FIX.json')))
aa=[]
for label in ['B1','B2']:
 prev=json.loads((P/('MACRO_'+label+'_AUDIT_BEFORE_NET_ENDPOINT_FIX.json')).read_text());a=macro_audit(prev['positions']);a['label']=label;save('MACRO_'+label+'_AUDIT.json',a);aa.append(a)
choice=min([a for a in aa if not a['physicalCollisions']],key=lambda x:x['score']);save('MACRO_SELECTION.json',{'selected':choice['label'],'positions':choice['positions'],'selectedOnceAfterVerifiedActualNetEndpoints':True,'hardMacroProxyCollisionGate':True,'candidateCoordinatesChangedDuringReadOnlyAuditCorrection':False,'allCandidateScores':[{k:a[k] for k in ['label','score','physicalCollisions','bbox','largestSampledEmptyRectangle','signalLengthSumMm']} for a in aa]});print(json.dumps({'selected':choice['label'],'scores':[a['score'] for a in aa]}))
with (P/'PLAN_AND_LEDGER.md').open('a',encoding='utf8') as f:f.write('\nMacro audit endpoint correction: U4 CMD3 pad18 replaces NC15; U11 sense1-to-V5 classified functional divider, not false direct pin4 same-net. Both original candidate coordinates frozen; initial score/selection evidence retained BEFORE_NET_ENDPOINT_FIX. Same two candidates only re-audited, no extra macro/coords. Empty rectangle explicitly excludes boundary cells; still 1mm sampled proxy. Final selection B2 under corrected actual endpoints.\n')
