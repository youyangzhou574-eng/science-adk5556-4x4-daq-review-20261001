import pathlib,json,csv,itertools,hashlib,unittest,numpy as np
from analytical_validation import adc_residual,protected_cf_current_bound
p=pathlib.Path(__file__).resolve().parent
E=.25;RF=4990.;VCM=2.5
calls=0
def solve(R,lead,row):
 global calls;calls+=1
 R=np.asarray(R,float);lead=np.array(lead,float);src=np.full(8,VCM);src[row]-=E
 A=np.zeros((8,8));b=np.zeros(8)
 for i in range(4):
  for j in range(4):
   g=1/R[i,j];k=4+j;A[i,i]+=g;A[k,k]+=g;A[i,k]-=g;A[k,i]-=g
 fixed=np.where(lead==0)[0];free=np.where(lead>0)[0];v=src.copy()
 for k in free:A[k,k]+=1/lead[k];b[k]+=src[k]/lead[k]
 if len(free):v[free]=np.linalg.solve(A[np.ix_(free,free)],b[free]-A[np.ix_(free,fixed)]@v[fixed])
 sensor=(v[4:][None,:]-v[:4,None])/R
 col=sensor.sum(axis=0);sink=sensor.sum(axis=1)
 return {'D':RF*col,'row_preiso':src[:4]-1000*sink,'tia_tap':VCM+RF*col,'tia_preiso':VCM+(RF+1000)*col,'sensor':sensor,'v':v}
def signals(R,lead):return np.array([solve(R,lead,i)['D']for i in range(4)])
# Calibration computed exactly once, never per validation pattern or lead vector.
cal_lead=np.full(8,.05)
D1=signals(np.full((4,4),1000.),cal_lead);D2=signals(np.full((4,4),6800.),cal_lead)
a=(D1-D2)/(1/1000-1/6800);b=D1-a/1000
(p/'FIXED_CALIBRATION.json').write_text(json.dumps({'standards_ohm':[1000,6800],'calibration_leads_ohm':cal_lead.tolist(),'a':a.tolist(),'b':b.tolist(),'immutable_for_all_cases':True,'exact_calibration':True},indent=2)+'\n')
patterns={'all800':np.full((4,4),800.),'all8000':np.full((4,4),8000.),'all3300':np.full((4,4),3300.),'checker':np.where(np.indices((4,4)).sum(axis=0)%2,800,8000).astype(float),'high_corner':np.full((4,4),800.),'low_corner':np.full((4,4),8000.)}
patterns['high_corner'][0,0]=8000;patterns['low_corner'][0,0]=800
leads={'zero':np.zeros(8),'calibration_unchanged':cal_lead,'asym_within_0p1':np.array([0,.02,.05,.1,.1,.06,.03,0]),'asym_reverse':np.array([.1,.06,.03,0,0,.02,.05,.1]),'postcal_contact_plus0p1':cal_lead+np.array([.1,0,0,0,0,0,0,.1]),'asym1ohm_stress':np.array([1,.6,.3,0,0,.2,.5,1]),'postcal_contact_plus1':cal_lead+np.array([1,0,0,0,0,0,0,1])}
dc=[];headroom=[]
for ln,lead in leads.items():
 for pn,R in patterns.items():
  z=[solve(R,lead,i)for i in range(4)];D=np.array([x['D']for x in z]);ghat=(D-b)/a;gerr=ghat*R-1;rh=1/ghat
  dc.append({'case':len(dc)+1,'pattern':pn,'wire_condition':ln,'leads_ohm':lead.tolist(),'R_ohm':R.tolist(),'D_V':D.tolist(),'Rhat_ohm':rh.tolist(),'max_G_error_pct':float(abs(gerr).max()*100),'max_R_error_pct':float(abs(rh/R-1).max()*100),'wire_budget_0p20_G_pct_pass':bool(abs(gerr).max()<=.002)})
  if ln=='zero':
   headroom.append({'pattern':pn,'row_output_min_V':float(min(x['row_preiso'].min()for x in z)),'TIA_tap_max_V':float(max(x['tia_tap'].max()for x in z)),'TIA_preiso_max_V':float(max(x['tia_preiso'].max()for x in z)),'against_4p75_rail_margin_V':float(4.75-max(x['tia_preiso'].max()for x in z)),'classification':'IDEAL_DC_HEADROOM_ONLY_NOT_OUTPUT_SWING_MACRO'})
# Shared blank ADC INL error is subtracted as one correlated quantity, not four independent noise sources.
# ADC +/-2 LSB INL. Default +/-10.24V span has 312.5uV/code.
# Sensitivity only: within phase shared blank; cross-phase independent errors require additional drift/nonstationarity, not fixed INL alone.
# Static-curve same-input correlation is separately evaluated in ADC_STATIC_CURVE_FIXED_CAL_RESULTS.
inl=[]
ideal1=RF*E/1000;ideal2=RF*E/6800
for range_name,span in [('V1_default_bipolar10p24',20.48),('R2_unipolar5p12',5.12)]:
 bound=2*span/65536
 for e1,e2,et,ebcal,ebtest in itertools.product([-bound,bound],repeat=5):
  d1=ideal1+e1-ebcal;d2=ideal2+e2-ebcal
  ac=(d1-d2)/(1/1000-1/6800);bc=d1-ac/1000
  for R in [800.,8000.]:
   rh=ac/(RF*E/R+et-ebtest-bc)
   inl.append({'range':range_name,'R':R,'cal1_inl_V':e1,'cal2_inl_V':e2,'target_inl_V':et,'cal_shared_blank_inl_V':ebcal,'test_shared_blank_inl_V':ebtest,'R_error_pct':100*(rh/R-1),'shared_blank_correlation':'one per phase, not independent per column','classification':'CONSERVATIVE_CROSS_PHASE_BLANK_CHANGE_SENSITIVITY_NOT_STATIC_INL'})
assert max(abs(x['R_error_pct'])for x in inl if x['range']=='V1_default_bipolar10p24')>1
assert max(abs(x['R_error_pct'])for x in inl if x['range']=='R2_unipolar5p12')<.5
row=[]
for design,rb,ch in [('V1_REJECTED',10000,1e-9),('R2_CANDIDATE',4990,100e-12)]:
 for R in [800.,8000.]:
  for CL in [0,100e-12,1e-9]:
   for t in [200e-6,300e-6]:
    res=adc_residual(rs=1000,rb=rb,ch=ch,conductance=4/R,line_cap=CL,sample_time=t)
    row.append({'design':design,'equal_cells_R':R,'line_C_F':CL,'sample_time_s':t,'ADC_residual_V':res,'ideal_100uV_pass':res<=100e-6,'model':'ideal amplifier exact rational row + ideal TIA + ADC RC; not macro transient'})
# Supervisor threshold all explicit tolerance vertices and SENSE bias signs.
mon=[]
for rail,rt,RtTol in [('V5',32000,.001*30000+.01*2000),('V3V3',16990,.001*14990+.01*2000)]:
 bounds=[]
 for st,sb,sref,ib in itertools.product([-1,1],repeat=4):
  top=rt+st*RtTol;bot=10000*(1+sb*.001);vit=1.15*(1+sref*.01)
  threshold=vit*(1+top/bot)+ib*100e-9*top
  bounds.append(threshold)
 mon.append({'rail':rail,'nominal_fall_V':1.15*(1+rt/10000),'min_fall_V':min(bounds),'max_fall_V':max(bounds),'conservative_max_release_V':max(bounds)*1.00825,'CT_F':100e-9,'nominal_release_delay_s':.107025,'propagation_delay':'18us nominal at3.3V; no datasheet worst-case bound; hardware10ms remains HOLD'})
faults=[]
for line in range(8):
 for fault in ['GND','5V25','OPEN']:
  faults.append({'case':len(faults)+1,'line':line,'fault':fault,'classification':'STATIC_LIMIT_BOUND_ONLY' if fault!='OPEN' else 'QUALITATIVE_OPEN','max_output_iso_current_mA':5.75/990*1000 if fault!='OPEN'else None,'max_sense_injection_mA':5.75/9990*1000 if line>=4 and fault!='OPEN'else None,'iso_power_W':5.75**2/990 if fault!='OPEN'else None,'CF_edge_energy_nJ':.5*2.31e-9*5.75**2*1e9 if line>=4 and fault!='OPEN'else None,'60s_full_board_thermal':'HOLD','absolute_max_complete':'HOLD'})
for fault in ['ROW_COL_SHORT','CELL_SHORT','CELL_OPEN','V5_FIRST_OFF','V3_FIRST_OFF','BOTH_OFF_EXTERNAL_DIGITAL','SLOW_RAMP','RESET','RESTORE']:
 faults.append({'case':len(faults)+1,'fault':fault,'classification':'MODEL_REQUIRED','result':'FAULT_PROTECTION_HOLD'})
noise={'T_K':303.15,'k':1.380649e-23,'sense_R_ohm':10000,'sense_noise_nV_rtHz':float(np.sqrt(4*1.380649e-23*303.15*10000)*1e9),'column_sense_bias_10nA_bound_uV':100.,'R_error_from_bias_before_cal_at8000_pct':100*100e-6/(RF*E/8000),'standard_error_bound_pct':.05,'precision_calibration_standard_error_verified':False,'integrated_frame_std':'HOLD: no full loop ENBW or ADC stochastic/driver noise model','Rf_TCR_ppm_per_C':25,'deltaT_C':10,'Rf_drift_pct':.025,'excit_reference_change':'HOLD: E actual must be measured/fixed after calibration'}
for name,rows in [('DC_FIXED_CAL_RESULTS',dc),('HEADROOM_RESULTS',headroom),('ADC_INL_FIXED_CAL_RESULTS',inl),('ROW_ANALYTIC_RESULTS',row),('SUPERVISOR_TOLERANCE_RESULTS',mon),('FAULT_CASES',faults)]:
 (p/(name+'.json')).write_text(json.dumps(rows,indent=2)+'\n')
 fields=[k for k,value in rows[0].items()if not isinstance(value,(list,dict))]
 with(p/(name+'.csv')).open('w',encoding='utf-8-sig',newline='')as f:w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
(p/'NOISE_AND_DRIFT_BOUNDS.json').write_text(json.dumps(noise,indent=2)+'\n')
summary={'DC_row_state_solves':calls,'DC_validation_patterns':len(patterns),'DC_validation_wire_vectors':len(leads),'fixed_calibration_groups':1,'row_analytic_cases':len(row),'ADC_INL_vertices_endpoints':len(inl),'fault_static_or_qualitative_cases':len(faults),'AC_macro':0,'normal_transient_macro':0,'fault_transient_macro':0,'within_0p1_wire_G_error_max_pct':max(x['max_G_error_pct']for x in dc if x['wire_condition']in('asym_within_0p1','asym_reverse','calibration_unchanged','zero')),'postcal_plus0p1_G_error_max_pct':max(x['max_G_error_pct']for x in dc if x['wire_condition']=='postcal_contact_plus0p1'),'postcal_plus1_G_error_max_pct':max(x['max_G_error_pct']for x in dc if x['wire_condition']=='postcal_contact_plus1'),'default_ADC_INL_R_error_max_pct':max(abs(x['R_error_pct'])for x in inl if x['range']=='V1_default_bipolar10p24'),'R2_ADC_INL_R_error_max_pct':max(abs(x['R_error_pct'])for x in inl if x['range']=='R2_unipolar5p12'),'R2_300us_residual_max_V':max(x['ADC_residual_V']for x in row if x['design']=='R2_CANDIDATE'and x['sample_time_s']==300e-6),'native_proceed_gate':'ADC range0-5.12V and range readback required; known topology corrected; dynamic/thermal/capacity remain HOLD'}
assert calls<=256
(p/'OFFLINE_VALIDATION_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
