from pathlib import Path
import json,sys,datetime
P=Path(__file__).parent;f=P/'EXECUTION_BUDGET.json';b=json.loads(f.read_text('utf8'));kind=sys.argv[1];n=int(sys.argv[2]);reason=' '.join(sys.argv[3:])
assert b['status']=='ACTIVE'or(b.get('evidenceOnlyAfterStop')and kind in('captureaudit','reviewExport')),'STOP remains sticky; no further mutations'
assert datetime.datetime.now(datetime.timezone.utc)<datetime.datetime.fromisoformat(b['startUTC'])+datetime.timedelta(minutes=b['approvedMinutes']),'Package time exhausted'
assert n>0 and b['actual'][kind]+n<=b['limits'][kind],kind
b['actual'][kind]+=n;b['reservations'].append({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'kind':kind,'count':n,'reason':reason});f.write_text(json.dumps(b,indent=2),'utf8');print(json.dumps({'reserved':kind,'actual':b['actual'][kind],'limit':b['limits'][kind],'reason':reason}))
