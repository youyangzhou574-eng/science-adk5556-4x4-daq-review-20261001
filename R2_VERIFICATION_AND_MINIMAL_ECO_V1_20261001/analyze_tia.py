import numpy as np,pathlib,json
ROOT=pathlib.Path(__file__).resolve().parent
rows=[]
for rev in [1,2]:
 p=ROOT/f'results/tia_r{rev}_tran/trace.txt';a=np.loadtxt(p,skiprows=1);t=a[:,0];v=a[:,5]
 end=650e-6 if rev==1 else 700e-6;window=(t>end-25e-6)&(t<end-2e-6);target=float(np.median(v[window]))
 edges=200e-6+np.arange(325,1200,25)*1e-6
 # Never compare edges after the command falls again at701us to the active-state target.
 edges=edges[(edges<t[-1])&(edges<700e-6)];err=np.interp(edges,t,v)-target
 rows.append({'case':f'tia_r{rev}_tran','reference_V':target,'reference_window_us':[(end-25e-6)*1e6,(end-2e-6)*1e6],'active_edge_times_us':(edges*1e6).tolist(),'active_edge_residual_V':err.tolist(),'max_active_residual_V':float(max(abs(err))),'status':'PASS_PARTIAL_EDGES'if max(abs(err))<=100e-6 else 'FAIL_PARTIAL_EDGES','scope':'only active edges available before pulse falls; not full1200us state or coupled proof'})
(ROOT/'results/TIA_TRANSIENT_METRICS.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
print(json.dumps(rows,indent=2))
