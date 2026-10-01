import pathlib,numpy as np,json
ROOT=pathlib.Path(__file__).resolve().parent
def analyze(path):
 a=np.loadtxt(path,skiprows=1);assert np.isfinite(a).all()
 f=a[:,0];L=a[:,1]+1j*a[:,2];gain=20*np.log10(abs(L));phase=np.rad2deg(np.unwrap(np.angle(L)))
 # Return-ratio negative feedback is positive at DC, normalise nearest DC phase to zero.
 phase-=360*round(phase[0]/360)
 crossings=[];gm=[]
 for i in np.flatnonzero(gain[:-1]*gain[1:]<0):
  x=-gain[i]/(gain[i+1]-gain[i]);fc=float(np.exp(np.log(f[i])+x*np.log(f[i+1]/f[i])));ph=float(phase[i]+x*(phase[i+1]-phase[i]));crossings.append({'frequency_Hz':fc,'phase_deg':ph,'PM_deg':180+ph,'direction':'down' if gain[i+1]<gain[i] else 'up'})
 for target in range(-900,541,360):
  for i in np.flatnonzero((phase[:-1]-target)*(phase[1:]-target)<0):
   x=(target-phase[i])/(phase[i+1]-phase[i]);gm.append({'frequency_Hz':float(np.exp(np.log(f[i])+x*np.log(f[i+1]/f[i]))),'phase_deg':target,'GM_dB':float(-(gain[i]+x*(gain[i+1]-gain[i])))})
 simple=len(crossings)==1 and crossings[0]['direction']=='down'
 return {'case':path.parent.name,'frequency_span_Hz':[float(f[0]),float(f[-1])],'dc_gain_dB':float(gain[0]),'all_unity_crossings':crossings,'all_negative_real_crossings':gm,'PM_60_nominal_screen':('PASS' if crossings[0]['PM_deg']>=60 else 'FAIL') if simple else 'UNQUALIFIED_MULTICROSSING','bias_status':'requires transient settled operating-point validation; AC exit0 alone does not qualify','GM_10_screen':'FINITE_CROSSINGS_PASS' if gm and min(x['GM_dB'] for x in gm)>=10 else ('FAIL' if gm else 'NO_CROSSOVER_WITHIN_BAND'),'GM_without_crossing':'no finite phase crossover within span; not a global infinite-GM claim','injection_scope':'series voltage at high impedance inverting input, L=-V(fb)/V(minus); other sources AC0; single loop, not full coupled proof'}
if __name__=='__main__':
 rows=[analyze(p) for p in sorted((ROOT/'results').glob('loop*/loop.txt'))]
 (ROOT/'results/LOOP_METRICS.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');print(json.dumps(rows,indent=2))
