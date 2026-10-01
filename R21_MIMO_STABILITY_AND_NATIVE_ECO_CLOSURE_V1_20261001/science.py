"""Bounded scientific case runner. No changes to frozen inputs or macro models."""
from pathlib import Path
import json,sys,time,subprocess,hashlib,datetime,os,shutil
ROOT=Path(__file__).resolve().parent
OLD=ROOT.parent/'R21_COUPLED_ROOTCAUSE_AND_R21_NATIVE_ECO_V1'
EXE=ROOT.parent/'R2_VERIFICATION_AND_MINIMAL_ECO_V1'/'runtime/Spice64/bin/ngspice_con.exe'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def dump(p,o):p.write_text(json.dumps(o,indent=2,ensure_ascii=True)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def init():
    raise RuntimeError('Legacy initializer disabled: no budget reset; package setup is immutable')

def analysis_commands(net):
    commands=[];inside=False
    for index,line in enumerate(net.splitlines()):
        line=line.strip().lower()
        if line=='.control':inside=True;continue
        if line=='.endc':inside=False;continue
        if line.startswith('*') or not line:continue
        word=line.split()[0]
        if inside and word in ['op','optran','ac','pz','tran']:commands.append(word)
        elif index>0 and not inside and word in ['.op','.ac','.pz','.tran']:commands.append(word[1:])
    return commands

def analysis_charges(commands,kind,net):
    charges={}
    count=sum(x in ['op','ac','pz'] for x in commands)
    if count:charges['DC_AC_PZ']=count
    count=commands.count('tran')
    if count:charges['transient']=count
    if kind in ['diagnostics','full_long'] or '.options method=gear' in net:charges['diagnostics']=1
    if kind=='full_long':charges['full_long']=1
    return charges

def require_technical_review(reason,source):
    p=ROOT/'EXECUTION_BUDGET.json';b=json.loads(p.read_text(encoding='utf-8'))
    if not b.get('scienceStopped'):
        b['scienceStopped']=True;b['scienceStoppedUTC']=utc();b['scienceStopReason']=reason
    b.setdefault('technicalReviewEvents',[]).append({'UTC':utc(),'reason':reason,'source':source})
    dump(p,b)

def register(name,phase,kind):
    p=ROOT/'EXECUTION_BUDGET.json';b=json.loads(p.read_text())
    assert not b.get('scienceStopped',False),'SCIENCE_STOP_PENDING_NEW_RULING'
    elapsed=(datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(b['startedUTC'])).total_seconds()/60
    assert elapsed<b['totalMaxMinutes'],'TOTAL_STOP'
    assert b['phase']==phase,'Phase transition must be explicit'
    spent=(datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(b['phaseStartedUTC'])).total_seconds()/60
    spent+=sum((datetime.datetime.fromisoformat(h['to'])-datetime.datetime.fromisoformat(h['from'])).total_seconds()/60 for h in b.get('phaseHistory',[])if h['phase']==phase)
    assert spent<b['limits'][phase]['minutes'],'PHASE_TIME_STOP'
    # Diagnostic attributes never exempt the actual analysis from its quota.
    import re
    net=(ROOT/'cases'/(name+'.cir')).read_text(errors='replace')
    commands=analysis_commands(net)
    charges=analysis_charges(commands,kind,net)
    assert any(x in charges for x in ['DC_AC_PZ','transient']),'NO_ANALYSIS_DECLARED'
    for category,count in charges.items():
        assert b['used'].get(category,0)+count<=b['globalLimits'][category],'COUNT_STOP:'+category
    assert name not in [r['name'] for r in b['cases']],'Never duplicate a case name'
    for category,count in charges.items():b['used'][category]=b['used'].get(category,0)+count
    b['cases'].append({'name':name,'phase':phase,'kind':kind,'charges':sorted(charges),'startedUTC':utc(),'commands':commands,'chargeCounts':charges});dump(p,b)
def phase(name):
    p=ROOT/'EXECUTION_BUDGET.json';b=json.loads(p.read_text());now=utc()
    b.setdefault('phaseHistory',[]).append({'phase':b['phase'],'from':b['phaseStartedUTC'],'to':now})
    b['phase']=name;b['phaseStartedUTC']=now;dump(p,b)
def start(name,phase_name,kind,limit=180):
    assert limit<=180 or (kind=='full_long' and limit<=480)
    register(name,phase_name,kind)
    dest=ROOT/'results'/name;dest.mkdir(exist_ok=False)
    args=[sys.executable,'-B',str(Path(__file__).resolve()),'supervise',name,str(limit)]
    with (dest/'supervisor.log').open('wb') as f:
        p=subprocess.Popen(args,stdout=f,stderr=subprocess.STDOUT,cwd=ROOT,creationflags=subprocess.CREATE_NO_WINDOW)
    dump(dest/'DISPATCH.json',{'supervisorPID':p.pid,'startedUTC':utc(),'limitSeconds':limit,'netlistSHA256':sha(ROOT/'cases'/(name+'.cir'))})
    print(json.dumps({'case':name,'supervisorPID':p.pid,'limitSeconds':limit}))
def supervise(name,limit):
    dest=ROOT/'results'/name;t=time.monotonic();status={'case':name,'startedUTC':utc(),'limitSeconds':limit,'status':'RUNNING'}
    with (dest/'stdout.log').open('wb') as out,(dest/'stderr.log').open('wb') as err:
        p=subprocess.Popen([str(EXE),'-n','-D','ngbehavior=psa','-b',str(ROOT/'cases'/(name+'.cir'))],cwd=dest,stdout=out,stderr=err,creationflags=subprocess.CREATE_NO_WINDOW)
        status['ownedPID']=p.pid;dump(dest/'STATUS.json',status)
        import re
        last_progress=None;changed_at=time.monotonic()
        while p.poll() is None:
            time.sleep(.5);now=time.monotonic()
            progress=re.findall(rb'Reference value\s*:\s*([0-9.eE+-]+)',(dest/'stdout.log').read_bytes())
            if progress:
                value=float(progress[-1]);status['lastProgressTime_s']=value
                if last_progress is None or value>last_progress+1e-9:last_progress=value;changed_at=now
            reason='Owned child reached bounded case wall limit' if now-t>=limit else 'Simulation time stopped advancing for 15s' if progress and now-changed_at>=15 else None
            if reason:
                p.kill();p.wait();status['status']='FORCED_STOP_NOT_NORMAL_EXIT';status['reason']=reason;break
        if status['status']=='RUNNING':status['status']='NORMAL_EXIT' if p.returncode==0 else 'EXECUTOR_ERROR'
        status['exitCode']=p.returncode
    errors=(dest/'stderr.log').read_text(errors='replace')
    status['analysisStatus']='ANALYSIS_ERROR' if re.search(r'(?im)^Error:|simulation\(s\) aborted|doAnalyses:',errors) else 'PROCESS_EXIT_ONLY_REQUIRES_DATA_VALIDATION'
    status['wallSeconds']=time.monotonic()-t;status['endedUTC']=utc();dump(dest/'STATUS.json',status)
    print(json.dumps(status))
if __name__=='__main__':
    if sys.argv[1]=='init':init()
    elif sys.argv[1]=='start':start(sys.argv[2],sys.argv[3],sys.argv[4],float(sys.argv[5]) if len(sys.argv)>5 else 180)
    elif sys.argv[1]=='supervise':supervise(sys.argv[2],float(sys.argv[3]))
    elif sys.argv[1]=='phase':phase(sys.argv[2])
    elif sys.argv[1]=='status':
        for p in sorted((ROOT/'results').glob('*/STATUS.json')):print(p.read_text())
