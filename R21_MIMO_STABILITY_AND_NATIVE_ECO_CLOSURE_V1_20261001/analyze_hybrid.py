import json,numpy as np
from science import ROOT,dump,require_technical_review
from network_cases import raw_nodes
from mimo_math import return_difference
tag='hybrid_blank_800';plan=json.loads((ROOT/'cases'/(tag+'_PLAN.json')).read_text());columns=[];bias=[];missing=[];baseline=raw_nodes(plan['OPsource'])
for j in range(20):
    m=plan['mapping'][str(j)];p=ROOT/'results'/(tag+'_p'+str(m['representative']));st=json.loads((p/'STATUS.json').read_text()) if(p/'STATUS.json').exists()else{}
    if st.get('status')!='NORMAL_EXIT' or st.get('analysisStatus')=='ANALYSIS_ERROR' or not(p/'hybrid.txt').exists():missing.append(j);continue
    data=np.loadtxt(p/'hybrid.txt',skiprows=1);assert data.shape[1]==41;out=data.copy();permutation=m['permutation'][:10]
    for offset in [1,21]:
        for old,new in enumerate(permutation):out[:,offset+2*new:offset+2*new+2]=data[:,offset+2*old:offset+2*old+2]
    columns.append(out);op=raw_nodes(p/'op.raw');bias.append(max(abs(op[k]-v) for k,v in baseline.items() if k in ['v(vcm)','v(vexc)']+[f'v(drv{i})'for i in range(4)]+[f'v(tdrv{i})'for i in range(4)]))
if missing:
    dump(ROOT/'HYBRID_RESULT.json',{'missing':missing,'status':'NUMERICAL_HOLD','bias':bias});print('MISSING',missing);raise SystemExit(1)
f=columns[0][:,0];ff=np.stack([a[:,1:21:2]+1j*a[:,2:21:2] for a in columns],axis=2);ee=np.stack([a[:,21::2]+1j*a[:,22::2] for a in columns],axis=2);B,A=ff[:,:,:10],ff[:,:,10:];D,C=ee[:,:,:10],ee[:,:,10:];eye=np.broadcast_to(np.eye(10),D.shape)
# Network currents into e/f and voltage e/f are reconstructed by exact port KCL.
cur=np.concatenate([np.concatenate([B,eye+A],axis=2),np.concatenate([-B,-A],axis=2)],axis=1)
vol=np.concatenate([np.concatenate([D,C],axis=2),np.concatenate([D-eye,C],axis=2)],axis=1)
y=np.linalg.solve(vol.swapaxes(1,2),cur.swapaxes(1,2)).swapaxes(1,2);l,rd,diag,g=return_difference(y);sv=np.linalg.svd(rd,compute_uv=False);eig=np.linalg.eigvals(l);cond=np.linalg.cond(vol);delta=float(max(bias));index=int(np.argmin(sv[:,-1]));relative=float(np.max(abs(g-diag@rd))/np.max(abs(g)))
old=np.load(ROOT/'results'/'mimo_blank_800_MATRIX.npz');difference=np.max(abs(l-old['L']),axis=(1,2))/np.maximum(np.max(abs(old['L']),axis=(1,2)),1e-30)
result={'status':'CLOSED_DOUBLE_INJECTION_MIMO_NUMERICAL_REVIEW','biasDifferenceMaxV':delta,'voltageReconstructionConditionMax':float(max(cond)),'sigmaMin':float(sv[index,-1]),'sigmaMinFrequencyHz':float(f[index]),'upperEigenGainMax':float(np.max(abs(eig[-1]))),'relativeClosureResidual':relative,'openClosedLRelativeDifferenceMax':float(max(difference)),'methodTrustedBandHz':[float(f[np.where(cond<1e12)[0][0]]) if np.any(cond<1e12) else None,float(f[-1])],'notAnInstabilityClaim':True,'PASS':False}
if result['sigmaMin']<.20:require_technical_review('sigma_min_I_plus_L below 0.20',tag)
np.savez(ROOT/'results'/'HYBRID_MIMO.npz',freq=f,Y=y,L=l,R=rd,eigenvalues=eig,sigma=sv[:,-1],condition=cond,openClosedRelativeDifference=difference)
np.savetxt(ROOT/'results'/'HYBRID_CONDITION_AND_COMPARISON.csv',np.column_stack([f,cond,sv[:,-1],difference]),delimiter=',',header='frequency_Hz,hybrid_reconstruction_condition,sigma_min_I_plus_L,open_closed_L_relative_difference',comments='')
dump(ROOT/'HYBRID_RESULT.json',result);print(json.dumps(result))
