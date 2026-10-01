"""Finite imaginary-axis proxy ONLY: not certified full RHP contour Nyquist."""
import numpy as np,json,datetime,csv
from science import ROOT,dump
from invariant_math import logdet
p=np.load(ROOT/'results/NEW_GC.npz');f=p['freq'];rows=[];summary=[]
for label in ['openGc','closedGc']:
 for index,scale in enumerate([np.ones(10),np.geomspace(.001,1000,10),np.geomspace(1000,.001,10)]):
  si=1/scale;ph=[];logs=[]
  for gg in p[label]:
   g=si[:,None]*gg*si[None,:];g0=np.diag(np.diag(g));lg,sg=logdet(g);l0,s0=logdet(g0);ph.append(sg/s0);logs.append(lg-l0)
  ph=np.asarray(ph)
  # Explicit provisional connections: +low to -low and high through conjugate high.
  # No measured DC gap or RHP arc; these segments CANNOT certify an absolute winding.
  contour=np.r_[ph[::-1],np.conj(ph),ph[-1]];inc=np.angle(np.r_[contour[1:]/contour[:-1],contour[0]/contour[-1]])
  summary.append({'topology':label,'fixedScale':scale.tolist(),'finiteAxisProxyTurns':float(sum(inc)/(2*np.pi)),'maxPhaseIncrementRad':float(max(abs(inc))),'lowFrequencyHz':float(f[0]),'highFrequencyHz':float(f[-1]),'lowEndpointPhaseRealImag':[float(ph[0].real),float(ph[0].imag)],'highEndpointPhaseRealImag':[float(ph[-1].real),float(ph[-1].imag)],'fullRHPCertificate':False})
  for hz,pp,ll in zip(f,ph,logs):rows.append({'topology':label,'scaleIndex':index,'Hz':float(hz),'detPhaseReal':float(pp.real),'detPhaseImag':float(pp.imag),'logAbsDetRatio':float(ll)})
with(ROOT/'results/DETERMINANT_FINITE_AXIS_PROXY.csv').open('w',newline='')as out:w=csv.DictWriter(out,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
dump(ROOT/'DETERMINANT_PROXY_SUMMARY.json',{'results':summary,'definition':'descend measured positive imaginary axis; join +0.01Hz to conjugate negative0.01Hz; ascend negative data; join high endpoints. Unknown low gap and RHP semicircle are not measured. No reference/internal RHP pole certificate. Proxy0 is NOT MIMO generalized Nyquist PASS.'})
b=json.loads((ROOT/'EXECUTION_BUDGET.json').read_text());b['used']['diagnostics']+=1;b['offlineDiagnostics'].append({'name':'auditable_determinant_proxy_reexecution','newSPICEAnalyses':0,'afterScienceSTOP':'offline evidence packaging only; no new SPICE or design'});dump(ROOT/'EXECUTION_BUDGET.json',b)
print(json.dumps({'proxyTurns':[x['finiteAxisProxyTurns']for x in summary],'fullRHPCertificate':False,'diagnosticsTotal':b['used']['diagnostics']}))
