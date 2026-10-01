import time,json
from science import ROOT
from physical_cut import dispatch
t=time.monotonic()
while time.monotonic()-t<48:
 b=json.loads((ROOT/'EXECUTION_BUDGET.json').read_text());states=[]
 for c in b['cases']:
  p=ROOT/'results'/c['name']/'STATUS.json'
  states.append(json.loads(p.read_text()) if p.exists() else {'status':'RUNNING'})
 audited={'tian_blank_p6','tian_blank_p16','tian_blank_warm_p6','tian_blank_warm_p16'}
 failures=[s for s in states if s.get('case')not in audited and (s['status']not in ['RUNNING','NORMAL_EXIT']or s.get('analysisStatus')=='ANALYSIS_ERROR')]
 if failures:print(json.dumps({'auditNeeded':failures}));break
 if any(s['status']=='RUNNING'for s in states):time.sleep(.5);continue
 if len(b['cases'])==50:print('All50 actual measurements terminal, four audited failed TIA cases remain HOLD');break
 dispatch(2)
print(json.dumps({'wallSeconds':time.monotonic()-t,'registeredCases':len(json.loads((ROOT/'EXECUTION_BUDGET.json').read_text())['cases'])}))
