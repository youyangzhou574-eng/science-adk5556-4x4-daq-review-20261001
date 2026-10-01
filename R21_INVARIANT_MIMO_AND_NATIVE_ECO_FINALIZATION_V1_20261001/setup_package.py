from pathlib import Path
import json,hashlib,shutil,datetime
R=Path(__file__).resolve().parent;old=R.parent/'R21_MIMO_STABILITY_AND_NATIVE_ECO_CLOSURE_V1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
assert not (R/'EXECUTION_BUDGET.json').exists(),'Never reset initialized budget'
for d in ['cases','results','evidence','models','plots','sources']:(R/d).mkdir(exist_ok=True)
inputs=json.loads((old/'INPUT_VERIFIED.json').read_text())
for n,h in inputs['models'].items():
 assert sha(old/'models'/n)==h.upper();shutil.copyfile(old/'models'/n,R/'models'/n)
assert sha(Path(inputs['executor']))==inputs['executorSHA256'].upper()
shutil.copyfile(old/'science.py',R/'science.py')
start='2026-10-01T14:32:44.519000+00:00';now=datetime.datetime.now(datetime.timezone.utc).isoformat()
b={'package':'SCIENCE_ADK5556_4X4_R21_INVARIANT_MIMO_AND_NATIVE_ECO_FINALIZATION_V1','ruling':'06','startedUTC':start,'totalMaxMinutes':360,'phase':'P0','phaseStartedUTC':start,'limits':{n:{'minutes':m}for n,m in zip(['P0','P1','P2','P3','P4'],[90,110,50,80,30])},'globalLimits':{'DC_AC_PZ':160,'diagnostics':24,'transient':48,'full_long':1,'reset_corners':96,'protocol_tests':48,'sources':8,'reset_candidates':2,'library':4,'copy':1,'session':2,'save':8,'capture_audit':4,'ERC':2,'PDF':2},'used':{},'cases':[],'offlineDiagnostics':[],'nativeGate':'NOT_ENTERED','scienceStopped':False,'newSigmaRule':'ROBUSTNESS_DIAGNOSTIC_ONLY; no 0.20 threshold gate','phaseHistory':[]}
(R/'EXECUTION_BUDGET.json').write_text(json.dumps(b,indent=2),encoding='utf-8')
inputs['verifiedUTC']=now;inputs['frozenCommits'].append('d152e092101188e6dc57f620f81d52f2e243fb01');inputs['previous76AnalysesClosed']=True;(R/'INPUT_VERIFIED.json').write_text(json.dumps(inputs,indent=2),encoding='utf-8')
print(json.dumps({'initialized':True,'minutes':360,'analysis':160,'diagnostics':24,'modelsUnchanged':True,'executorUnchanged':True}))
