import json,sys,numpy as np
from science import ROOT,dump,require_technical_review
from network_cases import raw_nodes
from make_mimo import PAIRS
from mimo_math import recover_y,return_difference
def analyze(tag):
    plan=json.loads((ROOT/'cases'/(tag+'_PLAN.json')).read_text());n=10;cols=[];bias=[];missing=[]
    base=raw_nodes(plan['OPsource']);physical=['v(vcm)','v(vexc)']+[f'v(drv{i})' for i in range(4)]+[f'v(tdrv{i})' for i in range(4)]
    for j in range(20):
        mapping=plan['mapping'][str(j)];rep=mapping['representative'];path=ROOT/'results'/(tag+'_p'+str(rep));st=json.loads((path/'STATUS.json').read_text()) if(path/'STATUS.json').exists()else{}
        if st.get('status')!='NORMAL_EXIT' or st.get('analysisStatus')=='ANALYSIS_ERROR' or not(path/'ac.txt').exists():missing.append({'column':j,'representative':rep,'caseStatus':st});continue
        a=np.loadtxt(path/'ac.txt',skiprows=1);assert a.shape[1]==81
        p=mapping['permutation'];out=np.array(a,copy=True)
        for offset in [1,41]:
            for old,new in enumerate(p):out[:,offset+2*new:offset+2*new+2]=a[:,offset+2*old:offset+2*old+2]
        cols.append(out)
        op=raw_nodes(path/'op.raw');bias.append(max(abs(op[k]-base[k]) for k in physical))
    if missing:
        r={'case':tag,'status':'MIMO_MEASUREMENT_NUMERICAL_HOLD','missingColumns':missing,'actualColumnBiasDifferences':bias};dump(ROOT/(tag+'_RESULT.json'),r);print(json.dumps({'tag':tag,'missing':len(missing),'bias':bias}));return r
    f,y,condition=recover_y(cols,n);l,rd,d,g=return_difference(y);sv=np.linalg.svd(rd,compute_uv=False);eig=np.linalg.eigvals(l);minindex=int(np.argmin(sv[:,-1]));tail=max(float(np.max(abs(eig[-1]))),float(np.linalg.svd(l[-1],compute_uv=False)[0]));delta=float(np.max(bias));allfinite=bool(np.all(np.isfinite(y)))
    result={'case':tag,'status':'MIMO_ENGINEERING_SCREEN_ONLY','range_Hz':[float(f[0]),float(f[-1])],'points':len(f),'sigmaMin':float(sv[minindex,-1]),'sigmaMinFrequencyHz':float(f[minindex]),'minEigenDistanceToMinusOne':float(np.min(abs(1+eig))),'upperEigenGainMax':float(np.max(abs(eig[-1]))),'upperLoopSpectralNorm':float(np.linalg.svd(l[-1],compute_uv=False)[0]),'portVoltageMatrixConditionMax':float(np.max(condition)),'baselineConditionMax':float(np.max(np.linalg.cond(d))),'actualColumnBiasMaxV':delta,'closureIdentityResidual':float(np.max(abs(g-d@rd))),'allFinite':allfinite,'symmetryGraphPASS':True,'dangerReviewRequired':float(sv[minindex,-1])<.20,'provisionalPASS':False,'missingQualifications':['full-network scalar crosscheck','independent repeated column','reference D qualification','general noncommuting fixture'],'notProved':'open-reference/internal RHP pole count and infinite-frequency absolute stability; scalar extraction/independent duplicate not yet checked'}
    if result['dangerReviewRequired']:require_technical_review('sigma_min_I_plus_L below 0.20',tag)
    np.savez(ROOT/'results'/(tag+'_MATRIX.npz'),freq=f,Y=y,L=l,R=rd,eigenvalues=eig,singular_values=sv)
    np.savetxt(ROOT/'results'/(tag+'_METRICS.csv'),np.column_stack([f,sv[:,-1],np.min(abs(1+eig),axis=1),np.max(abs(eig),axis=1)]),delimiter=',',header='frequency_Hz,sigma_min_I_plus_L,min_eigen_distance_to_minus1,max_eigen_gain',comments='')
    np.savetxt(ROOT/'results'/(tag+'_MATRIX.csv'),np.column_stack([f,l.real.reshape(len(f),100),l.imag.reshape(len(f),100)]),delimiter=',',header='frequency_Hz,'+','.join([part+'L_'+str(i)+'_'+str(j)for part in['real_','imag_']for i in range(10)for j in range(10)]),comments='')
    dump(ROOT/(tag+'_RESULT.json'),result);print(json.dumps(result));return result
if __name__=='__main__':analyze(sys.argv[1])
