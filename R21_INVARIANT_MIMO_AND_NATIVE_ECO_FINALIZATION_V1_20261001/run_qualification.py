from pathlib import Path
import numpy as np,json,csv,hashlib,datetime
from invariant_math import closed_contour_winding,pencil_metrics,characteristic_matrix
R=Path(__file__).resolve().parent
fixtures=[('nonnormal2_stable',np.array([[-1.,1000],[-.002,-3]])),('nonnormal2_RHP',np.array([[-1.,4],[2,-1]])),('asymmetric3_stable',np.array([[-1.,40,-8],[0,-3,12],[0,0,-7]]))]
rows=[];results=[]
for name,a in fixtures:
 n=len(a);truth=np.linalg.eigvals(a);expected=sum(truth.real>0);assert np.all(np.diag(a)<0)
 scales=[np.ones(n),np.geomspace(.001,1000,n),np.geomspace(1000,.001,n)]
 entries=[]
 for scale in scales:
  w=closed_contour_winding(a,scale);assert w['winding']==expected and abs(w['rawTurns']-expected)<1e-9;entries.append({'fixedPowerConjugateScale':scale.tolist(),**w})
 for f in [.01,.1,1,10,1e4,300e6]:
  g=2j*np.pi*f*np.eye(n)-a;g0=np.diag(np.diag(g));p=pencil_metrics(g,g0)
  assert p['backwardResidualMax']<1e-12
  rows.append({'fixture':name,'Hz':f,'condGc':p['condGc'],'condG0':p['condG0'],'backwardResidualMax':p['backwardResidualMax'],'pencilSensitivityProxy':p['pencilSensitivityProxy'],'logAbsDetRatio':p['logAbsDetRatio']})
 results.append({'fixture':name,'A':a.tolist(),'independentStateSpaceEigenvalues':[[float(v.real),float(v.imag)]for v in truth],'referenceLocalPoles':np.diag(a).tolist(),'RHPTruth':int(expected),'noncommutatorNorm':float(np.linalg.norm(a@np.diag(np.diag(a))-np.diag(np.diag(a))@a)),'fixedScaleResults':entries,'scope':'analytic state-space pencil fixture only; not SPICE or full physical network reference qualification'})
with (R/'results'/'FIXTURE_QZ_RESIDUALS.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(R/'FIXTURE_QUALIFICATION.json').write_text(json.dumps({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'fixtures':results,'fixtureClassificationPASS':True,'fixedActualScale':'Sv=I,Si=I frozen before actual-network computation'},indent=2),encoding='utf-8')
# Existing stored raw matrix replay: disclose it as offline diagnostics, not a new SPICE solve.
b=json.loads((R/'EXECUTION_BUDGET.json').read_text());b['used']['diagnostics']=b['used'].get('diagnostics',0)+1;b['offlineDiagnostics'].append({'name':'frozen_matrix_QZ_scale_replay','inputCommit':'d152e092101188e6dc57f620f81d52f2e243fb01','newSPICEAnalyses':0,'counterCategory':'diagnostics','detail':'one offline numerical diagnostic; actual new OP/AC/PZ remains0; no runner exemption for new solver'})
(R/'EXECUTION_BUDGET.json').write_text(json.dumps(b,indent=2),encoding='utf-8')
old=R.parent/'R21_MIMO_STABILITY_AND_NATIVE_ECO_CLOSURE_V1';output=[]
for fn in ['mimo_blank_800_MATRIX.npz','HYBRID_MIMO.npz']:
 p=old/'results'/fn;data=np.load(p);f=data['freq'];y=data['Y'];items=[]
 for index in [0,80,160,len(f)-1]:
  g=characteristic_matrix(y[index]);g0=np.diag(np.diag(g));j={'Hz':float(f[index]),'fixedScaleMetrics':[]}
  for scale in [np.ones(10),np.geomspace(.001,1000,10),np.geomspace(1000,.001,10)]:
   si=1/scale;v=pencil_metrics(si[:,None]*g*si[None,:],si[:,None]*g0*si[None,:]);v['mu']=[[float(z.real),float(z.imag)]for z in v['mu']];v['detRatioPhase']=[float(v['detRatioPhase'].real),float(v['detRatioPhase'].imag)];v['fixedScale']=scale.tolist();j['fixedScaleMetrics'].append(v)
  items.append(j)
 output.append({'source':fn,'inputSHA256':hashlib.sha256(p.read_bytes()).hexdigest().upper(),'data':items,'lowestMeasuredHz':float(f[0]),'newLowFrequencyData':False})
(R/'FROZEN_NETWORK_QZ_PRECHECK.json').write_text(json.dumps({'scope':'old measured data offline replay, no actual full-network PASS; low0.01/0.1 absent, reference G0 not physically qualified','results':output},indent=2),encoding='utf-8')
print(json.dumps({'threeFixtures':'classification/scalingPASS','newSPICE':0,'offlineDiagnostic':b['used']['diagnostics'],'frozenNetwork':'qualification still pending'}))
