import datetime,json,pathlib,os
ROOT=pathlib.Path(__file__).resolve().parent
def utc():return datetime.datetime.now(datetime.timezone.utc)
def charge(kind,label,n=1):
 p=ROOT/'EXECUTION_BUDGET.json'; q=json.loads(p.read_text('utf8')); now=utc()
 if q['scienceStopped']:raise RuntimeError('sticky engineering STOP')
 if (now-datetime.datetime.fromisoformat(q['startedUTC'])).total_seconds()>q['totalMaxMinutes']*60:raise RuntimeError('total time budget')
 if (now-datetime.datetime.fromisoformat(q['phaseStartedUTC'])).total_seconds()>q['limits'][q['phase']]['minutes']*60:raise RuntimeError('phase time budget')
 used=q['used'].get(kind,0)
 if used+n>q['globalLimits'][kind]:raise RuntimeError('count budget '+kind)
 q['used'][kind]=used+n;q['operations'].append({'kind':kind,'label':label,'count':n,'preDebitedUTC':now.isoformat()})
 tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n','utf8');os.replace(tmp,p)
def phase(name):
 p=ROOT/'EXECUTION_BUDGET.json';q=json.loads(p.read_text('utf8'));now=utc();q['phaseHistory'].append({'phase':q['phase'],'startedUTC':q['phaseStartedUTC'],'endedUTC':now.isoformat()});q['phase']=name;q['phaseStartedUTC']=now.isoformat();p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n','utf8')
