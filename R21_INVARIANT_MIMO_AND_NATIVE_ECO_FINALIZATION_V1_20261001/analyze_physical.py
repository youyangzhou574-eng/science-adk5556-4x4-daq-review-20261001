import json,numpy as np,csv
from scipy.linalg import solve
from scipy.optimize import linear_sum_assignment
from science import ROOT,dump
from network_cases import raw_nodes
from invariant_math import characteristic_matrix,pencil_metrics
P=json.loads((ROOT/'EXTENDED_MEASUREMENT_PLAN.json').read_text());base=raw_nodes(P['OPsource']);bias=[];dup=[]
physical=['v(vcm)','v(vexc)']+[f'v(drv{i})'for i in range(4)]+[f'v(tdrv{i})'for i in range(4)]
def data(name):
 path=ROOT/'results'/name;status=json.loads((path/'STATUS.json').read_text())
 if status['status']!='NORMAL_EXIT' or status['analysisStatus']=='ANALYSIS_ERROR' or not(path/'data.txt').exists():return None
 a=np.loadtxt(path/'data.txt',skiprows=1);assert np.isfinite(a).all();op=raw_nodes(path/'op.raw');bias.append({'case':name,'maxPhysicalBiasDifferenceV':max(abs(op[k]-base[k])for k in physical)});return a
def recovered(top):
 arrays=[]
 for j in range(20):
  m=P['mapping'][str(j)];a=data(f'{top}_blank_p'+str(m['representative']));assert a is not None
  out=a.copy();p=m['permutation'] if top=='open' else m['permutation'][:10];offsets=[1,41]if top=='open' else [1,21]
  for offset in offsets:
   for old,new in enumerate(p):out[:,offset+2*new:offset+2*new+2]=a[:,offset+2*old:offset+2*old+2]
  if top=='closed' and j in [3,7,13,17]:
   actual=data(f'{top}_blank_p{j}');z=out[:,1::2]+1j*out[:,2::2];w=actual[:,1::2]+1j*actual[:,2::2];norm=np.linalg.norm(w,axis=1);err=np.linalg.norm(z-w,axis=1);valid=norm>1e-12
   dup.append({'column':j,'maxComplexColumnNormRelativeError':float(np.max(err[valid]/norm[valid])),'absoluteErrorBelow1e_12Norm':float(np.max(err[~valid]))if np.any(~valid)else 0.,'PASS':bool(np.all(err<=.005*norm+1e-12))})
  if P.get('fullActualColumns'):out=data(f'{top}_blank_p{j}');assert out is not None
  arrays.append(out)
 f=arrays[0][:,0]
 if top=='open':
  cur=np.stack([a[:,1:41:2]+1j*a[:,2:41:2]for a in arrays],axis=2);vol=np.stack([a[:,41::2]+1j*a[:,42::2]for a in arrays],axis=2)
 else:
  ff=np.stack([a[:,1:21:2]+1j*a[:,2:21:2]for a in arrays],axis=2);ee=np.stack([a[:,21::2]+1j*a[:,22::2]for a in arrays],axis=2);B,A=ff[:,:,:10],ff[:,:,10:];D,C=ee[:,:,:10],ee[:,:,10:];eye=np.broadcast_to(np.eye(10),D.shape)
  cur=np.block([[B,eye+A],[-B,-A]]);vol=np.block([[D,C],[D-eye,C]])
 y=np.linalg.solve(vol.swapaxes(1,2),cur.swapaxes(1,2)).swapaxes(1,2)
 if top=='open':
  yl=1/(2j*np.pi*f*1e9)
  for k in range(10):y[:,k,k]-=yl;y[:,k+10,k+10]-=yl;y[:,k,k+10]+=yl;y[:,k+10,k]+=yl
 np.savez(ROOT/'results'/(top+'_NEW_Y.npz'),freq=f,Y=y,portCondition=np.linalg.cond(vol));return f,y
def crossover(f,L):
 mag=20*np.log10(abs(L));phase=np.unwrap(np.angle(L))*180/np.pi;cross=[]
 for j in range(len(f)-1):
  if mag[j]>=0 and mag[j+1]<0:
   frac=mag[j]/(mag[j]-mag[j+1]);cross.append({'Hz':float(np.exp(np.log(f[j])+frac*np.log(f[j+1]/f[j]))),'PMdegree':float(180+phase[j]+frac*(phase[j+1]-phase[j]))})
 return cross

f,y=recovered('open');fc,z=recovered('closed');assert np.allclose(f,fc);g=np.stack([characteristic_matrix(a)for a in y]);h=np.stack([characteristic_matrix(a)for a in z]);np.savez(ROOT/'results'/'NEW_GC.npz',freq=f,openGc=g,closedGc=h)
summary=[]
for hz in [.01,.1,1,10,300e6]:
 j=int(np.argmin(abs(f-hz)));row={'Hz':float(f[j]),'GcRelativeTopologyDifference':float(np.linalg.norm(g[j]-h[j])/np.linalg.norm(h[j])),'topologyResults':[]}
 for label,matrix in [('open',g[j]),('closed',h[j])]:
  original=None;errors=[];metrics=[]
  for scale in [np.ones(10),np.geomspace(.001,1000,10),np.geomspace(1000,.001,10)]:
   si=1/scale;v=pencil_metrics(si[:,None]*matrix*si[None,:],si[:,None]*np.diag(np.diag(matrix))*si[None,:]);mu=v.pop('mu');phase=v.pop('detRatioPhase');v['detPhase']=[phase.real,phase.imag];v['generalizedEigenvalues']=[[w.real,w.imag]for w in mu];v['fixedPowerScale']=scale.tolist()
   if original is None:original=mu
   cost=abs(original[:,None]-mu[None,:]);a,b=linear_sum_assignment(cost);errors.append(float(np.max(cost[a,b])/max(1,float(max(abs(original))))));metrics.append(v)
  row['topologyResults'].append({'topology':label,'fixedScaleGeneralizedEigenSetRelativeDifferences':errors,'metrics':metrics})
 summary.append(row)
dump(ROOT/'LOW_FREQUENCY_QZ_AND_SCALING.json',{'scope':'double precision measured matrices; no reference pole qualification, no stable/unstable conclusion','frequenciesRetained':len(f),'results':summary});dump(ROOT/'ACTUAL_REPEATED_COLUMNS_AFTER_FULL_FALLBACK.json',dup);dump(ROOT/'PHYSICAL_OP_BIAS.json',bias)
cross=[]
for target in [0,1,2,6]:
 directMethod='SERIES_VOLTAGE_AND_SHUNT_CURRENT';directCases=[f'tian_blank_p{target}',f'tian_blank_p{target+10}']
 a=data(f'tian_blank_p{target}');b=data(f'tian_blank_p{target+10}')
 if a is None or b is None:
  a=data(f'tian_blank_warm_p{target}')if(ROOT/'results'/f'tian_blank_warm_p{target}'/'STATUS.json').exists()else None;b=data(f'tian_blank_warm_p{target+10}')if(ROOT/'results'/f'tian_blank_warm_p{target+10}'/'STATUS.json').exists()else None
 if a is None or b is None:
  x=data('tian_TIA0_loaded_p0')if target==6 and(ROOT/'results/tian_TIA0_loaded_p0/STATUS.json').exists()else None
  w=data('tian_TIA0_loaded_p1')if target==6 and(ROOT/'results/tian_TIA0_loaded_p1/STATUS.json').exists()else None
  if x is None or w is None:cross.append({'target':target,'status':'DIRECT_FULL_NETWORK_TIAN_NUMERICAL_HOLD'});continue
  directMethod='LOADED_TWO_PORT_VOLTAGE_COLUMNS';directCases=['tian_TIA0_loaded_p0','tian_TIA0_loaded_p1']
  current=np.stack([v[:,1:5:2]+1j*v[:,2:5:2]for v in [x,w]],axis=2);voltage=np.stack([v[:,5::2]+1j*v[:,6::2]for v in [x,w]],axis=2);yt=np.linalg.solve(voltage.swapaxes(1,2),current.swapaxes(1,2)).swapaxes(1,2);yl=1/(2j*np.pi*f*1e9);yt[:,0,0]-=yl;yt[:,1,1]-=yl;yt[:,0,1]+=yl;yt[:,1,0]+=yl;direct=(yt[:,0,1]+yt[:,1,0])/(yt[:,0,0]+yt[:,1,1])
 else:
  B=a[:,1]+1j*a[:,2];D=a[:,3]+1j*a[:,4];A=b[:,1]+1j*b[:,2];C=b[:,3]+1j*b[:,4];cur=np.array([[B,1+A],[-B,-A]]).transpose(2,0,1);vol=np.array([[D,C],[D-1,C]]).transpose(2,0,1);yt=np.linalg.solve(vol.swapaxes(1,2),cur.swapaxes(1,2)).swapaxes(1,2);direct=(yt[:,0,1]+yt[:,1,0])/(yt[:,0,0]+yt[:,1,1])
 other=[i for i in range(10)if i!=target];T=np.zeros((20,11));T[target,0]=1;T[target+10,1]=1
 for k,i in enumerate(other):T[i,k+2]=1;T[i+10,k+2]=1
 schur=[];res=[]
 for yy in y:
  q=T.T@yy@T;sol=solve(q[2:,2:],q[2:,:2]);res.append(float(np.linalg.norm(q[2:,2:]@sol-q[2:,:2])/max(np.linalg.norm(q[2:,:2]),1e-30)));s=q[:2,:2]-q[:2,2:]@sol;schur.append((s[0,1]+s[1,0])/(s[0,0]+s[1,1]))
 schur=np.array(schur);d=crossover(f,direct);s=crossover(f,schur);entry={'target':target,'direct':d,'matrixSchur':s,'schurResidualMax':max(res),'status':'CROSSCHECK_PENDING'}
 if len(d)==len(s)==1:
  entry['fcRelativeDifference']=abs(d[0]['Hz']-s[0]['Hz'])/d[0]['Hz'];entry['PMDifferenceDegree']=abs(d[0]['PMdegree']-s[0]['PMdegree']);entry['PASS']=entry['fcRelativeDifference']<=.1 and entry['PMDifferenceDegree']<=5
 else:entry['PASS']=False;entry['reason']='crossing multiplicity requires explanation'
 entry['measurementMethod']=directMethod;entry['sourceCases']=directCases;entry['directSeriesShuntQualified']=directMethod=='SERIES_VOLTAGE_AND_SHUNT_CURRENT';entry['PASSscope']='LOADED_2PORT_VS_SCHUR_ONLY' if not entry['directSeriesShuntQualified'] else 'DIRECT_TIAN_VS_SCHUR_LIMITED_CROSSOVER';entry['status']='LOADED_2PORT_SCHUR_CROSSCHECK_PASS_DIRECT_TIAN_HOLD' if target==6 and entry['PASS'] else 'DIRECT_TIAN_SCHUR_CROSSCHECK_PASS' if entry['PASS'] else 'CROSSCHECK_HOLD'
 cross.append(entry);np.savetxt(ROOT/'results'/f'FULL_TIAN_SCHUR_{target}.csv',np.column_stack([f,direct.real,direct.imag,schur.real,schur.imag]),delimiter=',',header='Hz,directReal,directImag,schurReal,schurImag',comments='')
dump(ROOT/'FULL_NETWORK_SCHUR_TIAN_CROSSCHECK.json',cross)
print(json.dumps({'duplicateColumns':dup,'crosscheck':cross,'lowFrequency':'all .01/.1/1/10 retained, numerical qualification pending'}))
