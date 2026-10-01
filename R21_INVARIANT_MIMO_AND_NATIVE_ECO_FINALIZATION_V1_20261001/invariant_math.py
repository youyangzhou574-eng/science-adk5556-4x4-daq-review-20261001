"""Qualified synthetic port pencils; real network pole count remains separate."""
import numpy as np
from scipy.linalg import eig,lu_factor

def power_coordinates(v,i):
 n=len(v)//2
 return np.r_[(v[:n]+v[n:])/2,v[:n]-v[n:]],np.r_[i[:n]+i[n:],(i[:n]-i[n:])/2]

def characteristic_matrix(y):
 n=y.shape[-1]//2;eye=np.eye(n);t=np.block([[eye,.5*eye],[eye,-.5*eye]])
 transformed=t.T@y@t
 return transformed[:n,:n]

def logdet(a):
 lu,piv=lu_factor(a);d=np.diag(lu)
 if np.any(d==0):return -np.inf,0j
 sign=(-1)**np.count_nonzero(piv!=np.arange(len(piv)))
 return float(np.sum(np.log(abs(d)))),complex(sign*np.prod(d/abs(d)))

def pencil_metrics(g,g0):
 # Generalized eigenproblem, homogeneous alpha/beta; no inverse of G0.
 ab,left,right=eig(g,g0,left=True,right=True,homogeneous_eigvals=True)
 alpha,beta=ab;values=np.divide(alpha,beta,out=np.full(alpha.shape,np.inf+0j),where=abs(beta)>0)
 ng=np.linalg.norm(g,2);n0=np.linalg.norm(g0,2);residual=[];sensitivity=[]
 for j in range(len(alpha)):
  v=right[:,j];u=left[:,j];den=(abs(beta[j])*ng+abs(alpha[j])*n0)*np.linalg.norm(v)
  residual.append(float(np.linalg.norm(beta[j]*(g@v)-alpha[j]*(g0@v))/max(den,np.finfo(float).tiny)))
  coupling=abs(np.vdot(u,g0@v));sensitivity.append(float(np.linalg.norm(u)*np.linalg.norm(v)/max(coupling,np.finfo(float).tiny)))
 lg,sg=logdet(g);l0,s0=logdet(g0)
 return {'mu':values,'backwardResidualMax':max(residual),'pencilSensitivityProxy':max(sensitivity),'logAbsDetRatio':lg-l0,'detRatioPhase':sg/s0,'condGc':float(np.linalg.cond(g)),'condG0':float(np.linalg.cond(g0))}

def closed_contour_winding(a,scale):
 n=len(a);omega=np.unique(np.r_[0,np.geomspace(2*np.pi*.01,2*np.pi*300e6,1800),2*np.pi*np.array([.01,.1,1,10])]);radius=omega[-1]
 # Positive orientation of RHP contour: descend imaginary axis, return on right arc.
 path=np.r_[1j*omega[::-1],-1j*omega[1:],radius*np.exp(1j*np.linspace(-np.pi/2,np.pi/2,901))[1:]]
 si=1/np.asarray(scale);ph=[];la=[]
 for s in path:
  g=s*np.eye(n)-a;g0=np.diag(np.diag(g));g=si[:,None]*g*si[None,:];g0=si[:,None]*g0*si[None,:]
  lg,sg=logdet(g);l0,s0=logdet(g0);ph.append(sg/s0);la.append(lg-l0)
 ph=np.asarray(ph);increments=np.angle(np.r_[ph[1:]/ph[:-1],ph[0]/ph[-1]]);turns=float(sum(increments)/(2*np.pi))
 return {'winding':int(round(turns)),'rawTurns':turns,'maxPhaseIncrementRad':float(max(abs(increments))),'minLogAbsDetRatio':float(min(la)),'pointCount':len(path),'contourClosed':True,'RHPReferenceZeros':int(sum(np.diag(a)>0))}
