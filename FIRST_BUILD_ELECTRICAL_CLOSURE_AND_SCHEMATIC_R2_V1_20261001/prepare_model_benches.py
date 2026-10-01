import pathlib,json,shutil,hashlib
p=pathlib.Path(__file__).resolve().parent;v=p.parent/'FIRST_BUILD_DETAILED_DESIGN_AND_NATIVE_SCHEMATIC_V1'
b=p/'model_benches';b.mkdir(exist_ok=True)
model=v/'sources/OPA4388_PSPICE.zip.unpacked/OPA4388.LIB';shutil.copyfile(model,b/'OPA4388.LIB')
base='''* R2 complete coupled 4x4 OPA4388 manufacturer-macro testbench, NOT EXECUTED
* ADC/switch/reference/gating/clamp/rail thermal behavior are not represented by this bench.
.LIB "OPA4388.LIB"
V5 v5 0 5
VCM vcm 0 2.5
'''
rows=[]
for i in range(4):
 base+=f'VCMD{i} cmd{i} 0 '+('PULSE(2.5 2.25 1m 10n 10n 2m 4m)' if i==0 else '2.5')+'\n'
 base+=f'XR{i} cmd{i} fb{i} v5 0 drv{i} OPA4388\nRISO{i} drv{i} row{i} 1k\nRFB{i} row{i} fb{i} 4.99k\nCHF{i} drv{i} fb{i} 100p\nCLROW{i} row{i} 0 1n\n'
for j in range(4):
 base+=f'XC{j} vcm sense{j} v5 0 tdrv{j} OPA4388\nRSENSE{j} col{j} sense{j} 10k\nRTOUT{j} tdrv{j} tap{j} 1k\nRF{j} tap{j} col{j} 4.99k\nCF{j} tap{j} col{j} 2.2n\nRADC{j} tap{j} ain{j} 100\nCADC{j} ain{j} 0 10n\nCLCOL{j} col{j} 0 1n\n'
 for i in range(4):base+=f'RARRAY{i}_{j} row{i} col{j} 800\n'
(b/'R2_COUPLED_ALL800_TRAN.cir').write_text(base+'.TRAN 0.1u 5m 0 0.1u\n.PROBE V(row0) V(drv0) V(tap0) V(tdrv0) V(ain0)\n.END\n')
rowloop='''* Row return-ratio probe: amplifier inverting input = fb + AC test.
* Independent sources AC0, keep real loading. L(s)=-V(fb)/V(minus) for injected series source; validate injection algebra against closed loop first.
.LIB "OPA4388.LIB"
V5 v5 0 5
VCMD cmd 0 2.25
VTEST minus fb DC 0 AC 1
XROW cmd minus v5 0 drv OPA4388
RISO drv row 1k
RFB row fb 4.99k
CHF drv fb 100p
RLOAD row vcm 200
VCM vcm 0 2.5
CL row 0 1n
.AC DEC 200 1 100MEG
.PROBE V(fb) V(minus) V(row) V(drv)
.END
'''
(b/'R2_ROW_RETURN_RATIO.cir').write_text(rowloop)
tialoop='''* TIA return-ratio candidate; injection algebra/multi-loop stability must be validated by the executor.
.LIB "OPA4388.LIB"
V5 v5 0 5
VCM vcm 0 2.5
VTEST minus sense DC 0 AC 1
XCOL vcm minus v5 0 drv OPA4388
RISO drv tap 1k
RSENSE col sense 10k
RF tap col 4.99k
CF tap col 2.2n
RARRAY col vcm 200
CL col 0 1n
RADC tap ain 100
CADC ain 0 10n
.AC DEC 200 1 100MEG
.PROBE V(sense) V(minus) V(tap) V(drv)
.END
'''
(b/'R2_TIA_RETURN_RATIO.cir').write_text(tialoop)
(b/'README.md').write_text('''# Manufacturer-model benches — NOT EXECUTED

Retained TI OPA4388 PSpice model (five terminals IN+ IN- VCC VEE OUT), unmodified. P0 did not confirm an installed compatible executor. These files have not been parsed or run by SPICE and are not guaranteed portable. No substitute ideal-opamp simulation is reported as macro-model validation.

The coupled 4×4 all800 bench includes four driven rows, four TIAs, 1k row/TIA isolation, row4.99k/100p, TIA4.99k/2.2n, 10k sense, 100R/10n ADC filters and1n line capacitance. It omits lead resistance; 0–0.1ohm lead sweeps, 8000ohm endpoints, temperature/model corners, VCM/VEXC actual buffers, ADC sampling kickback and reference/current protection models must be added by the eventual executor. It does not model TMUX1134, ADS8684, TPS3890, LM73100 or the installed BAT54S clamps. Therefore it is an amplifier/transient starting bench, not a full protected-board bench.

The two AC benches preserve real feedback loading and introduce one floating series source. With the injected-source equation Vminus=Vfeedback+Vtest, the return ratio is L=-Vfeedback/Vminus in a single-loop interpretation; confirm this against the closed-loop transfer before extracting PM/GM. Report all0dB crossings. Coupled row/VCM/TIA loops require multiloop checks. Nominal PM>=60deg; cornersPM>=45deg andGM>=10dB. These values are acceptance criteria, never results here.

Fault/rail/thermal models are unavailable: use FAULT_CASES.json as a33-case bounded list, not a claim that the listed cases ran. Model ESD clamps do not prove real continuous-fault ratings or PCB thermal safety.
''',encoding='utf-8')
(p/'MODEL_BENCH_MANIFEST.json').write_text(json.dumps({'model_source':str(model),'model_sha256':hashlib.sha256(model.read_bytes()).hexdigest(),'new_model_packages':0,'reused_primary_model_packages':1,'SPICE_runs':0,'executor_confirmed':False,'benches':[f.name for f in b.glob('*.cir')],'model_boundaries':'README.md lists unrepresented complete-board components and required model additions'},indent=2)+'\n')
print(json.dumps({'prepared_benches':3,'SPICE_runs':0}))
