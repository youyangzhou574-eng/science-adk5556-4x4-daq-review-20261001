import json,pathlib,subprocess,datetime,time,os,sys
from budget_guard import precharge
P=pathlib.Path(__file__).resolve().parent
name=sys.argv[1];kind=sys.argv[2]
folder=(P/'cases'/name).resolve()
if not folder.is_relative_to(P/'cases'):raise SystemExit('case outside package')
costs={'OP_AC_PZ':1}
if kind=='TRAN':costs['TRAN']=1
bfile=P/'EXECUTION_BUDGET.json'
now=datetime.datetime.now(datetime.timezone.utc)
b=json.loads(bfile.read_text('utf-8-sig'))
if (now-datetime.datetime.fromisoformat(b['phaseStartedUTC'])).total_seconds()>=110*60:raise SystemExit('C2 phase budget')
b=precharge(b,costs,now)
b['operations'].append({'case':name,'costs':costs,'preDebitedUTC':now.isoformat()})
tmp=bfile.with_suffix('.tmp');tmp.write_text(json.dumps(b,indent=2),'utf8');os.replace(tmp,bfile)
exe=P.parent/'R2_VERIFICATION_AND_MINIMAL_ECO_V1/runtime/Spice64/bin/ngspice_con.exe'
started=time.monotonic();limit=180 if kind=='TRAN' else 60
with (folder/'stdout.log').open('wb') as out,(folder/'stderr.log').open('wb') as err:
    process=subprocess.Popen([str(exe),'-n','-D','ngbehavior=psa','-b','case.cir'],cwd=folder,stdout=out,stderr=err)
    result={'case':name,'PID':process.pid,'startedUTC':now.isoformat(),'exe':str(exe),'command':[str(exe),'-n','-D','ngbehavior=psa','-b','case.cir'],'costs':costs,'limitSeconds':limit}
    try:process.wait(timeout=limit);result['forcedStop']=False
    except subprocess.TimeoutExpired:
        process.terminate();process.wait(timeout=10);result['forcedStop']='OWN_PROCESS_WALL_LIMIT'
    result.update(returncode=process.returncode,wallSeconds=time.monotonic()-started)
(folder/'RUN.json').write_text(json.dumps(result,indent=2),'utf8')
print(json.dumps(result))
