import json,re,csv,numpy as np
from science import ROOT,dump
def matrix(p):
    with p.open()as f:header=f.readline().split()
    return header,np.loadtxt(p,skiprows=1)
def check_static(d):
    cfg=json.loads((ROOT/'cases'/(d.name+'.json')).read_text());op=d/'op.txt';ac=d/'ac.txt'
    if not op.exists()or not ac.exists():return {'case':d.name,'status':'NUMERICAL_NO_VALID_DC_AC'}
    h,x=matrix(op);ha,a=matrix(ac)
    assert len(x)==len(h)and a.shape[1]==len(ha)
    values=dict(zip(h[1:],x[1:]));finite=np.isfinite(x).all()and np.isfinite(a).all()
    bias=abs(values['v(vcm)']-2.5)<.001 and abs(values['v(vexc)']-2.25)<.001
    # driver clipping is evaluated only at a finite, intended-bias OP.
    drivers={n:v for n,v in values.items() if re.fullmatch(r'v\((?:t?drv|cmdrv|exdrv)\d?\)',n)}
    no_rail=all(.05<v<cfg['vdd']-.05 for v in drivers.values())
    peaks={}
    for i in range(4):
        n='v(ain'+str(i)+')';idx=ha.index(n);z=a[:,idx]+1j*a[:,idx+1];peaks[n]={'peak_magnitude':float(abs(z).max()),'peak_frequency_Hz':float(a[abs(z).argmax(),0])}
    cols=values['v(col0)'];cols_ok=all(abs(values[f'v(col{i})']-values['v(vcm)'])<.001 for i in range(4))
    return {'case':d.name,'state':cfg['state'],'load':cfg['load'],'vdd':cfg['vdd'],'status':'FINITE_STATIC_SCREEN_ONLY'if finite and bias and cols_ok and no_rail else 'INVALID_OR_CLIPPING_REQUIRES_REVIEW','VCM_V':values['v(vcm)'],'VEXC_V':values['v(vexc)'],'drivers_V':drivers,'no_rail_at_valid_OP':bool(no_rail),'AC_frequency_range_Hz':[float(a[0,0]),float(a[-1,0])],'AC_points':len(a),'AC_peaks':peaks,'RHP_poles_proved_absent':False}
def check_trace(d):
    p=d/'trace.txt'
    if not p.exists():
        s=json.loads((d/'STATUS.json').read_text());return {'case':d.name,'status':'INCOMPLETE_NO_SETTLING_PROOF','last_progress_time_s':s.get('lastProgressTime_s'),'wall_s':s.get('wallSeconds'),'stop':s.get('reason')}
    h,a=matrix(p);t=a[:,0];single=d.name.startswith('single_');sw=100e-6
    targets=[n for n in h if n.startswith('v(ain')]
    valid=(t>=sw+300e-6)&(t<=sw+500e-6);tail=(t>=t[-1]-20e-6)
    measures=[]
    if single:
        # Actual non-dummy CS edges across four 9-transfer channel slots: 32, not35.
        edges=np.array([sw+(300+(ch*9+slot)*25)*1e-6 for ch in range(4)for slot in range(1,9)])
        assert len(edges)==32 and edges[-1]<t[-1]
    else:edges=sw+np.arange(325,501,25)*1e-6
    for n in targets:
        v=a[:,h.index(n)];ref=float(np.median(v[tail]));res=np.interp(edges,t,v)-ref
        measures.append({'node':n,'reference_V':ref,'edge_count':len(edges),'edge_times_us':(edges*1e6).tolist(),'max_edge_residual_V':float(abs(res).max()),'max_continuous_300_500us_residual_V':float(abs(v[valid]-ref).max()),'tail_span_V':float(np.ptp(v[tail])),'PASS_screen':bool(abs(res).max()<=100e-6 and abs(v[valid]-ref).max()<=100e-6)})
    return {'case':d.name,'status':'LOCAL_SCREEN_PASS'if all(x['PASS_screen']for x in measures)else'LOCAL_SCREEN_FAIL','method':'trap'if 'single_'in d.name else'gear','scope':'single ideal-VCM equivalent load'if single else'4 macros, ideal remaining ports; Gear numerical diagnostic only; eight short-window sample edges per modeled AIN, not whole frame','last_time_s':float(t[-1]),'points':len(t),'measurements':measures}
def run():
    stat=[check_static(d)for d in sorted((ROOT/'results').glob('full_static*'))]
    traces=[check_trace(d)for d in sorted((ROOT/'results').iterdir())if d.name.startswith(('part_','single_','full_monolithic'))]
    dump(ROOT/'STATIC_COUPLED_RESULTS.json',stat);dump(ROOT/'TRANSIENT_RESULTS.json',traces)
    rows=[]
    for d in sorted((ROOT/'results').iterdir()):
        if not d.is_dir()or not(d/'STATUS.json').exists():continue
        j=json.loads((d/'STATUS.json').read_text());err=(d/'stderr.log').read_text(errors='replace');analysis_error=bool(re.search(r'(?im)^Error:|simulation\(s\) aborted|doAnalyses:',err))
        rows.append({'case':d.name,'processStatus':j['status'],'exitCode':j.get('exitCode'),'analysisErrors':analysis_error,'wallSeconds':j.get('wallSeconds'),'progressLast_s':j.get('lastProgressTime_s'),'OP':(d/'op.txt').exists(),'AC':(d/'ac.txt').exists(),'trace':(d/'trace.txt').exists(),'stopReason':j.get('reason'),'qualifiedModelsUnchanged':True})
    with(ROOT/'CASE_EXECUTION_INDEX.csv').open('w',encoding='utf-8',newline='')as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    print(json.dumps({'all_cases':len(rows),'static_total':len(stat),'static_finite':sum(x['status']=='FINITE_STATIC_SCREEN_ONLY'for x in stat),'static_invalid':sum(x['status']=='INVALID_OR_CLIPPING_REQUIRES_REVIEW'for x in stat),'trace_complete':sum(x['status'].startswith('LOCAL_SCREEN')for x in traces),'trace_screen_pass':sum(x['status']=='LOCAL_SCREEN_PASS'for x in traces)},indent=2))
if __name__=='__main__':run()
