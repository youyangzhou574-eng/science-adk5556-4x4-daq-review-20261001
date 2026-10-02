from pathlib import Path
import sys,json,datetime,subprocess
p=Path(__file__).parent
label=sys.argv[1];costs=json.loads(sys.argv[2]);args=sys.argv[3:]
b=json.loads((p/'EXECUTION_BUDGET.json').read_text(encoding='utf-8'))
now=datetime.datetime.now(datetime.timezone.utc)
assert not b['STOP'] and now<datetime.datetime.fromisoformat(b['deadlineUTC'])
for k,v in costs.items(): assert isinstance(v,int) and v>=0 and b['spent'][k]+v<=b['limits'][k],k
for k,v in costs.items():b['spent'][k]+=v
b['events'].append({'utc':now.isoformat(),'label':label,'cost':costs,'prechargedBeforeLaunch':True})
(p/'EXECUTION_BUDGET.json').write_text(json.dumps(b,indent=2),encoding='utf-8')
r=subprocess.run([sys.executable,str(p/'cli_call.py'),label]+args,cwd=p,timeout=60)
sys.exit(r.returncode)
