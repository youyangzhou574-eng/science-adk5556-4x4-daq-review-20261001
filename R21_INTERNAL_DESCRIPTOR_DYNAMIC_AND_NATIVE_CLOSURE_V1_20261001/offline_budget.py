from pathlib import Path
import json,datetime
ROOT=Path(__file__).resolve().parent
def debit(name,count=1,note=''):
 p=ROOT/'EXECUTION_BUDGET.json';b=json.loads(p.read_text());n=datetime.datetime.now(datetime.timezone.utc)
 assert not b['scienceStopped'],'STICKY_SCIENTIFIC_STOP';assert (n-datetime.datetime.fromisoformat(b['startedUTC'])).total_seconds()/60<b['totalMaxMinutes'];assert (n-datetime.datetime.fromisoformat(b['phaseStartedUTC'])).total_seconds()/60<b['limits'][b['phase']]['minutes']
 rows=b.setdefault('offlineDiagnostics',[]);assert name not in [x['name']for x in rows];assert b['used'].get('diagnostics',0)+count<=b['globalLimits']['diagnostics']
 b['used']['diagnostics']=b['used'].get('diagnostics',0)+count;rows.append({'name':name,'preDebitedUTC':n.isoformat(),'count':count,'phase':b['phase'],'note':note,'actualSPICE':0});p.write_text(json.dumps(b,indent=2),encoding='utf-8')
