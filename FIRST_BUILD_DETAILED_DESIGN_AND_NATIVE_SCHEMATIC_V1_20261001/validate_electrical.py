import numpy as np,json,pathlib,csv
p=pathlib.Path(__file__).resolve().parent
E=.25;VCM=2.5;RF=4990.
def solve(R,lead=0.,row=0):
 R=np.asarray(R,dtype=float);assert R.shape==(4,4) and np.all(R>0)
 lead=np.broadcast_to(np.asarray(lead,dtype=float),(8,)).copy();assert np.all(lead>=0)
 src=np.full(8,VCM);src[row]-=E
 A=np.zeros((8,8));b=np.zeros(8)
 for i in range(4):
  for j in range(4):
   g=1/R[i,j];a=i;c=4+j;A[a,a]+=g;A[c,c]+=g;A[a,c]-=g;A[c,a]-=g
 fixed=np.where(lead==0)[0];free=np.where(lead>0)[0]
 v=src.copy()
 if len(free):
  for k in free:A[k,k]+=1/lead[k];b[k]+=src[k]/lead[k]
  v[free]=np.linalg.solve(A[np.ix_(free,free)],b[free]-A[np.ix_(free,fixed)]@v[fixed])
 sensor=(v[4:][None,:]-v[:4,None])/R
 # positive: each column supplies current to lower selected row.
 col=sensor.sum(axis=0);sink=sensor.sum(axis=1)
 return dict(v=v,signal=RF*col,output=VCM+RF*col,row_preiso=src[:4]-1000*sink,row_sink=sink,kcl_sensor=sensor)
checks=[]
def check(name,cond):
 assert cond,name;checks.append(dict(name=name,status='PASS'))
R=np.full((4,4),800.)
z=solve(R,0,2);check('zero_leads_exact_selected_cell_current',np.allclose(z['signal'],RF*E/800,atol=1e-12))
check('row_sink_total',abs(z['row_sink'][2]-.00125)<1e-14)
check('ideal_row_output_headroom',abs(z['row_preiso'][2]-1)<1e-12)
a=solve(R,1,2);check('finite_leads_reduce_signal',np.all(a['signal']<z['signal']))
check('finite_lead_kcl_residual',np.max(np.abs(a['kcl_sensor'].sum(axis=1)-(a['v'][:4]-np.array([2.5,2.5,2.25,2.5]))))<1e-12)
high=R.copy();high[2,1]=8000;zero=solve(high,0,2);check('neighbor_independent_zero_lead',abs(zero['signal'][1]-RF*E/8000)<1e-12)
check('finite_leads_neighbor_dependence',abs(solve(high,1,2)['signal'][1]-solve(np.full((4,4),8000.),1,2)['signal'][1])>1e-7)
def cal(lead):
 s1=np.array([solve(np.full((4,4),1000.),lead,i)['signal']for i in range(4)])
 s2=np.array([solve(np.full((4,4),6800.),lead,i)['signal']for i in range(4)])
 a=(s1-s2)/(1/1000-1/6800);b=s1-a/1000
 return a,b
ca,cb=cal(0);check('conductance_two_point_ideal',np.allclose(ca,RF*E)and np.allclose(cb,0,atol=1e-12))
patterns={'all_low':np.full((4,4),800.),'all_high':np.full((4,4),8000.),'all_mid':np.full((4,4),3300.),'checker':np.where((np.indices((4,4)).sum(axis=0)%2),800.,8000.)}
for val in(1500.,4700.,7000.):patterns['all_'+str(int(val))]=np.full((4,4),val)
for name,base,target in[('high_corner_low_neighbors',800.,8000.),('low_corner_high_neighbors',8000.,800.)]:
 r=np.full((4,4),base);r[0,0]=target;patterns[name]=r
rows=[];details=[]
for lead in(0.,.1,1.):
 ca,cb=cal(lead)
 for supply in(4.75,5.,5.25):
  for name,R in patterns.items():
   sig=np.array([solve(R,lead,i)['signal']for i in range(4)]);rh=ca/(sig-cb);err=rh/R-1
   normal=[solve(R,lead,i)for i in range(4)]
   out=np.concatenate([v['output']for v in normal]);drive=np.concatenate([v['row_preiso']for v in normal])
   row=dict(case_id=len(rows)+1,pattern=name,lead_each_ohm=lead,avdd=supply,calibration='same_lead_all1k_all6k8_fixed_for_all_patterns',max_abs_R_error_pct=float(np.max(np.abs(err))*100),min_tia_output_V=float(out.min()),max_tia_output_V=float(out.max()),min_row_drive_V=float(drive.min()),max_row_drive_V=float(drive.max()),ideal_rail_headroom_only=bool(out.max()<supply and drive.min()>0),wire_allocation_0_2pct=bool(np.max(np.abs(err))<=.002))
   rows.append(row);details.append(dict(**row,R=R.tolist(),D=sig.tolist(),Rhat=rh.tolist(),Rerr=err.tolist()))
with(p/'DC_CASES.csv').open('w',encoding='utf-8-sig',newline='')as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(p/'DC_RESULTS.json').write_text(json.dumps(details,indent=2)+'\n',encoding='utf-8')
fault=[]
for typ in('row_gnd','row_5V25','col_gnd','col_5V25','row_col_short','unit_short','unit_open','electrode_open','MCU_HiZ','digital_first_loss','analog_first_loss','slow_start'):
 for index in (range(4) if typ.startswith(('row_','col_'))and typ!='row_col_short' else [0]):
  fault.append(dict(case_id=len(fault)+1,type=typ,index=index,analysis='static resistor bound or qualitative open/reset/power disposition; not transient/thermal simulation',row_resistor_limit_mA=5.25/990*1000 if typ.startswith('row_')else None,input_sense_resistor_limit_mA=5.25/9990*1000 if typ.startswith('col_')else None,absolute_max_full_board_verified=False,sixty_second_thermal_verified=False,result='FAULT_PROTECTION_HOLD'))
(p/'FAULT_CASES.json').write_text(json.dumps(fault,indent=2)+'\n',encoding='utf-8')
summary=dict(dc_groups=len(rows),dc_selected_row_states=len(rows)*4,dc_cell_readouts=len(rows)*16,patterns=list(patterns),selfchecks=checks,lead_results={str(l):dict(max_R_error_pct=max(r['max_abs_R_error_pct']for r in rows if r['lead_each_ohm']==l),within_wire_alloc_all=all(r['wire_allocation_0_2pct']for r in rows if r['lead_each_ohm']==l))for l in(0.,.1,1.)},fault_static_cases=len(fault),AC_cases=0,transient_cases=0,official_macromodels_downloaded=2,official_macromodel_execution=False,noise_verified=False,PM_GM_verified=False,settling_300us_verified=False,model_limits=['ideal infinite DC opamp gain; no saturation, finite loop gain, input bias, reference variation or clamp dynamics','one lumped resistance per electrode; no distributed resistance/capacitance/contact model','supply cases only verify ideal output-voltage headroom; no power-sequencing model','calibration uses exact mathematical standards; no standard measurement uncertainty/noise included'],result='DC_MODEL_COMPLETED / DYNAMIC_VALIDATION_HOLD / FAULT_PROTECTION_HOLD')
(p/'VALIDATION_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
(p/'VALIDATION_REPORT.md').write_text('# 验证报告\n\n标准库numpy线性DC KCL实际执行，非SPICE全宏模型。'+str(len(rows))+'组，每组4选行/16读数；8类物理自检通过。完整输入/代码/CSV及结果保留。\n\n'+json.dumps(summary['lead_results'],indent=2)+'\n\n校准固定于同线阻的全1k/全6.8k，不按邻点模式重校。零线阻精确，有限线阻的邻点误差见CSV；1Ω敏感性点不是保证的线阻规格。供电角点只计算理想静态余量，不能宣称低压运放能力已模拟。\n\n已下载厂家PSpice/TINA模型，但本机尚未找到可用且已确认兼容的SPICE执行器，不安装第三方、不延续接口排错。实际AC/正常瞬态/故障瞬态均0；PM/GM、300µs建立、噪声、热和掉电验证全部HOLD。不得以模型自检或理想RC公式替代实物。\n\n故障列表含'+str(len(fault))+'项静态/定性审查，无60s实测/热模型。保护尚缺电源排序/联锁/回灌闭合，FAULT_PROTECTION_HOLD，BENCH_NOT_RELEASED。\n',encoding='utf-8')
print(json.dumps(summary,ensure_ascii=True))
