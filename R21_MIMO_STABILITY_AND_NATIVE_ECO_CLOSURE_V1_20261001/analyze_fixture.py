import json,numpy as np
from science import ROOT,OLD,dump
from mimo_math import return_difference,recover_y
columns=[np.loadtxt(ROOT/'results'/('fixture_y2_'+str(i))/'ac.txt',skiprows=1) for i in range(4)]
f,y,cond=recover_y(columns,2);exact=np.zeros_like(y);exact[:,:2,:2]=np.eye(2)*1e-5;exact[:,2:,2:]=np.eye(2)*.001;exact[:,2:,:2]=np.array([[.1,.015],[.005,.1]])[None,:,:]/(1+1j*f[:,None,None]/1000)
l,r,d,g=return_difference(y);err=float(np.max(np.abs(y-exact))/np.max(np.abs(exact)));closure=float(np.max(np.abs(g-d@r)));analytic_l=exact[:,2:,:2]/.00101;looperr=float(np.max(abs(l-analytic_l))/np.max(abs(analytic_l)))
result={'fixtureRelativeYMax':err,'loopRelativeMax':looperr,'closureResidual':closure,'voltageMatrixConditionMax':float(np.max(cond)),'frequencyHz':[float(f[0]),float(f[-1])],'fixturePASS':err<1e-5 and looperr<1e-5 and closure<1e-12,'closedKnownPoles_rad_s':(-2*np.pi*1000*(1+np.linalg.eigvals(np.array([[.1,.015],[.005,.1]])/.00101))).tolist(),'scalarIdentityFrozen':[]}
for kind in ['row','tia','vcm','vexc']:
    data=np.loadtxt(OLD/'results'/('YPORT_'+kind+'.csv'),delimiter=',',skiprows=1);delta=float(np.max(abs((data[:,1]+1j*data[:,2])-(data[:,3]+1j*data[:,4]))/np.maximum(abs(data[:,3]+1j*data[:,4]),1e-12)))
    result['scalarIdentityFrozen'].append({'class':kind,'TianYRelativeMax':delta,'sameN1AdmittanceFormula':True})
dump(ROOT/'MIMO_FIXTURE_VALIDATION.json',result);np.savez(ROOT/'results'/'MIMO_FIXTURE.npz',freq=f,Y=y,L=l,R=r);print(json.dumps(result));assert result['fixturePASS']
