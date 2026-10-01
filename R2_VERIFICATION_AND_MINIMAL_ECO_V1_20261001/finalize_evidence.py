import pathlib,json,csv,hashlib,datetime,importlib.util,os
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']=str(ROOT/'runtime'/'mplconfig')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from analyze_loops import analyze
baseline=ROOT.parent/'FIRST_BUILD_ELECTRICAL_CLOSURE_AND_SCHEMATIC_R2_V1'
spec=importlib.util.spec_from_file_location('legacy_r2',baseline/'spi_state_machine.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
samples=[(s,ch,(32000<<16)|(ch<<12)|(6<<7)) for s in ['BLANK_PRE','ROW0','ROW1','ROW2','ROW3','BLANK_POST'] for ch in range(4)for _ in range(8)]
before=[]
for name,second_id,second_time in [('10s_gap_sequential',2,10110),('10s_gap_jump',100,10110),('10ms_jump',100,120)]:
 v=old.Validity();v.power_good(True,0);v.configure([6]*4,3,100);first=v.complete_frame(110,1,samples);second=v.complete_frame(second_time,second_id,samples)
 before.append({'counterexample':name,'first_valid':first,'second_valid':second,'expected_for_new_contract':False})
(ROOT/'results/LEGACY_COUNTEREXAMPLES.json').write_text(json.dumps({'baseline_sha256':hashlib.sha256((baseline/'spi_state_machine.py').read_bytes()).hexdigest(),'actual_legacy_results':before,'tick_entry_present':hasattr(old.Validity,'tick')},indent=2),encoding='utf-8')
actual=list(csv.DictReader((baseline/'R2_ACTUAL_ALL_534_PINS.csv').open(encoding='utf-8-sig')))
selected=[x for x in actual if x['ref'].startswith(('D_ROW','D_TIA','D_VCM','D_VEX','R_ISO','R_TIA_ISO','R_J3_5'))]
with(ROOT/'results/FAULT_TOPOLOGY_FROM_FROZEN_R2.csv').open('w',encoding='utf-8',newline='')as f:
 w=csv.DictWriter(f,fieldnames=list(actual[0]));w.writeheader();w.writerows(selected)
rows=[analyze(p) for p in sorted((ROOT/'results').glob('loop*/loop.txt'))]
(ROOT/'results/LOOP_METRICS.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
executions=[]
for p in sorted((ROOT/'results').glob('*/execution.json')):
 d=json.loads(p.read_text());executions.append({'case':p.parent.name,'category':d['category'],'qualification':d.get('qualification',False),'exit_code':d.get('exit_code','unknown'),'elapsed_seconds':d.get('elapsed_seconds',d.get('actual_wall_minutes',0)*60),'input_sha256':d.get('input_sha256',hashlib.sha256((ROOT/'cases'/f'{p.parent.name}.cir').read_bytes()).hexdigest()),'scope':'full details and logs in results/'+p.parent.name})
with(ROOT/'CASE_EXECUTION_INDEX.csv').open('w',encoding='utf-8',newline='')as f:
 w=csv.DictWriter(f,fieldnames=list(executions[0]));w.writeheader();w.writerows(executions)
errors=[
 ('fixed_calibration_line_contact_G',.108707,'percent_G','Frozen R2 finite six-pattern/selected vectors, two contacts +.1ohm','BOUNDED_ANALYTICAL_INPUT'),
 ('fixed_static_INL_G',.206068/(1-.206068/100),'percent_G','Conservative conversion from0.206068% resistance bound; same-input blank correlation','BOUNDED_ANALYTICAL_INPUT'),
 ('two_state_residual_D',200e-6/(.25*4990/8000)*100,'percent_G','If both states<=100uV then differential<=200uV; coupled premise UNPROVEN','CONDITIONAL_BOUND'),
 ('calibration_standard',None,'percent_G','Exact standards uncertainty and temperature evidence required','HOLD'),
 ('offset_and_bias_drift',None,'percent_G','Need actual stable coupled operating points and guaranteed family limits','HOLD'),
 ('Rf_excitation_reference_drift',None,'percent_G','Need temp/aging/bias conditions and fixed calibration constants','HOLD'),
 ('ADC_quantization',None,'percent_G','78.125uV/LSB for5.12V span; signal/code dependence not folded into INL again','HOLD'),
 ('frame_noise_repeatability',None,'std_percent_G','Separate stochastic quantity; synthetic averaging is not measured<=.2%','HOLD')]
with(ROOT/'UNIFIED_ERROR_BUDGET.csv').open('w',encoding='utf-8',newline='')as f:
 w=csv.writer(f);w.writerow(['term','value','unit','scope','status']);w.writerows(errors)
plots=ROOT/'plots';plots.mkdir(exist_ok=True)
fig,axs=plt.subplots(1,2,figsize=(12,4),constrained_layout=True)
for name,col in [('p0_rc',2),('p0_opa_psa',2)]:
 a=np.loadtxt(ROOT/f'results/{name}/trace.txt',skiprows=1);ax=axs[0 if name=='p0_rc' else 1];ax.plot(a[:,0]*1e6,a[:,1],label='Input');ax.plot(a[:,0]*1e6,a[:,col],label='Output');ax.set(xlabel='Time (us)',ylabel='Voltage (V)',title=name+' qualification');ax.legend();ax.grid(alpha=.3)
fig.savefig(plots/'P0_QUALIFICATION.png',dpi=200);plt.close(fig)
fig,axs=plt.subplots(2,1,figsize=(10,7),constrained_layout=True)
for name in ['loop_common_r0','loop_common_opax388_r1_settled','loop_tia_r1_settled','loop_tia_r2_settled']:
 a=np.loadtxt(ROOT/f'results/{name}/loop.txt',skiprows=1);L=a[:,1]+1j*a[:,2];axs[0].semilogx(a[:,0],20*np.log10(abs(L)),label=name);axs[1].semilogx(a[:,0],np.rad2deg(np.unwrap(np.angle(L))),label=name)
axs[0].axhline(0,color='black',ls=':');axs[1].axhline(-180,color='black',ls=':');axs[0].set(ylabel='Return ratio (dB)',title='Single-loop screens; injection/bias/coupled qualification remains open');axs[1].set(xlabel='Frequency (Hz)',ylabel='Phase (deg)')
for ax in axs:ax.grid(alpha=.3);ax.legend(fontsize=8)
fig.savefig(plots/'SINGLE_LOOP_SCREENS.png',dpi=200);plt.close(fig)
a=np.loadtxt(ROOT/'results/tia_r2_full_state/trace.txt',skiprows=1);metric=json.loads((ROOT/'results/TIA_R2_FULL_STATE_METRICS.json').read_text());fig,axs=plt.subplots(2,1,figsize=(10,6),constrained_layout=True);axs[0].plot(a[:,0]*1e6,a[:,5],label='ADC input');axs[0].set(ylabel='Voltage (V)',title='22pF local HF feedback: single TIA at ideal VCM, not coupled proof');axs[1].plot(a[:,0]*1e6,(a[:,5]-metric['reference_V'])*1e6);axs[1].scatter(metric['edges_us'],np.array(metric['residual_V'])*1e6,s=10,label='32 valid CS edges');axs[1].axhline(100,color='red',ls=':');axs[1].axhline(-100,color='red',ls=':');axs[1].set(xlim=(450,1400),ylim=(-120,120),xlabel='Time (us)',ylabel='Residual (uV)');axs[1].legend()
for ax in axs:ax.grid(alpha=.3)
fig.savefig(plots/'SINGLE_TIA_VALID_EDGES.png',dpi=200);plt.close(fig)
b=json.loads((ROOT/'EXECUTION_BUDGET.json').read_text());b['counts']['DC']=40;b['counts']['fault_cases']=2;b['DC_split']={'explicit_macro_operating_points':8,'analytical_reset_corners':32};b['fault_split']={'analytical_positive_negative_reset':2,'macro_fault':0};b['finished_scientific_work_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();b['scientific_elapsed_wall_minutes']=(datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(b['started_utc'])).total_seconds()/60;b['time_notes']='Wall time conservatively logged; P0~8.4min, P1~26.1min including preliminary small model set; P2 stop~2.5min after formal entry plus earlier model time already charged toP1; no claim240min used';(ROOT/'EXECUTION_BUDGET.json').write_text(json.dumps(b,indent=2),encoding='utf-8')
print(json.dumps({'execution_files':len(executions),'ledger_counts':b['counts'],'plots':3,'scientific_elapsed_wall_minutes':b['scientific_elapsed_wall_minutes']}))
