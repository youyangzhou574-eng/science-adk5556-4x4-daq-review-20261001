from pathlib import Path
import csv,json,datetime,hashlib,re,zipfile
p=Path(__file__).parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
b=json.loads((p/'EXECUTION_BUDGET.json').read_text(encoding='utf-8'))
assert not b['STOP'] and b['spent']['OP_AC_PZ']+10<=b['limits']['OP_AC_PZ']
b['spent']['OP_AC_PZ']+=10
b['events'].append({'utc':now,'cost':{'OP_AC_PZ':10},'purpose':'Conservative precharge ten scalar analytic DC endpoints; not ngspice OP/AC/PZ launches','prechargedBeforeCalculation':True})
(p/'EXECUTION_BUDGET.json').write_text(json.dumps(b,indent=2),encoding='utf-8')
def bound(vmin,vmax,topmin,topmax,botmin,botmax,leak):
 return (vmin*(1+topmin/botmax)-leak*topmax,vmax*(1+topmax/botmin)+leak*topmax)
ov=bound(1.183,1.223,34800*.999,34800*1.001,10000*.999,10000*1.001,1e-7)
ldo=bound(1.204*.99,1.204*1.01,52300*.999,52300*1.001,30100*.999,30100*1.001,0)
v5=bound(1.15*.99,1.15*1.01,24000*.999,24000*1.001,7500*.999,7500*1.001,1e-7)
toplow=10000*.999+4990*.999+2000*.99;tophigh=10000*1.001+4990*1.001+2000*1.01
v3=bound(1.15*.99,1.15*1.01,toplow,tophigh,10000*.999,10000*1.001,1e-7)
offnom=6*3.3/(4990/100+6);offmax=6*3.6/(4990*.999/101+6)
rows=[]
for name,x in [('U9_OVLO_V',ov),('U8_FB_RESISTOR_CONDITIONAL_V',ldo),('U11_FALLING_V',v5),('U12_ACTUAL_16K99_FALLING_V',v3),('OFF_SIX_PATH_V',(offnom,offmax))]:
 for label,val in zip(['low_or_nominal','high'],x):rows.append({'analysis':name,'endpoint':label,'value_V':val,'method':'scalar analytic; no device transient model','qualification':'HOLD / conditional assumptions'})
with (p/'ANALYTIC_POWER_BOUND_ENDPOINTS.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(p/'ANALYTIC_POWER_BOUND_ASSUMPTIONS.md').write_text('''# Conditional power bounds — not SPICE or bench
10 analytic endpoints are conservatively charged to OP/AC/PZ allowance; actual solver launches remain 0. No transient curves were synthesized.
U9 threshold 1.183–1.223V, external resistors ±0.1%, sense leak ±0.1uA. U11/U12 use 1.15V ±1% and ±0.1uA leak, actual component tolerances; temperature drift of external R is not additionally enveloped here. U12 actual top is 10k+4.99k+1k+1k, nominal 16.99k, not an exact17k.
U8 envelope uses 1.204V±1% and external±0.1%; it is a conditional resistor/reference envelope, not a comprehensive output/load/bias/startup qualification. It does not re-add input-bias to an overall accuracy spec. External temperature/load conditions remain HOLD.
OFF endpoints: six paths, each4.99k to a positive external source, 100R bleed; ignore diode VF and all board loads to bound steady-state upward. Nominal sources3.3V/nominal R; second point explicitly assumes sources≤3.6V, Rseries−0.1% and bleed+1%. This source ceiling is an analytic assumption, NOT a newly approved interface contract. NRST external push-pull-high excluded: external NRST must OD/Hi-Z. This is not a waveform, fault-latency, reverse-current, negative-fault, or all-temperature PASS.
TPS7A37 reverse protection requires EN low before VIN removal. Adjustable FB>VIN+1V is another reverse-current condition; fixed-version typical0.1uA is not an adjustable guaranteed maximum. TPS3890 tPD values are typical, not guaranteed all-condition maximum. Fast5V loss, diode NRST VOL/temperature and EN ordering remain HOLD. No model editing/retries.
''',encoding='utf-8')
base=json.loads((p/'BASELINE_PARTS_AND_NETS.json').read_text(encoding='utf-8'));act=json.loads((p/'C_ACTUAL_PARTS_AND_NETS.json').read_text(encoding='utf-8'));plan=json.loads((p/'C_NATIVE_BUILD_PLAN.json').read_text(encoding='utf-8'))
old={q['ref']:q for pg in base['pages'] for q in pg['parts']};new={q['ref']:q for pg in act['pages'] for q in pg['parts']};expected={q['ref']:q for q in plan['parts']}
dr=[];pr=[]
for ref in sorted(set(old)|set(new)):
 o=old.get(ref);n=new.get(ref);status='ADDED' if o is None else 'REMOVED' if n is None else 'RETAINED_OR_CHANGED'
 dr.append({'ref':ref,'status':status,'oldName':o['name'] if o else '', 'actualName':n['name'] if n else '', 'DNP':expected.get(ref,{}).get('dnp',False),'role':expected.get(ref,{}).get('role','')})
 for num in sorted(set(x['number'] for x in o['pins']) if o else set() | set()):pass
 pins=(set(x['number'] for x in o['pins']) if o else set())|(set(x['number']for x in n['pins'])if n else set())
 for num in sorted(pins):
  k=ref+'-'+num;before=base['pinNetMap'].get(k);after=act['pinNetMap'].get(k)
  pr.append({'ref':ref,'pin':num,'oldNet':before or '', 'actualNet':after or '', 'change':status if not(o and n)else('NET_CHANGED' if before!=after else 'NET_RETAINED')})
for name,rs in [('C_DESIGNATOR_DIFF.csv',dr),('C_ALL_PIN_NET_DIFF.csv',pr)]:
 with(p/name).open('w',encoding='utf-8',newline='')as f:w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
with zipfile.ZipFile(p/'C_SCHEMATIC_CANDIDATE_LEGACY_PCB_NOT_FOR_USE.epro2')as z:
 for name in z.namelist():
  if name.endswith('.epru'):
   data=z.read(name);(p/'C_NATIVE_EXPORTED_PROJECT_SOURCE.epru').write_bytes(data)
(p/'PDF_VISUAL_INSPECTION.md').write_text('''# Six actual PDF pages inspected once
All six Poppler PNG renders viewed. Native PDF has named ports with short wires and sparse four-column grids; it is an electrical candidate/net-audit drawing, NOT a polished functional schematic or PCB distribution image. Page1/2/5/6 top items have little page-edge margin; sparse large pages and small text require zoom. These are real export limitations, not a claim of final drawing acceptance. No second PDF or native edits under spent quota. Every pin has a readable CSV companion C_ACTUAL_ALL_PINS.csv; actual net source and material dictionary retained. Full native retains legacy PCB that must not be used for C. Render-only initial fitz import failed (package absent), wrapper Poppler path failed, actual bundled executable succeeded; no installation. All six images are the successful native PDF renders, not generated replacements.
''',encoding='utf-8')
(p/'PRIMARY_SOURCE_NOTES.md').write_text('''# Primary sources and exact limits
New sources2/4: [TPS7A37 SBVS220B](https://www.ti.com/lit/ds/symlink/tps7a37.pdf), [STM32G031 DS12992](https://www.st.com/resource/en/datasheet/stm32g031k8.pdf). Reused sources: [TPS3890](https://www.ti.com/lit/ds/symlink/tps3890.pdf), [TMUX1109](https://www.ti.com/lit/ds/symlink/tmux1109.pdf), [BAT54XY](https://assets.nexperia.com/documents/data-sheet/BAT54XY.pdf), [LM73100](https://www.ti.com/lit/ds/symlink/lm73100.pdf). Official source URLs are references, not chatgpt-content-reference placeholders; bulk third-party documents excluded.
TPS7A3701 WSON EP grounded; output≥1uF with low-ESR ringing condition COUT×ESR<50nΩ-F requires real rail/load assessment. ENlow≤.5/high≥1.7; EN low before VIN removed for reverse protection; adjustable FB condition and fixed-version typical leakage are distinct. LDO output3.296V is nominal only.
TPS3890 valid VDD1.5–5.5V; RESET POR only at specified conditions, belowPOR undefined. tPD18us@3.3/8us@5.5 typical, not guaranteed full-envelope maximum. CT100nF implies nominal107ms+25us, not107us. NRST logicVILmax0.3VDD/VIHmin0.7VDD from STM32 datasheet; firmware Hi-Z/reset/init timing not bench qualified.
TMUX1109 active-high EN and actual16pin map used. BAT54XY isolated series pairs1→6→2 and4→3→5 used; diode propagation needs VOL/temperature/delay validation. TPD4E05U06 is ESD, not3.3V DC rail clamp or arbitrary continuous wrong-wire protection. No generalized stable/full-matrix/100fps claim.
''',encoding='utf-8')
g={'C_SCHEMATIC_WORKING_CANDIDATE_CREATED':True,'ACTUAL_PIN_PLAN_MATCH':True,'ACTUAL_BOM_COUNTS_CONFIRMED':True,'C_SCHEMATIC_ACCEPTED':False,'C_POWER_SEQUENCE_QUALIFIED':False,'DNP_RECOVERY_NETWORK_QUALIFIED':False,'COLD_AUDIT_PASS':False,'ERC_DETAIL_PASS':False,'DRAWING_STANDALONE_RELEASE':False,'CAD_RELEASED':False,'SPICE_RELEASED':False,'PCB_RELEASED':False,'BENCH_RELEASED':False,'MANUFACTURE_RELEASED':False,'STOP':'C_POWER_DNP_MATERIAL_AND_DRAWING_REVIEW_HOLD_NATIVE_SAVE_SESSION_QUOTAS_SPENT','holds':['POWER_EN_SEQUENCE_AND_DIODE_RESET_HOLD','DNP_RECOVERABLE_POSITION_HOLD','U12_EXACT_MPN_HOLD','VEX_DIVIDER_THEVENIN_CHANGE_HOLD','TPD_MANUFACTURER_TEMPLATE_HOLD','COLD_AUDIT_HOLD','ERC_DETAIL_HOLD','DRAWING_READABILITY_HOLD','FULL_MATRIX_DYNAMIC_PERFORMANCE_HOLD','MLCC_CEFF_HOLD','FFC_MECHANICAL_HOLD','BENCH_NOT_RELEASED']}
(p/'GATES.json').write_text(json.dumps(g,indent=2),encoding='utf-8')
b['STOP']=True;b['STOPUTC']=datetime.datetime.now(datetime.timezone.utc).isoformat();b['STOPReason']=g['STOP'];b['actualNewSPICEProcesses']=0;b['analyticDCScalarEndpoints']=10;b['nativeIndependentCold']=0
(p/'EXECUTION_BUDGET.json').write_text(json.dumps(b,indent=2),encoding='utf-8')
receipt='''# C power / native schematic closeout — complete candidate review receipt, HOLD
This is a real six-page working schematic, not an accepted circuit, new PCB, or performance PASS. Prior source/failure packages remain frozen. Sole new Pro ruling7492ccc0 / parent2d7fdffa grants300min C only. TPS7A3701 replaces LP5912, U9/U11/U12 direction retained; no A or solver/tool study.

## Actual implementation
115 structural components; actual native Add-into-BOM flags103yes/12no. Populated:39R/44C/6protection packages/10IC/4J. Compared with old176 this is73 fewer populated parts (~41.5%), NOT the Pro provisional88–94 and NOT an actual83-part BOM. 12NC DNP references are physically unqualified placeholders. Actual391pins:327connected/57nets/64NC; all391 match explicit candidate plan, no duplicate membership. Matching a plan does not establish functional correctness or approve amendments.
Shared OPA388 ROW+dual4:1 TMUX1109 remote feedback, four direct TIAs, direct REF3025 VCM/VEX divider, MCU GPIO defaults, TPS7A3701 52.3k/30.1k and retained bulk/reference caps. U9 actual34.8k/10k OVLO; U11 actual24k/7.5k; six external4.99k, NRST1k, four dual Schottky packages and100R bleed retained. J2 eight-line FFC mapping remains1–4ROW0..3/5–8COL0..3; inherited PCB footprint not inspected/qualified here.

## Concrete exceptions for engineering decision
1. U11 VDD/MR=V5, outputPWR5_OK pulls LDO EN via100k→V5. U12 outputPGOOD→MCUNRST. Spare BAT54 upper branch PGOOD→PWR5_OK propagates power-bad without5V MCU pullup. This is a candidate amendment to literal common wired-AND, NOT approved fast EN-before-VIN guarantee. Reverse sequence, diodeVOL/temp and NRST→GPIOHiZ→MUXOFF latency HOLD. TPS7A37 adjustable reverse condition is conditional; fixed-version typical0.1uA cannot be called guaranteed adjustable leakage.
2. U12 exact17k0.1% unavailable: actual old16.99k series chain retained (10k/4.99k .1% +two1k1%). Nominal3.10385V; accurate chain MPN/tolerance shown, not fake17k.
3. VEX uses catalog18k/162k ratio. Nominal2.25 preserved, Thevenin rises9k→16.2k. Loading/startup not qualified.
4. Twelve compensation references are NC on both pins and DNP. This does NOT meet functional recoverable compensation positions; restoring requires an explicit net/PCB-option ECO. Candidate direct TIA not qualified delete of those12.
5. TPD C125795 supplier template actual10pin/footprint verified electrically against plan; manufacturer field missing. TI-stock identity/material qualification HOLD. J1/J3/J4 mating and FFC mechanical qualification remain unknown.
6. All ADC doublebulk/refcaps retained; Ceff and startup/load not measured. No forced deletion tohit90. Actual native export includes legacy176PCB, explicitly LEGACY_PCB_NOT_FOR_USE; no CPCB generated or synced.

## Verification actually performed
Warm actualFile pin-set/net/value/DNP audit391/391; raw actual native BOM flags103yes12no. Old private source SHA unchanged; both own headless sessions officialclosed. Save6/6 true; first session unsaved build timeout discarded. Imported16char internal ID was unsuitable creation ID; corrected using existing32char catalog records, guard RED→4GREEN; failed code/logs retained, no API research or installation. Second session built six pages with actual IDs/pins and all saves.
ERC1 gives warncount772 only, no body: ERC_DETAIL_HOLD. PDF1 succeeded, six actual pages rendered/viewed; sparse port-based drawing and small labels/page-edge margins remain drawing HOLD, not polished final. No independent cold (two-session quota spent). Native688033bytes/PDF405178bytes decoded and hashed; native zip has no accountSQLite/password/access_token/refresh_token fields found. Entire private.eprj2 excluded from publication.
Finite electrical:10 scalar analytic endpoints conservatively charged OP/AC/PZ budget; actual SPICE0, TRAN0. CSV contains conditional thresholds/OFF steady-state bounds and explicit assumptions. No synthetic transient/full-matrix curves. Existing full16R NUMERICAL_UNRESOLVED and oldPZ_INVALID_PORT_SETUP persist; no fourthOP/PZ retry. Startup/brownout/fastbackfeed and system accuracy/noise100fps remain HOLD.

## Budget / STOP / delivery
sources2/4 candidate1/2 copy1/1 session2/2 save6/6 capture2/6 audit1/4 ERC1/2 PDF1/1; conservative analyses10/16 allanalytic, actualSPICE0, TRAN0/4. Placement/PCB/routing/pour/Gerber/manufacture/procurement/bench/localGit/system0. Sticky STOP C_POWER_DNP_MATERIAL_AND_DRAWING_REVIEW_HOLD_NATIVE_SAVE_SESSION_QUOTAS_SPENT. No further native edit or solver until full new unified scope. Finish only receipt/review/public delivery, not expand scientific work.
Single fresh-context final review follows; disposition appended without second review, new scientific calculations, or extra native/PDF operations. Full own sources, actualBOM/pins/netdiff/rawnet, actual failure evidence and native/PDF are to be direct-file public attachments plus ZIP/manifest; privacy exclusions explicit. Rulings and costs in PLAN_AND_LEDGER.md are the complete decision register; previous duplicated generator ledger lines are historical rerun record, not extra authorizations.
END-OF-COMPLETE-C-POWER-AND-SCHEMATIC-CANDIDATE-HOLD-RECEIPT
'''
(p/'COMPLETE_C_POWER_RECEIPT.md').write_text(receipt,encoding='utf-8');(p/'README.md').write_text(receipt,encoding='utf-8')
print(json.dumps({'actual103plus12':True,'newSPICE':0,'analyticEndpoints':10,'STOP':b['STOP'],'bounds':{'OV':ov,'LDOconditional':ldo,'V5':v5,'V3':v3,'OFF':[offnom,offmax]}}))
