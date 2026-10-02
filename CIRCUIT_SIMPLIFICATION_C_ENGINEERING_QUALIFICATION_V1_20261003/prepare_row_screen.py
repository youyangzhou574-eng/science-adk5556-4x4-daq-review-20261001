import pathlib, json, hashlib, shutil, datetime
P=pathlib.Path(__file__).resolve().parent
OLD=P.parent/'R21_ENGINEERING_R21_NATIVE_AND_LIMITED_VALIDATION_V1'
(P/'models').mkdir(exist_ok=True)
manifest=[]
for name in ['OPAx388.LIB','OPA4388_ORIGINAL.LIB']:
    source=OLD/'models'/name
    shutil.copyfile(source,P/'models'/name)
    manifest.append({'file':name,'source':str(source),'SHA256':hashlib.sha256(source.read_bytes()).hexdigest(),'edited':False})
(P/'MODEL_SOURCE_SHA.json').write_text(json.dumps(manifest,indent=2),'utf8')
code='''C first Type III selected-row screening, not full matrix qualification
.include "../../models/OPAx388.LIB"
V5 v5 0 5
VCM vcm 0 2.5
VEX vex 0 2.25
XROW vex fb v5 0 out OPAx388
.model MUX SW(Ron=4.9 Roff=1e12 Vt=.5 Vh=.1)
VSEL sel 0 1
SD out row sel 0 MUX
SS row fb sel 0 MUX
R00 row vcm 800
R01 row vcm 800
R02 row vcm 800
R03 row vcm 800
CLROW row 0 1n
.options method=gear
.control
set wr_singlescale
set wr_vecnames
set numdgt=15
op
wrdata op.txt v(row) v(fb) v(out) i(VCM)
quit
.endc
.end
'''
folder=P/'cases'/'row800_selected_op';folder.mkdir(parents=True,exist_ok=True)
(folder/'case.cir').write_text(code,'utf8')
(folder/'ASSUMPTIONS.json').write_text(json.dumps({'screenOnly':True,'fixedVCM':2.5,'fixedVEXC':2.25,'parallelElements':4,'sensorOhm':800,'switchModel':'ideal SW + max Ron4.9ohm and assumed Roff1e12, not a qualified TMUX model','rowCapacitance_F':1e-9,'rowCapacitanceMeasured':False,'fullMatrix':False,'TIAMacros':0,'REF3025Macro':0,'adcMacro':0,'blankIncluded':False},indent=2),'utf8')
b=json.loads((P/'EXECUTION_BUDGET.json').read_text('utf-8-sig'))
b['actual']['newSources']=3;b['actual']['protectionCandidates']=1
b['phase']='C2_EARLY_ROW_SCREEN';b['phaseStartedUTC']=datetime.datetime.now(datetime.timezone.utc).isoformat()
b['C0Reception']='3 new datasheets received; Ceff and low-VIN reset remain HOLD; no full C certificate'
b['operations']=[{'kind':'newSources','count':3,'label':'TMUX1109 / LP5912 / BAT54XY','accounting':'recorded at reception; no solver or CAD preceded its precharge'}]
(P/'EXECUTION_BUDGET.json').write_text(json.dumps(b,indent=2),'utf8')
print('prepared one OP case, unedited models copied, scientific launch=0')
