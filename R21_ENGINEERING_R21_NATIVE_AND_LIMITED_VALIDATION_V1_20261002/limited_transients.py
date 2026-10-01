import pathlib,re,subprocess,time,json,hashlib,shutil,os
from budget import ROOT,charge
BASE=ROOT.parent/'R21_COUPLED_ROOTCAUSE_AND_R21_NATIVE_ECO_V1'
EXE=ROOT.parent/'R2_VERIFICATION_AND_MINIMAL_ECO_V1/runtime/Spice64/bin/ngspice_con.exe'
def prepare():
 (ROOT/'models').mkdir(exist_ok=True);manifest=[]
 for name in ['OPA4388_ORIGINAL.LIB','OPAx388.LIB']:
  src=BASE/'models'/name
  if not src.exists():src=ROOT.parent/'R2_VERIFICATION_AND_MINIMAL_ECO_V1/models'/name
  shutil.copyfile(src,ROOT/'models'/name);manifest.append({'name':name,'source':str(src),'SHA256':hashlib.sha256(src.read_bytes()).hexdigest()})
 (ROOT/'MODEL_SOURCE_SHA.json').write_text(json.dumps(manifest,indent=2)+'\n','utf8')
 names=[]
 for part in ['4row_1tia','1row_4tia']:
  for mode in ['800','8000','high_target']:
   name=f'part_{part}_{mode}';folder=ROOT/'cases'/name;folder.mkdir(parents=True,exist_ok=True)
   src=BASE/'cases'/f'{name}_gear_180.cir';code=src.read_text('utf8')
   code=code.replace('100u 10n 10n 1m 10m','3u 10n 10n 1m 10m')
   code=re.sub(r'^optran.*\n','',code,flags=re.M)
   code=code.replace('tran 200n 600u 0 100n','tran 100n 353u 0 100n')
   (folder/'case.cir').write_text(code,'utf8');(folder/'SOURCE.json').write_text(json.dumps({'source':str(src),'sourceSHA':hashlib.sha256(src.read_bytes()).hexdigest(),'changes':['switch100us to3us','remove optran initialization','end353us,step100ns'],'no_model_edits':True},indent=2),'utf8');names.append(name)
 return names
def run(name):
 import numpy as np
 folder=ROOT/'cases'/name;charge('OP_AC',name+' OP');charge('transient',name+' short TRAN')
 start=time.time();last=None;progress=time.time();why=None
 with (folder/'stdout.log').open('wb') as out,(folder/'stderr.log').open('wb') as err:
  p=subprocess.Popen([str(EXE),'-n','-D','ngbehavior=psa','-b','case.cir'],cwd=folder,stdout=out,stderr=err)
  while p.poll() is None:
   time.sleep(1);elapsed=time.time()-start
   txt=(folder/'stderr.log').read_bytes().decode('utf8','replace')[-8000:]
   nums=re.findall(r'Reference value\s*:\s*([0-9.eE+\-]+)',txt)
   if nums:
    v=float(nums[-1])
    if last is None or v>last+1e-12:last=v;progress=time.time()
    elif time.time()-progress>=30 and elapsed>=40:why='INTEGRATION_STAGNATION_30s'
   if elapsed>=180:why='WALL_LIMIT_180s'
   if why:p.terminate();p.wait(timeout=10);break
 result={'case':name,'PID':p.pid,'executable':str(EXE),'startedUnix':start,'wallSeconds':time.time()-start,'returncode':p.returncode,'forcedStop':why,'status':'MACROMODEL_NUMERICAL_LIMIT','optran':0,'lastIntegrationTime_s':last}
 op=folder/'op.txt';trace=folder/'trace.txt'
 if op.exists():result['opText']=op.read_text('utf8')
 if trace.exists() and not why:
  data=np.genfromtxt(trace,names=True)
  if data.size>1 and data.dtype.names and data['time'][-1]>=352.9e-6:
   status='COMPLETED_SCOPE_LIMITED';summ=[]
   for col in data.dtype.names:
    if not col.startswith(('v_tap','v_ain')):continue
    val=data[col];end=val[data['time']>=343e-6].mean();valid=val[data['time']>=303e-6];res=float(np.max(abs(valid-end)));summ.append({'node':col,'finalMean_V':float(end),'max303to353usResidual_V':res,'min_V':float(val.min()),'max_V':float(val.max()),'pass100uV':res<=100e-6})
   # Completed results are evaluated before any additional case is started.
   result.update(status=status,columns=list(data.dtype.names),samples=int(data.size),tEnd_s=float(data['time'][-1]),summaries=summ)
   normal='high_target' in name
   if normal and any(x['min_V']<0 or x['max_V']>5.12 or not x['pass100uV'] for x in summ):result['status']='COMPLETED_NORMAL_ENGINEERING_STOP'
 (folder/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n','utf8');print(json.dumps({k:v for k,v in result.items() if k!='opText'}),flush=True)
 return result
if __name__=='__main__':
 names=prepare();results=[]
 for name in names:
  q=run(name);results.append(q)
  if q['status']=='COMPLETED_NORMAL_ENGINEERING_STOP':
   f=ROOT/'EXECUTION_BUDGET.json';b=json.loads(f.read_text('utf8'));b['scienceStopped']=True;b['stopReason']=q['status']+' '+name;f.write_text(json.dumps(b,indent=2),'utf8');break
 (ROOT/'TRANSIENT_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n','utf8')
