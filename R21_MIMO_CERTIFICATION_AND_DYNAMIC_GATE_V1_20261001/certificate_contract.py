"""Offline known-realization checks, never certify a sampled physical network."""
import numpy as np

def internal_certificate(a,b,c):
 a=np.asarray(a);b=np.asarray(b);c=np.asarray(c);n=len(a);p=np.linalg.eigvals(a);rhp=p[p.real>0]
 hidden=[]
 for pole in rhp:
  controllable=np.linalg.matrix_rank(np.c_[pole*np.eye(n)-a,b])==n
  observable=np.linalg.matrix_rank(np.r_[pole*np.eye(n)-a,c])==n
  if not controllable or not observable:hidden.append(complex(pole))
 return {'internallyStable':bool(np.all(p.real<0)),'hiddenRHPCount':len(hidden),'portResponseCertifiesInternalStability':len(hidden)==0,'scope':'KNOWN_STATE_SPACE_REALIZATION_ONLY','poles':[{'real':float(x.real),'imag':float(x.imag)}for x in p]}

def reference_contract(referencePoles,referenceZeros,internalCertificate):
 poles=sum(complex(x).real>0 for x in referencePoles);zeros=sum(complex(x).real>0 for x in referenceZeros)
 return {'referenceRHPPoles':poles,'referenceRHPZeros':zeros,'internalCertificate':bool(internalCertificate),'defaultZeroWindingSufficient':poles==0 and zeros==0 and bool(internalCertificate),'scope':'KNOWN_RATIONAL_DETERMINANT_ONLY','unknownPhysicalData':'HOLD'}

def block_reference(g):
 g=np.asarray(g);assert g.shape==(10,10);z=np.zeros_like(g)
 for ids in ([2,3,4,5],[6,7,8,9],[0,1]):z[np.ix_(ids,ids)]=g[np.ix_(ids,ids)]
 return z

def frequency_coverage(freq):
 rows=[]
 for f in (.01,.1,1.,10.):
  nearest=float(freq[np.argmin(abs(freq-f))]);rows.append({'requiredHz':f,'nearestActualHz':nearest,'absoluteDifferenceHz':abs(nearest-f),'exact':abs(nearest-f)<=1e-10})
 return {'allRequiredExact':all(x['exact']for x in rows),'points':rows,'interpolationUsed':False}

def spectrum_comparison(a,b):
 from scipy.optimize import linear_sum_assignment
 finiteA=np.isfinite(a);finiteB=np.isfinite(b);aa=a[finiteA];bb=b[finiteB]
 r={'infiniteCountA':int(sum(~finiteA)),'infiniteCountB':int(sum(~finiteB)),'fullFiniteQualified':bool(np.all(finiteA)and np.all(finiteB)),'finiteMatchedDifference':None,'status':'FULL_SPECTRUM_HOLD'if not(np.all(finiteA)and np.all(finiteB))else 'FINITE_NUMERICAL_COMPARISON_ONLY'}
 if len(aa)==len(bb)and len(aa):
  cost=abs(aa[:,None]-bb[None,:])/np.maximum(1,abs(aa[:,None]));i,j=linear_sum_assignment(cost);r['finiteMatchedDifference']=float(max(cost[i,j]))
 return r
