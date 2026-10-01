import pathlib,json,csv,copy
p=pathlib.Path(__file__).resolve().parent;v=p.parent/'FIRST_BUILD_DETAILED_DESIGN_AND_NATIVE_SCHEMATIC_V1'
libs=json.loads((p/'V1_LIBRARY_PARSED.json').read_text(encoding='utf-8'))
libs.update(json.loads((p/'NEW_LIBRARY_PARSED.json').read_text(encoding='utf-8')))
parts=copy.deepcopy(json.loads((v/'PLANNED_NATIVE_DESIGN.json').read_text(encoding='utf-8'))['parts'])
by={q['ref']:q for q in parts}
def change(ref,device=None,value=None,nets=None,page=None,role=None):
 q=by[ref]
 if device:q.update(device=device,device_uuid=libs[device]['device']['uuid'],library_uuid=libs[device]['device']['libraryUuid'],subpart=libs[device]['pins'][0]['part'])
 if value is not None:q['value']=value
 if nets is not None:q['nets']={str(k):n for k,n in nets.items()}
 if page is not None:q['page']=page
 if role is not None:q['role']=role
def add(ref,device,page,nets,value=None,role=''):
 assert ref not in by
 q=dict(ref=ref,device=device,device_uuid=libs[device]['device']['uuid'],library_uuid=libs[device]['device']['libraryUuid'],page=page,x=0,y=0,rotation=0,subpart=libs[device]['pins'][0]['part'],nets={str(k):n for k,n in nets.items()},value=value,role=role)
 parts.append(q);by[ref]=q
def r(ref,page,a,b,value='10k 0.1%',kind='RT0603BRD0710KL',role=''):add(ref,kind,page,{1:a,2:b},value,role)
def c(ref,page,a,b,value='100nF',kind='GRM188R71C104KA01D',role=''):add(ref,kind,page,{1:a,2:b},value,role)
def clamp(ref,page,node,rail='V5'):add(ref,'BAT54S,215',page,{1:'GND',2:rail,3:node},role='Output/connector rail clamp; leakage and Vf/thermal corners remain HOLD')
def hf(ref,page,node):c(ref,page,node,'GND','2.2uF 50V X7R','GRM31CR71H225KA88L','Require >=1uF effective; DC-bias curve not yet verified')
def bulk(ref,page,node):
 for n in ('A','B'):c(ref+n,page,node,'GND','22uF 25V X7R','GRM32ER71E226KE15L','Pair 44uF nominal; >=10uF effective needs retained-bias-factor >=0.2971 after tolerance/temperature')
# Existing parts: main eight-lead topology, excitation and Rf remain frozen.
change('J1',nets={1:'V5_IN',2:'GND'},role='Regulated 5V nominal input; actual V5 must be qualified before valid data')
change('U8',nets={1:'V5',2:'GND',3:'V5',4:None,5:'V3_LDO'})
change('C_LDO_OUT',device='GRM31CR71H225KA88L',value='2.2uF 50V X7R',nets={1:'V3_LDO',2:'GND'},role='LDO output before reverse blocker; effective >=0.47uF required')
change('C_LDO_IN',device='GRM31CR71H225KA88L',value='2.2uF 50V X7R')
change('C_PWR',device='GRM31CR71H225KA88L',value='2.2uF 50V X7R')
change('U3',nets={1:'VCM_DRV',2:'VCM',3:'REF_2V5',4:'GND',5:'DIV_2V25',6:'VEXC',7:'VEXC_DRV',8:'V5'})
r('R_VCM_ISO',0,'VCM_DRV','VCM','1k 1%','0603WAF1001T5E','Feedback senses VCM after isolation')
r('R_VEX_ISO',0,'VEXC_DRV','VEXC','1k 1%','0603WAF1001T5E','Feedback senses VEXC after isolation')
clamp('D_VCM',0,'VCM_DRV');clamp('D_VEX',0,'VEXC_DRV')
for i in range(4):
 change('R_ROW_FB'+str(i),device='RT0603BRD074K99L',value='4.99k 0.1%')
 change('C_ROW_HF'+str(i),device='GRM1885C1H101JA01D',value='100pF 50V C0G')
 clamp('D_ROW'+str(i),1,'ROW_DRV'+str(i))
 # Rf and Cf see the isolated tap. The amplifier output has no direct Cf-to-COL path.
 by['U2']['nets'][str((1,7,8,14)[i])]='TIA_DRV'+str(i)
 r('R_TIA_ISO'+str(i),2,'TIA_DRV'+str(i),'TIA'+str(i),'1k 1%','0603WAF1001T5E','All RF/CF and ADC takeoff after 1k output isolation')
 clamp('D_TIA'+str(i),2,'TIA_DRV'+str(i))
# ADC page 3; move MCU/communications to page 4.
for ref in ['U7','J3','J4','R_RST','C_RST','C_MCU1','C_MCU_BULK']:change(ref,page=4)
change('C_ADC_REFIO',device='GRM32ER71E226KE15L',value='22uF 25V X7R',role='Independent REFIO capacitor; supplemented by C_REFIO_B')
c('C_REFIO_B',3,'ADC_REFIO','GND','22uF 25V X7R','GRM32ER71E226KE15L','REFIO combined >=10uF effective remains HOLD')
change('C_ADC_REFCAP',device='GRM31CR71H225KA88L',value='2.2uF 50V X7R',role='Near REFCAP HF decoupler; >=1uF effective remains HOLD')
bulk('C_REFCAP_BULK',3,'ADC_REFCAP')
for supply,ref in [('V5','C_AVDD9'),('V5','C_AVDD30'),('V3V3','C_DVDD34')]:bulk(ref,3,supply)
hf('C_AVDD9_HF',3,'V5');hf('C_AVDD30_HF',3,'V5')
change('R_RST',nets={1:'V3V3',2:'PGOOD'})
change('C_RST',nets={1:'V3V3',2:'GND'},role='Moved reset RC capacitor to auxiliary supply decoupling; supervisor CT supplies reset delay')
by['U7']['nets']['6']='PGOOD'
for i in range(4):by['U7']['nets'][str(7+i)]='MCU_ROW'+str(i)
by['U7']['nets']['15']='MCU_ADC_RESET'
# Existing unused PB1 pin16 is assigned explicit acquisition permit, verified in the real library.
by['U7']['nets']['16']='MCU_ENABLE'
by['U5']['nets']['2']='ADC_RESET_N'
change('R_ADC_RESET_PD',nets={1:'ADC_RESET_N',2:'GND'})
# 4.99k series limits external injection; 100ohm rail bleeder absorbs all seven worst-case connector currents.
for j in ['J3','J4']:
 for pin,net in list(by[j]['nets'].items()):
  if net is None or net=='GND':continue
  ext=net+'_EXT'
  by[j]['nets'][pin]=ext
  r('R_'+j+'_'+pin,4,ext,'PGOOD' if net=='MCU_NRST' else net,'4.99k 0.1%','RT0603BRD074K99L','External probe/programmer no board power input; current limited even on sense pins')
  clamp('D_'+j+'_'+pin,4,'PGOOD' if net=='MCU_NRST' else net,'V3V3')
# Protection/qualification page 5.
for ref,src,dst in [('U9','V5_IN','V5'),('U10','V3_LDO','V3V3')]:
 add(ref,'LM73100RPWR',5,{1:ref+'_EN',2:ref+'_OV',3:None,4:ref+'_PGTH',5:src,6:dst,7:None,8:'GND',9:'GND',10:None},role='Always-on reverse current blocking; PG unused because power-off low is not assured')
 r(ref+'_EN_R',5,src,ref+'_EN','10k 0.1%')
 r(ref+'_EN_G',5,ref+'_EN','GND','10k 0.1%')
 r(ref+'_OV_T',5,src,ref+'_OV','10k 0.1%')
 r(ref+'_OV_B1',5,ref+'_OV',ref+'_OV_M','1k 1%','0603WAF1001T5E')
 r(ref+'_OV_B2',5,ref+'_OV_M','GND','1k 1%','0603WAF1001T5E')
 r(ref+'_PG_T',5,dst,ref+'_PGTH','10k 0.1%')
 r(ref+'_PG_B',5,ref+'_PGTH','GND','10k 0.1%')
 hf(ref+'_IN_CAP',5,src);hf(ref+'_OUT_CAP',5,dst)
 r(ref+'_BLEED',5,dst,'GND','100R 1%', 'RC2010FK-07100RL' if dst=='V5' else 'RC1206FR-07100RL','Finite rail sink, 0.278W/0.110W worst normal, not precision shunt regulation')
# TPS389001: threshold1.15V; both powered from V3V3, monitor actual downstream rails.
for ref,rail,values in [('U11','V5',[('10k 0.1%','RT0603BRD0710KL')]*3+[('1k 1%','0603WAF1001T5E')]*2),('U12','V3V3',[('10k 0.1%','RT0603BRD0710KL'),('4.99k 0.1%','RT0603BRD074K99L'),('1k 1%','0603WAF1001T5E'),('1k 1%','0603WAF1001T5E')])]:
 add(ref,'TPS389001DSET',5,{1:ref+'_SENSE',2:'GND',3:'V3V3',4:'V3V3',5:ref+'_CT',6:'PGOOD'},role='Open-drain supervisors wired AND to reset and hardware enable')
 chain=[rail]+[ref+'_DIV'+str(i)for i in range(1,len(values))]+[ref+'_SENSE']
 for i,(value,kind)in enumerate(values):r(ref+'_TOP'+str(i),5,chain[i],chain[i+1],value,kind)
 r(ref+'_BOT',5,ref+'_SENSE','GND')
 c(ref+'_SENSE_C',5,ref+'_SENSE','GND','1nF C0G','GRM1885C1H102JA01D')
 c(ref+'_CT_C',5,ref+'_CT','GND','100nF')
 c(ref+'_VDD_C',5,'V3V3','GND','100nF')
add('U15','SN74LVC1G17DBVR',5,{1:None,2:'PGOOD',3:'GND',4:'PG_OK_FAST',5:'V3V3'},role='Schmitt reshapes supervisor open-drain edge before LVC08 inputs')
c('C_U15',5,'V3V3','GND')
add('U13','SN74LVC08APWR',5,{1:'PG_OK_FAST',2:'MCU_ENABLE',3:'HW_ENABLE',4:'PG_OK_FAST',5:'MCU_ADC_RESET',6:'ADC_RESET_N',7:'GND',8:None,9:'GND',10:'GND',11:None,12:'GND',13:'GND',14:'V3V3'})
add('U14','SN74LVC08APWR',1,{1:'HW_ENABLE',2:'MCU_ROW0',3:'ROW_SEL0',4:'HW_ENABLE',5:'MCU_ROW1',6:'ROW_SEL1',7:'GND',8:'ROW_SEL2',9:'HW_ENABLE',10:'MCU_ROW2',11:'ROW_SEL3',12:'HW_ENABLE',13:'MCU_ROW3',14:'V3V3'})
r('R_ENABLE_PD',5,'MCU_ENABLE','GND','100k 1%','0603WAF1003T5E')
r('R_HW_PD',5,'HW_ENABLE','GND','100k 1%','0603WAF1003T5E')
c('C_U13',5,'V3V3','GND');c('C_U14',1,'V3V3','GND')
# Library pin names/number/pads were read from real elibz2. Validate all maps, never fabricate omitted pins.
for q in parts:assert set(q['nets'])=={x['number']for x in libs[q['device']]['pins']},q['ref']
pages=['Power_Reference','Rows_8lead_Interface','Continuous_Column_TIAs','ADS8684_Decoupling','MCU_Protected_Interfaces','Power_Qualification']
# Roomy uniform part cells; keep ICs in a separate band. Decorative default frame is removed, labels stay visible.
for page in range(6):
 a=[q for q in parts if q['page']==page]
 ics=[q for q in a if q['ref'].startswith('U')];others=[q for q in a if q not in ics]
 for i,q in enumerate(ics):q.update(x=350+(i%3)*620,y=260+(i//3)*280)
 start=620 if len(ics)<=3 else 860
 for i,q in enumerate(others):q.update(x=280+(i%4)*450,y=start+(i//4)*140)
notes=[
 ['R2 REVIEW ONLY: 4x4 / 8 leads; VCM2.5V, VEXC2.25V, E0.25V, Rf4.99k','Feedback senses VCM/VEXC after 1k isolation; macro stability HOLD','Reference/supply capacitance and rail qualification: see page4/6 and report'],
 ['Rs1k / Rb4.99k / Ch100pF candidate; ideal 300us screening PASS','SEL = MCU_ROW AND HW_ENABLE; HW_ENABLE = PGOOD AND MCU_ENABLE','Eight sensor leads only; no mounted16 sensor resistors; clamps do not establish whole-board fault PASS'],
 ['Four continuous TIAs; Rf4.99k || Cf2.2nF from isolated TIA tap to COL','OPA output -> 1k -> TIA tap; all ADC/filter/feedback takeoffs after isolation','COL -> 10k -> OPA minus; internal input-clamp current bounded, fault/thermal and macro loop HOLD'],
 ['Internal4.096V ADC reference; REFIO and REFCAP independently bulk bypassed','AVDD pins9/30 each44uF+2.2uF nominal; DVDD pin34 44uF nominal','Effective capacitance and placement must meet datasheet: REFERENCE_CAPACITANCE_HOLD'],
 ['GPIO PB1 pin16 = MCU_ENABLE; PGOOD resets MCU; Schmitt reshapes hardware gate edge','External SWD/UART/sense lines all4.99k current limited, clamps and rail sink','Offline SPI: 0-5.12V range0x06, tagged48clk frames, 40kSPS / hardware timing HOLD'],
 ['LM73100 both supply paths; TPS389001 monitors actual V5/V3V3 rails','PGOOD = both supervisor RESET outputs released; nominal thresholds4.830V/3.10385V','No manufacture / procurement / bench power release. DYNAMIC and FAULT HOLD retained']]
plan={'package':'SCIENCE_ADK5556_4X4_FIRST_BUILD_ELECTRICAL_CLOSURE_AND_SCHEMATIC_R2_V1','project_uuid':None,'page_names':pages,'parts':parts,'notes':notes,'schema_version':2,'status':'R2_CANDIDATE_FROZEN_FOR_VALIDATION','new_function_classes':['output_isolation_and_clamps','supply_reverse_blocking','dual_power_supervision','hardware_acquisition_inhibit','external_digital_injection_limiting'],'limitations':['No confirmed SPICE executor','MLCC effective-capacity curves unavailable','Clamps not yet verified for all temperatures/60s','Native/visual/field persistence audits pending']}
(p/'R2_PLAN.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(p/'R2_ALL_LIBRARY_PARSED.json').write_text(json.dumps(libs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
rows=[{'ref':q['ref'],'device':q['device'],'device_uuid':q['device_uuid'],'page':pages[q['page']],'pin':n,'net':net,'NC':net is None}for q in parts for n,net in q['nets'].items()]
with(p/'R2_PLANNED_PIN_NET.csv').open('w',encoding='utf-8-sig',newline='')as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
with(p/'R2_BOM.csv').open('w',encoding='utf-8-sig',newline='')as f:
 w=csv.DictWriter(f,fieldnames=['ref','device','value','page','supplier_id','footprint','role']);w.writeheader()
 for q in parts:w.writerow({'ref':q['ref'],'device':q['device'],'value':q['value'],'page':pages[q['page']],'supplier_id':libs[q['device']]['device']['supplierId'],'footprint':libs[q['device']]['device']['footprintName'],'role':q['role']})
print(json.dumps({'parts':len(parts),'pins':len(rows),'nets':len(set(x['net']for x in rows if x['net'])),'NC':sum(x['NC']for x in rows),'page_counts':[sum(q['page']==i for q in parts)for i in range(6)]}))
