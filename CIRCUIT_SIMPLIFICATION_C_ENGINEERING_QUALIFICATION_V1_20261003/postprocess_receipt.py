"""Read existing evidence only. No solver, CAD, network or budget reset."""
import pathlib,json,re,hashlib,csv,collections,numpy as np
P=pathlib.Path(__file__).resolve().parent
records=[]
for f in sorted((P/'cases').glob('*/RUN.json')):
 r=json.loads(f.read_text('utf8'));folder=f.parent
 log=(folder/'stderr.log').read_text('utf8',errors='replace')
 r['opFileExists']=(folder/'op.txt').exists()
 r['traceFileExists']=(folder/'trace.txt').exists()
 r['acFileExists']=(folder/'ac.txt').exists()
 r['pzAborted']='pz simulation(s) aborted' in log
 r['opAborted']='op simulation(s) aborted' in log
 r['numericalExitIsNotPass']=True
 records.append(r)
(P/'CASE_EXECUTION_INDEX.json').write_text(json.dumps(records,indent=2),'utf8')
with (P/'CASE_EXECUTION_INDEX.csv').open('w',encoding='utf-8-sig',newline='') as f:
 fields=['case','PID','startedUTC','wallSeconds','returncode','opFileExists','traceFileExists','acFileExists','opAborted','pzAborted','forcedStop'];w=csv.DictWriter(f,fields,extrasaction='ignore');w.writeheader();w.writerows(records)
# Preserve real File bytes; the previous .text() rendering is not a raw netlist.
j=json.loads((P/'C_BASELINE_CAPTURE.json').read_text('utf8'))['parsed']['value']
raw=bytes(j['actualFile']['bytes']);(P/'BASELINE_ACTUAL_RAW.net').write_bytes(raw)
try:t=raw.decode('utf-8-sig');enc='UTF8'
except UnicodeDecodeError:t=raw.decode('gb18030');enc='GB18030'
t=t.replace('\r\r\n','\n').replace('\r\n','\n').replace('\r','\n')
pins={};nets={}
for m in re.finditer(r'^\(\s*\n([^\n]+)\n([\s\S]*?)^\)\s*$',t,re.M):
 net=m.group(1).strip();members=[x.split()[0] for x in m.group(2).splitlines() if x.strip()]
 if not members:raise RuntimeError('empty net')
 if net in nets:raise RuntimeError('duplicate net')
 nets[net]=members
 for pin in members:
  if pin in pins:raise RuntimeError('duplicate pin')
  pins[pin]=net
parts=[c for q in j['pages'] for c in q['parts']]
nc={c['ref']+'-'+v['number'] for c in parts for v in c['pins'] if v['nc']}
allpins={c['ref']+'-'+v['number'] for c in parts for v in c['pins']}
audit={'physicalPartCount':len(parts),'schematicPins':len(allpins),'connectedPins':len(pins),'netCount':len(nets),'NCCount':len(nc),'pinsUnaccounted':sorted(allpins-set(pins)-nc),'NCInNet':sorted(nc&set(pins)),'originalFileRawSHA256':hashlib.sha256(raw).hexdigest(),'originalFileBytes':len(raw),'parserEncoding':enc,'CChangesImplemented':0,'J2FootprintObject':next(c['footprint'] for c in parts if c['ref']=='J2'),'J2FootprintNameMatchesFFC':False,'PCBMechanicalPadsCaptured':False,'FileTextReadbackNotRaw':True}
(P/'BASELINE_AUDIT.json').write_text(json.dumps(audit,indent=2),'utf8')
(P/'BASELINE_PARTS_AND_NETS.json').write_text(json.dumps({'pages':[{'page':q['page'],'parts':q['parts'],'nets':q['nets']} for q in j['pages']],'pinNetMap':pins},ensure_ascii=False,indent=2),'utf8')
with(P/'BASELINE_ALL_SCHEMATIC_PINS.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['ref','pin','name','net','NC'])
 for c in parts:
  for v in c['pins']:w.writerow([c['ref'],v['number'],v['name'],pins.get(c['ref']+'-'+v['number'],''),v['nc']])
# Trace conversion retains every sample. Scalars below are readbacks, not new analyses.
summary={}
for case,cols in [('row800_blank_to_enable',['time_s','ROW_V','FB_V','OUT_V','EN']),('tia_step_800_1000_7000_8000',['time_s','COL_V','TIA_V','ADC_IN_V','VEXC_V','sensor_Ohm'])]:
 d=np.loadtxt(P/'cases'/case/'trace.txt',skiprows=1)
 with(P/(case+'_TRACE.csv')).open('w',encoding='utf-8-sig',newline='') as f:w=csv.writer(f);w.writerow(cols);w.writerows(d.tolist())
 if case.startswith('row'):
  mask=d[:,0]>=25.01e-6;err=np.abs(d[:,1]-2.25)/.25;bad=np.where(mask&(err>.01))[0]
  summary['rowScreen']={'static_ROW_V':2.250000185683255,'final_ROW_V':float(d[-1,1]),'last1percentExcursion_s':float(d[bad[-1],0]) if len(bad) else None,'enabledAt_s':25.01e-6,'samples':len(d),'load':'four800ohm to idealVCM, 1nF assumed cable, equivalent switches, 27C'}
 else:
  spans=[(.3e-3,.39e-3,800),(.7e-3,.79e-3,1000),(1.1e-3,1.19e-3,7000),(1.5e-3,1.6e-3,8000)]
  points=[]
  for lo,hi,r in spans:
   z=d[(d[:,0]>=lo)&(d[:,0]<=hi)];expected=2.5+(.25*4990/r);points.append({'Ohm':r,'window_s':[lo,hi],'idealTIA_V':expected,'meanTIA_V':float(z[:,2].mean()),'meanADC_V':float(z[:,3].mean()),'absTIAOffset_V':float(abs(z[:,2].mean()-expected))})
  summary['tiaStepScreen']={'samples':len(d),'points':points,'input':'three ideal unselected row sources, not full shared floating-row matrix','noiseQualification':False}
d=np.loadtxt(P/'cases/tia800_op_ac/ac.txt',skiprows=1)
L=-(d[:,1]+1j*d[:,2])/(d[:,3]+1j*d[:,4]);g=20*np.log10(np.abs(L));ph=np.unwrap(np.angle(L))*180/np.pi
cross=np.where(g[:-1]*g[1:]<0)[0];summary['tiaACScreen']={'method':'scalar series injection at input; T=-Vcol/Vminus; ideal row bounds','crossingLowerSampleApprox':[{'Hz':float(d[i,0]),'phaseMargin_deg':float(180+ph[i])} for i in cross],'globalCertificate':False,'interpolated':False}
with(P/'TIA800_SCALAR_AC_SCREEN.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['Hz','col_real','col_imag','minus_real','minus_imag','out_real','out_imag','returnMagnitude_dB','returnPhase_deg']);w.writerows(np.column_stack([d,g,ph]).tolist())
(P/'LIMITED_SCREEN_SUMMARY.json').write_text(json.dumps(summary,indent=2),'utf8')
# Verify old inputs and both copied macro files; no rewrite or rerun of old packages.
old=[P.parent/'R21_J2_FFC_FINAL_NATIVE_AND_GUI_COLD_CLOSURE_V1'/'SCIENCE_ADK5556_4X4_R21_J2_FFC_FINAL.eprj2',P.parent/'R21_ENGINEERING_R21_NATIVE_AND_LIMITED_VALIDATION_V1'/'models'/'OPA4388_ORIGINAL.LIB',P.parent/'R21_ENGINEERING_R21_NATIVE_AND_LIMITED_VALIDATION_V1'/'models'/'OPAx388.LIB']
sha=[{'path':str(f),'SHA256':hashlib.sha256(f.read_bytes()).hexdigest(),'modifiedByThisPackage':False} for f in old]
(P/'FROZEN_INPUT_CURRENT_SHA.json').write_text(json.dumps(sha,indent=2),'utf8')
print(json.dumps({'baseline':audit,'cases':len(records),'OP':len(records),'AC':1,'PZ':1,'TRAN':2,'fullMatrixOPsAborted':sum(x['opAborted'] for x in records),'screens':summary},ensure_ascii=True))
