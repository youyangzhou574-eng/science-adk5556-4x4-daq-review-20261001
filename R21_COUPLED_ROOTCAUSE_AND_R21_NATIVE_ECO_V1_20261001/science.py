"""Bounded scientific case runner. No changes to frozen inputs or macro models."""
from pathlib import Path
import json,sys,time,subprocess,hashlib,datetime,os,shutil
ROOT=Path(__file__).resolve().parent
OLD=ROOT.parent/'R2_VERIFICATION_AND_MINIMAL_ECO_V1'
EXE=OLD/'runtime/Spice64/bin/ngspice_con.exe'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def dump(p,o):p.write_text(json.dumps(o,indent=2,ensure_ascii=True)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def init():
    for d in ['models','cases','results','sources','evidence','plots']: (ROOT/d).mkdir(exist_ok=True)
    expected={'OPA4388_ORIGINAL.LIB':'958ff133418bd47522015057497858263e73b9e6d75860ef9c0b6fdabed5cd0d','OPAx388.LIB':'bb9c6c7ac80dc7ff1ac5b698c05c53f0a8d55babb1ab210150d9bd910a6bf8e4'}
    rows=[]
    for n,h in expected.items():
        src=OLD/'models'/n
        assert sha(src)==h,(n,sha(src))
        shutil.copyfile(src,ROOT/'models'/n);rows.append({'file':n,'sha256':h,'unchanged':True})
    assert sha(EXE)=='22d5cae2bd32b2e39157a8d27bf457122f68285b72a9ebefdf41551b628233ab'
    dump(ROOT/'INPUT_VERIFIED.json',{'UTC':utc(),'models':rows,'executor':str(EXE),'executor_SHA256':sha(EXE),'switches':['-n','-D','ngbehavior=psa'],'frozen_commits':['da6ca87b9f49c5af03a16c24af6186d7c5c2e0d3','c13555a330f8ad676750b8fec5d5d42bfc0b5edb']})
    if not (ROOT/'EXECUTION_BUDGET.json').exists():
        dump(ROOT/'EXECUTION_BUDGET.json',{'startedUTC':'2026-10-01T11:10:00+00:00','totalMaxMinutes':240,'phase':'P0','phaseStartedUTC':'2026-10-01T11:10:00+00:00','limits':{'P0':{'minutes':45,'AC_DC_PZ':32,'diagnostics':8},'P1':{'minutes':85,'transient':32,'static_AC':24,'PZ':12,'full_long':1},'P2':{'minutes':35,'reset_corners':64,'protocol_tests':32,'sources':6,'library':2},'P3':{'minutes':60,'copy':1,'session':2,'save':5,'capture_audit':3,'ERC':2,'PDF':2},'P4':{'minutes':15,'delivery':1}},'used':{},'cases':[],'nativeGate':'NOT_ENTERED'})
def register(name,phase,kind):
    p=ROOT/'EXECUTION_BUDGET.json';b=json.loads(p.read_text())
    assert not b.get('scienceStopped',False),'SCIENCE_STOP_PENDING_NEW_RULING'
    elapsed=(datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(b['startedUTC'])).total_seconds()/60
    assert elapsed<240,'TOTAL_STOP'
    assert b['phase']==phase,'Phase transition must be explicit'
    spent=(datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(b['phaseStartedUTC'])).total_seconds()/60
    spent+=sum((datetime.datetime.fromisoformat(h['to'])-datetime.datetime.fromisoformat(h['from'])).total_seconds()/60 for h in b.get('phaseHistory',[])if h['phase']==phase)
    assert spent<b['limits'][phase]['minutes'],'PHASE_TIME_STOP'
    # Diagnostic attributes never exempt the actual analysis from its quota.
    import re
    net=(ROOT/'cases'/(name+'.cir')).read_text(errors='replace')
    charges={kind}
    if phase=='P0' and re.search(r'(?im)^\s*\.?\s*(op|optran|ac|pz)\b',net):charges.add('AC_DC_PZ')
    if phase=='P1' and re.search(r'(?im)^\s*\.?\s*tran\b',net):charges.add('transient')
    for category in charges:
        assert b['used'].get(phase+'/'+category,0)+1<=b['limits'][phase][category],'COUNT_STOP:'+phase+'/'+category
    assert name not in [r['name'] for r in b['cases']],'Never duplicate a case name'
    for category in charges:b['used'][phase+'/'+category]=b['used'].get(phase+'/'+category,0)+1
    b['cases'].append({'name':name,'phase':phase,'kind':kind,'charges':sorted(charges),'startedUTC':utc()});dump(p,b)
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
