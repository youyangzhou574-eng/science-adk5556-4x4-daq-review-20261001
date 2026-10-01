import numpy as np,json,csv
from science import ROOT,dump
def load(kind,inj):return np.loadtxt(ROOT/'results'/f'loop_{kind}_{inj}'/'ac.txt',skiprows=1)
def crosses(f,z):
    db=20*np.log10(abs(z));ph=np.unwrap(np.angle(z))*180/np.pi
    # phase branch referenced to low-frequency positive negative-feedback return ratio.
    ph-=round(ph[0]/360)*360
    rows=[]
    for j in np.flatnonzero(db[:-1]*db[1:]<0):
        a=-db[j]/(db[j+1]-db[j]);fc=np.exp(np.log(f[j])+a*np.log(f[j+1]/f[j]));p=ph[j]+a*(ph[j+1]-ph[j])
        rows.append({'fc_Hz':float(fc),'phase_deg':float(p),'PM_deg':float(180+p),'direction':'falling' if db[j+1]<db[j] else 'rising'})
    return rows
def calc(kind):
    v,i=load(kind,'v'),load(kind,'i');assert np.array_equal(v[:,0],i[:,0])
    f=v[:,0];D=v[:,1]+1j*v[:,2];B=v[:,5]+1j*v[:,6];C=i[:,1]+1j*i[:,2];A=i[:,5]+1j*i[:,6]
    vf=v[:,3]+1j*v[:,4];Tvol=-vf/D
    det=A*D-B*C
    Ttwo=(2*det-A+D)/(1-2*det+A-D)
    cv,ct=crosses(f,Tvol),crosses(f,Ttwo)
    passed=len(cv)==len(ct) and len(cv)>0 and all(abs(a['fc_Hz']/b['fc_Hz']-1)<=.1 and abs(a['PM_deg']-b['PM_deg'])<=5 for a,b in zip(cv,ct))
    result={'class':kind,'voltage_method_crossings':cv,'Tian_twoport_crossings':ct,'crosscheck_PASS':passed,'max_abs_complex_difference':float(np.max(abs(Tvol-Ttwo))), 'OP_delta_max':float(np.max(abs(np.loadtxt(ROOT/'results'/f'loop_{kind}_v'/'op.txt',skiprows=1)-np.loadtxt(ROOT/'results'/f'loop_{kind}_i'/'op.txt',skiprows=1))))}
    if kind=='fixture':
        exact=(100*.001/(1+1j*f/1000))/(.001+.00001)
        result['fixture_Tian_relative_error_max']=float(np.max(abs(Ttwo-exact)/abs(exact)))
        assert result['fixture_Tian_relative_error_max']<1e-5,'Tian sign/orientation/formula not validated'
    data=np.column_stack([f,Tvol.real,Tvol.imag,Ttwo.real,Ttwo.imag])
    np.savetxt(ROOT/'results'/('METHOD_'+kind+'.csv'),data,delimiter=',',header='frequency_Hz,series_voltage_real,series_voltage_imag,Tian_return_real,Tian_return_imag',comments='')
    return result
if __name__=='__main__':
    import sys
    kinds=sys.argv[1:] or ['fixture','row','tia','vcm','vexc'];r=[calc(k) for k in kinds];dump(ROOT/'RETURN_RATIO_RESULTS.json',r);print(json.dumps(r,indent=2))
