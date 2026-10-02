from pathlib import Path
import json,copy,csv
p=Path(__file__).parent
base=json.loads((p/'BASELINE_PARTS_AND_NETS.json').read_text(encoding='utf-8'))
parts={q['ref']:dict(q,page=pg['page']['index']) for pg in base['pages'] for q in pg['parts']}
oldlib=json.loads((p/'C_LIBRARY_CANDIDATES.json').read_text(encoding='utf-8'))
newlib=json.loads((p/'POWER_CONTEXT_INVOKE.json').read_text(encoding='utf-8'))['parsed']['value']
extra=json.loads((p/'EXACT_MATERIALS.json').read_text(encoding='utf-8'))['parsed']['value']['searches']
lib={**{k:v[0] for k,v in oldlib.items() if v},**{k:v[0]for k,v in newlib['searches'].items()if v},**{v[0]['manufacturerId']:v[0]for v in extra.values()if v}}
output=[]
def original(ref,nets=None,page=None,value=None,dnp=False):
 q=copy.deepcopy(parts[ref]);q['nets']=nets if nets is not None else {x['number']:base['pinNetMap'].get(ref+'-'+x['number'])for x in q['pins']};q['page']=q['page']if page is None else page;q['value']=value or q['name'];q['dnp']=dnp;output.append(q);return q
def new(ref,mpn,nets,page,value=None,role=''):
 m=lib[mpn];q={'ref':ref,'page':page,'value':value or mpn,'dnp':False,'association':{'libraryUuid':m['libraryUuid'],'uuid':m['uuid']},'sub':m.get('symbolName',mpn)+'.1','name':mpn,'nets':nets,'role':role};output.append(q);return q
original('J1');original('U6',{'1':'V5','2':'VCM','3':'GND'})
new('U8','TPS7A3701DRVT',{'1':'V3V3','2':'LDO_FB','3':'GND','4':'PWR5_OK','5':None,'6':'V5','7':'GND'},0,role='EN from independent V5 qualification; actual pad7 must match library EP')
original('C_REF');original('C_PWR');original('C_LDO_IN');original('C_LDO_OUT',{'1':'V3V3','2':'GND'})
q=original('C_MCU_BULK',page=0);q['ref']='C_VCM_OUT';q['nets']={'1':'VCM','2':'GND'}
new('RD_TOP','RT0603BRD0718KL',{'1':'VCM','2':'VEXC'},0,'18k 0.1%')
new('RD_B1','RT0603BRD07162KL',{'1':'VEXC','2':'GND'},0,'162k 0.1%')
original('C_DIV',{'1':'VEXC','2':'GND'})
new('R_LDO_TOP','RT0603BRD0752K3L',{'1':'V3V3','2':'LDO_FB'},0,'52.3k 0.1%')
new('R_LDO_BOT','RT0603BRD0730K1L',{'1':'LDO_FB','2':'GND'},0,'30.1k 0.1%')
q=original('C_ADC0',page=0);q['ref']='C_LDO_FF';q['nets']={'1':'V3V3','2':'LDO_FB'};q['value']='10nF X7R'
new('U1','OPA388IDBVR',{'1':'ROW_DRV','2':'GND','3':'VEXC','4':'ROW_FB','5':'V5'},1)
mux={'1':'ROW_A0','2':'ROW_MUX_EN','3':'GND','8':'ROW_DRV','9':'ROW_FB','14':'V5','15':'GND','16':'ROW_A1'}
for i in range(4):mux[str(4+i)]='ROW'+str(i);mux[str(13-i)]='ROW'+str(i)
new('U4','TMUX1109PWR',mux,1);original('C_ROW_OP');original('C_MUX');original('J2')
original('R_SEL_PD0',{'1':'ROW_A0','2':'GND'});original('R_SEL_PD1',{'1':'ROW_A1','2':'GND'})
original('R_ENABLE_PD',{'1':'ROW_MUX_EN','2':'GND'},1)
tpd=next(v for v in extra['TPD4E05U06 C125795'] if v['uuid']=='9cd0174bf23d4a2a88c341978769c934')
lib['TPD4E05U06DQAR_C125795']=tpd
for j,prefix in enumerate(['ROW','COL']):
 ns={'1':prefix+'0','2':prefix+'1','3':'GND','4':prefix+'2','5':prefix+'3','6':None,'7':None,'8':'GND','9':None,'10':None}
 new('D_FFC_'+prefix,'TPD4E05U06DQAR_C125795',ns,1,'TPD4E05U06DQAR',role='Supplier C125795 template; manufacturer field missing: material conformance HOLD, not a verified TI-stock device')
tia={x['number']:base['pinNetMap'].get('U2-'+x['number'])for x in parts['U2']['pins']}
for i,(minus,out) in enumerate([('2','1'),('6','7'),('9','8'),('13','14')]):tia[minus]='COL'+str(i);tia[out]='TIA'+str(i)
original('U2',tia)
for i in range(4):
 for f in ['RF','CF','R_ADC','C_ADC']:original(f+str(i))
 for f in ['R_COL_SENSE','R_TIA_ISO','C_TIA_HF']:
  q=original(f+str(i),{x['number']:None for x in parts[f+str(i)]['pins']},dnp=True)
  q['role']='DNP recovery reference placeholder; isolated NC pins, NOT a PCB-selectable compensation network; restoration needs later explicit net ECO'
original('C_TIA_OP')
for q in base['pages'][3]['parts']:original(q['ref'])
for q in base['pages'][4]['parts']:
 if q['ref'].startswith('D_J') or q['ref']=='C_RST':continue
 z=original(q['ref'])
 if q['ref']=='U7':z['nets'].update({'7':'ROW_A0','8':'ROW_A1','9':None,'10':None,'15':'ADC_RESET_N','16':'ROW_MUX_EN'})
clamps=['V3V3','SWDIO','SWCLK','PGOOD','V3V3','UART_TX','UART_RX']
for i in range(4):
 a=clamps[2*i];b=clamps[2*i+1] if 2*i+1<len(clamps) else 'PGOOD'
 ns={'1':'GND','6':a,'2':'V3V3','4':'GND','3':b,'5':'V3V3' if i<3 else 'PWR5_OK'}
 new('D_DBG'+str(i),'BAT54XY',ns,4,'BAT54XY,115',role='Last spare isolated branch diode-isolates 5V supervisor from 3.3V NRST; no 5V pullup on MCU')
for ref in ['U9','U9_EN_R','U9_EN_G','U9_IN_CAP','U9_OUT_CAP','U9_BLEED','U10_BLEED','U11','U12','U11_CT_C','U12_CT_C','U11_SENSE_C','U12_SENSE_C','U11_VDD_C','U12_VDD_C']:original(ref)
next(q for q in output if q['ref']=='U9')['nets']['4']=None
new('U9_OV_T','RT0603BRD0734K8L',{'1':'V5_IN','2':'U9_OV'},5,'34.8k 0.1%')
q=original('U11_BOT',{'1':'U9_OV','2':'GND'});q['ref']='U9_OV_B1'
new('U11_TOP0','RT0603BRD0724KL',{'1':'V5','2':'U11_SENSE'},5,'24k 0.1%')
new('U11_BOT','RT0603BRD077K5L',{'1':'U11_SENSE','2':'GND'},5,'7.5k 0.1%')
# Accurate single17k device not found. Preserve the original qualified16.99k chain rather than invent a manufacturer part or silently use5%.
for ref in ['U12_TOP0','U12_TOP1','U12_TOP2','U12_TOP3','U12_BOT']:original(ref)
new('R_LDO_EN_PU','RT0603BRD07100KL',{'1':'V5','2':'PWR5_OK'},5,'100k 0.1%')
for q in output:
 if q['ref']=='U11':q['nets'].update({'3':'V5','4':'V5','6':'PWR5_OK'})
 if q['ref']=='U11_VDD_C':q['nets']['1']='V5'
assert len({q['ref']for q in output})==len(output)
assert next(q for q in output if q['ref']=='U8')['nets']['4']=='PWR5_OK'
assert next(q for q in output if q['ref']=='U11')['nets']['6']=='PWR5_OK'
assert next(q for q in output if q['ref']=='U12')['nets']['6']=='PGOOD'
assert next(q for q in output if q['ref']=='D_DBG3')['nets']['3']=='PGOOD'
assert next(q for q in output if q['ref']=='D_DBG3')['nets']['5']=='PWR5_OK'
counts={f:sum(q['ref'].startswith(f) and not q['dnp']for q in output)for f in ['R','C','D','U','J']}
plan={'project':newlib['project']['uuid'],'pages':[x['page']for x in base['pages']],'parts':output,'populatedCount':sum(not q['dnp']for q in output),'structuralCount':len(output),'counts':counts,'prototypeOnly':True,'hold':['DNP placeholders NOT a qualified switchable compensation footprint arrangement','TPS7A37 EN falling sequencing / adjustable FB reverse condition still requires bounded qualification','TPD C125795 manufacturer field absent','U12 single17k MPN missing; old16.99k equivalent chain retained','All ADC double bulk caps kept until Ceff qualified','Exact J2 footprint metadata inherited, no PCB geometry inspected']}
(p/'C_NATIVE_BUILD_PLAN.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
with(p/'C_CANDIDATE_BOM.csv').open('w',encoding='utf-8',newline='')as f:
 w=csv.DictWriter(f,fieldnames=['ref','value','page','dnp','name','association','nets','role']);w.writeheader()
 for q in output:w.writerow({k:json.dumps(q.get(k),ensure_ascii=False) if k in ['nets','association']else q.get(k,'')for k in w.fieldnames})
print(json.dumps({'plannedStructural':len(output),'populatedCandidate':plan['populatedCount'],'counts':counts,'nativeImplemented':False}))
