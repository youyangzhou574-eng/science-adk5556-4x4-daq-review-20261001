from pathlib import Path
import sys,json,datetime,hashlib,csv,shutil
import numpy as np
from scipy.optimize import linear_sum_assignment
from certificate_contract import block_reference,internal_certificate,reference_contract,frequency_coverage,spectrum_comparison
ROOT=Path(__file__).resolve().parent;OLD=ROOT.parent/'R21_INVARIANT_MIMO_AND_NATIVE_ECO_FINALIZATION_V1'
sys.path.insert(0,str(OLD));from invariant_math import pencil_metrics,logdet
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
budget=ROOT/'EXECUTION_BUDGET.json';b=json.loads(budget.read_text());assert b['used']['diagnostic']==11 and not b['scienceStopped'] and not b.get('qzInfiniteRetryDebited')
b['used']['diagnostic']+=6;b['qzInfiniteRetryDebited']=True;b['events'].append({'UTC':now(),'kind':'ADDITIONAL_DEBIT_PRESERVED_INFINITE_QZ_FAILURE','diagnostic':6,'actualAnalyses':0,'reason':'previous attempt wrote3 open pencil datasets then infinite-eigenvalue matching failed; conservatively debit all6 replayed pencils, no reset'});budget.write_text(json.dumps(b,indent=2),encoding='utf-8')
for folder in ('inputs','results','evidence'):(ROOT/folder).mkdir(exist_ok=True)
source=OLD/'results/NEW_GC.npz';shutil.copyfile(source,ROOT/'inputs/NEW_GC.npz');data=np.load(source);freq=data['freq'];coverage=frequency_coverage(freq)
(ROOT/'EXACT_FREQUENCY_COVERAGE.json').write_text(json.dumps(coverage,indent=2),encoding='utf-8')
inputMeta={'UTC':now(),'fixedCommit':'2e2829f17c2b07c95c5d5c953a5fc3fdfb0a3b98','source':str(source),'SHA256':hashlib.sha256(source.read_bytes()).hexdigest().upper(),'frequencyCount':len(freq),'minHz':float(freq.min()),'maxHz':float(freq.max()),'allColumnsActual':True,'matrixGroups':{'REF':[0,1],'ROW':[2,3,4,5],'TIA':[6,7,8,9]},'interpretation':'principal block extraction is an algebraic candidate, not proof of independently realizable physical reference or internal stability'}
(ROOT/'INPUT_VERIFIED.json').write_text(json.dumps(inputMeta,indent=2),encoding='utf-8')
summary={};allValues={};warnings=[]
scales=[np.ones(10),np.geomspace(1e-3,1e3,10),np.geomspace(1e3,1e-3,10)]
for top in ('openGc','closedGc'):
 gset=data[top];topsummary=[];mvalues=[]
 for sn,scale in enumerate(scales):
  rows=[];phases=[];mus=[];maxcond=0
  for f,g in zip(freq,gset):
   g0=block_reference(g);k=1/scale;gs=k[:,None]*g*k[None,:];g0s=k[:,None]*g0*k[None,:]
   try:m=pencil_metrics(gs,g0s)
   except Exception as error:raise RuntimeError(f'{top} scale{sn} {f}: {error}')
   mus.append(m['mu']);phases.append(m['detRatioPhase']);maxcond=max(maxcond,m['condGc']);row=[f,m['condGc'],m['condG0'],m['backwardResidualMax'],m['pencilSensitivityProxy'],m['logAbsDetRatio'],np.angle(m['detRatioPhase'])]
   row.extend(v for z in m['mu']for v in (z.real,z.imag));rows.append(row)
  with (ROOT/'results'/f'{top}_SCALE_{sn}_BLOCK_PENCIL.csv').open('w',newline='',encoding='utf-8')as fh:
   w=csv.writer(fh);w.writerow(['frequencyHz','condGc','condG0','backwardResidualMax','pencilSensitivityProxy','logAbsDetRatio','detPhaseRad']+[f'mu{i}_{part}'for i in range(10)for part in ('real','imag')]);w.writerows(rows)
  # An explicit sampled-axis proxy, not an evaluation on the missing RHP arc/DC gap.
  phase=np.asarray(phases);proxy=np.r_[np.conj(phase[::-1]),phase];steps=np.angle(np.r_[proxy[1:]/proxy[:-1],proxy[0]/proxy[-1]])
  item={'scaleIndex':sn,'fixedScale':scale.tolist(),'powerConjugate':True,'proxyTurns':float(steps.sum()/(2*np.pi)),'maxProxyPhaseIncrement':float(max(abs(steps))),'condGcMaximum':maxcond,'pointCount':len(freq),'realRHPContourQualified':False,'referenceInternalCertificate':False,'status':'OFFLINE_CANDIDATE_ONLY'}
  topsummary.append(item);mvalues.append(np.asarray(mus))
 for sn in (1,2):
  errors=[];details=[]
  for a,c in zip(mvalues[0],mvalues[sn]):
   match=spectrum_comparison(a,c);details.append(match);errors.append(match['finiteMatchedDifference'])
  finiteErrors=[x for x in errors if x is not None];topsummary[sn]['finiteMatchedDifferenceMax']=max(finiteErrors)if finiteErrors else None;topsummary[sn]['fullSpectrumHoldFrequencyCount']=sum(not x['fullFiniteQualified']for x in details);topsummary[sn]['lowFrequencyComparisons']={str(f):dict(details[int(np.argmin(abs(freq-f)))],actualFrequencyHz=float(freq[np.argmin(abs(freq-f))]))for f in [.01,.1,1,10]}
  with (ROOT/'results'/f'{top}_SCALE_{sn}_SPECTRUM_COMPARISON.csv').open('w',newline='',encoding='utf-8')as fh:
   w=csv.writer(fh);w.writerow(['frequencyHz','infiniteCountBaseline','infiniteCountScaled','fullFiniteQualified','finiteMatchedDifference']);w.writerows([f,x['infiniteCountA'],x['infiniteCountB'],x['fullFiniteQualified'],x['finiteMatchedDifference']]for f,x in zip(freq,details))
 summary[top]=topsummary

# Exact hidden-state counterexample: same observed response, one unstable unobservable/uncontrollable state.
a=np.diag([-1.,1.]);bb=np.array([[1.],[0.]]);cc=np.array([[1.,0.]])
hidden=internal_certificate(a,bb,cc);comparison=[]
for f in freq:
 s=2j*np.pi*f;observed=(cc@np.linalg.solve(s*np.eye(2)-a,bb))[0,0];expected=1/(s+1);comparison.append(abs(observed-expected))
hidden.update(A=a.tolist(),B=bb.tolist(),C=cc.tolist(),sameObservedTransfer='1/(s+1)',maxObservedDifference=float(max(comparison)),conclusion='port transfer alone cannot distinguish stable realization A=[-1] from A=diag(-1,+1) with hidden +1 state; illustrative only, no evidence actual OPA has hidden RHP modes')

# Proper rational determinants have no RHP poles but reference has a RHP zero.
omega=np.r_[0,np.geomspace(1e-6,1e6,2400)];path=np.r_[1j*omega[::-1],-1j*omega[1:],1e6*np.exp(1j*np.linspace(-np.pi/2,np.pi/2,1501))[1:]]
ratio=(path+1)/(path-1);increments=np.angle(np.r_[ratio[1:]/ratio[:-1],ratio[0]/ratio[-1]])
reference=reference_contract([-2],[1],True);reference.update(Gc='(s+1)/(s+2)',G0='(s-1)/(s+2)',R='(s+1)/(s-1)',positiveOrientation='imaginary axis downwards plus true RHP arc',winding=float(sum(increments)/(2*np.pi)),trueContour=True,fullSystemGcRHPZeroCount=0,detRatioRHPPoleCount=1,conclusion='stable Gc can have winding -1 relative to reference with RHP zero; no RHP transfer poles alone does not warrant a default N=0 criterion; not rejection of a separately qualified internally stable physical reference')

fixtures=[]
for label,unstable in [('stable_block_fixture',False),('unstable_interblock_fixture',True)]:
 a=-np.diag(np.arange(1,11,dtype=float));a[0,2]=4.;a[2,0]=2. if unstable else .1;a[4,8]=.5
 poles=np.linalg.eigvals(a);a0=block_reference(a);rp=np.linalg.eigvals(a0);turns=[]
 # Independent known-state fixture: evaluate the actual complex RHP contour, not measured-data interpolation.
 for scale in scales:
  k=1/scale;phase=[]
  for s in path:
   g=s*np.eye(10)-a;g0=s*np.eye(10)-a0;_,sg=logdet(k[:,None]*g*k[None,:]);_,s0=logdet(k[:,None]*g0*k[None,:]);phase.append(sg/s0)
  z=np.asarray(phase);turns.append(float(sum(np.angle(np.r_[z[1:]/z[:-1],z[0]/z[-1]]))/(2*np.pi)))
 expected=int(sum(poles.real>0));assert all(abs(x-expected)<1e-8 for x in turns) and np.all(rp.real<0)
 fixtures.append({'label':label,'A':a.tolist(),'knownPoles':poles.tolist(),'referencePoles':rp.tolist(),'expectedRHPCount':expected,'trueRHPWindingAllScales':turns,'status':'PASS_KNOWN_REALIZATION_FIXTURE_ONLY'})

for name,item in [('BLOCK_REFERENCE_CANDIDATES.json',summary),('HIDDEN_INTERNAL_MODE_COUNTEREXAMPLE.json',hidden),('REFERENCE_ZERO_COUNTEREXAMPLE.json',reference),('KNOWN_BLOCK_REALIZATION_FIXTURES.json',fixtures)]:
 (ROOT/name).write_text(json.dumps(item,indent=2),encoding='utf-8')
gates={'MIMO_REFERENCE_QUALIFIED':'HOLD physical block realization and internal pole/zero certificate missing','GENERALIZED_NYQUIST_PASS':'HOLD actual data only finite imaginary axis, no certified real RHP contour/DC gap/high arc','FULL_NETWORK_PORT_CUT_PASS':'PARTIAL inherited VCM/VEXC/ROW0 direct; TIA loaded scope only','TIA_LOADED_DOMAIN_CONFIRMED':'PARTIAL finite-crossing domain from prior evidence, not internal stability certificate','EXACT_LOW_FREQUENCY_POINTS':'HOLD .01 exact; .1/1/10 only nearest existing samples, no interpolation','PARTITIONED_COUPLED_DYNAMIC':'NOT_ENTERED','R2_1_NATIVE_ECO':'NOT_ENTERED','BENCH':'NOT_RELEASED','NO_SYMMETRY_RECONSTRUCTION':True,'actualCircuitInstabilityProven':False,'actualCircuitStabilityProven':False,'scienceSTOP':'REFERENCE_REALIZATION_AND_INTERNAL_CERTIFICATE_HOLD'}
(ROOT/'GATES.json').write_text(json.dumps(gates,indent=2),encoding='utf-8')
b=json.loads(budget.read_text());b.update(scienceStopped=True,scienceStoppedUTC=now(),stopReason=gates['scienceSTOP']);b['events'].append({'UTC':now(),'kind':'STICKY_SCIENTIFIC_STOP','newSolversStarted':0,'reason':gates['scienceSTOP']});budget.write_text(json.dumps(b,indent=2),encoding='utf-8')
print(json.dumps({'diagnostic':17,'actualSPICE':0,'fixtures':fixtures,'hidden':hidden,'referenceWinding':reference['winding'],'gate':gates['scienceSTOP'],'frequencyCoverage':coverage,'blockSummary':summary},default=lambda x:x.real if isinstance(x,complex)and x.imag==0 else str(x)))
