import json,pathlib,csv
p=pathlib.Path(__file__).resolve().parent
libs=json.loads((p/'ALL_LIBRARY_PARSED.json').read_text(encoding='utf-8'))
parts=[]
def add(ref,device,page,x,y,nets,value=None,role='',rotation=0):
 pins={q['number']for q in libs[device]['pins']}
 mapping={str(k):v for k,v in nets.items()}
 assert set(mapping)==pins,(ref,set(mapping)^pins)
 assert ref not in {q['ref']for q in parts}
 parts.append(dict(ref=ref,device=device,device_uuid=libs[device]['device']['uuid'],library_uuid=libs[device]['device']['libraryUuid'],page=page,x=x,y=y,rotation=rotation,subpart=libs[device]['pins'][0]['part'],nets=mapping,value=value,role=role))
def r(ref,page,x,y,a,b,value,kind='RT0603BRD0710KL',role=''):
 add(ref,kind,page,x,y,{1:a,2:b},value,role)
def c(ref,page,x,y,a,b,value,kind='GRM188R71C104KA01D',role=''):
 add(ref,kind,page,x,y,{1:a,2:b},value,role)
# Page 1: power, common mode, excitation and precision divider.
add('J1','HDR-M_2.54_1x2P',0,120,150,{1:'V5',2:'GND'},role='Regulated5V input; verify ADC pins4.75-5.25V; no reverse-polarity certification')
add('U6','REF3025AIDBZR',0,330,150,{1:'V5',2:'REF_2V5',3:'GND'})
add('U8','TPS7A2033PDBVR',0,770,150,{1:'V5',2:'GND',3:'V5',4:None,5:'V3V3'})
add('U3','OPA2388IDR',0,300,340,{1:'VCM',2:'VCM',3:'REF_2V5',4:'GND',5:'DIV_2V25',6:'VEXC',7:'VEXC',8:'V5'})
r('RD_TOP',0,100,510,'VCM','DIV_2V25','10k 0.1%')
for i in range(9):
 a='DIV_2V25' if i==0 else 'DIV_SEG'+str(i)
 b='GND' if i==8 else 'DIV_SEG'+str(i+1)
 r('RD_B'+str(i+1),0,320+200*(i%4),480+75*(i//4),a,b,'10k 0.1%',role='9 series precision10k = nominal90k')
c('C_DIV',0,100,620,'DIV_2V25','GND','100nF')
for ref,x,y,supply,kind,val in [('C_PWR',120,260,'V5','GRM188R61C105KA93D','1uF'),('C_REF',480,150,'V5','GRM188R71C104KA01D','100nF'),('C_BUF',520,340,'V5','GRM188R71C104KA01D','100nF'),('C_LDO_IN',690,265,'V5','GRM188R61C105KA93D','1uF'),('C_LDO_OUT',950,265,'V3V3','GRM188R61C105KA93D','1uF')]:c(ref,0,x,y,supply,'GND',val,kind)
# Page 2: row selection/drive. Low SEL chooses B=VCM, high A=VEXC.
mux={1:'ROW_SEL0',2:'VEXC',3:'ROW_CMD0',4:'VCM',5:'GND',6:'GND',7:'VCM',8:'ROW_CMD1',9:'VEXC',10:'ROW_SEL1',11:'ROW_SEL2',12:'VEXC',13:'ROW_CMD2',14:'VCM',15:None,16:'V5',17:'VCM',18:'ROW_CMD3',19:'VEXC',20:'ROW_SEL3'}
add('U4','TMUX1134PWR',1,180,250,mux)
amps=[(1,2,3),(7,6,5),(8,9,10),(14,13,12)]
rowmap={4:'V5',11:'GND'};colmap={4:'V5',11:'GND'}
for i,(out,minus,plus)in enumerate(amps):rowmap.update({out:'ROW_DRV'+str(i),minus:'ROW_FB'+str(i),plus:'ROW_CMD'+str(i)})
add('U1','OPA4388IDR',1,450,250,rowmap)
for i in range(4):
 y=145+125*i
 r('R_ISO'+str(i),1,680,y,'ROW_DRV'+str(i),'ROW'+str(i),'1k 1%','0603WAF1001T5E','Output limit; full DC feedback after resistor; dynamic HOLD')
 r('R_ROW_FB'+str(i),1,900,y,'ROW'+str(i),'ROW_FB'+str(i),'10k 0.1%')
 c('C_ROW_HF'+str(i),1,680,y+55,'ROW_DRV'+str(i),'ROW_FB'+str(i),'1nF C0G','GRM1885C1H102JA01D')
 r('R_SEL_PD'+str(i),1,900,y+55,'ROW_SEL'+str(i),'GND','100k 1%','0603WAF1003T5E','Reset/3V3-loss default SEL low')
c('C_ROW_OP',1,180,480,'V5','GND','100nF');c('C_MUX',1,450,480,'V5','GND','100nF')
add('J2','HDR-M_2.54_1x8P',1,200,635,{1:'ROW0',2:'ROW1',3:'ROW2',4:'ROW3',5:'COL0',6:'COL1',7:'COL2',8:'COL3'},role='FIXED8-wire external4x4 array; no16 sensor resistors mounted on this board')
# Page 3: continuously closed four-column TIA. Sense resistor does not carry sensor current.
for i,(out,minus,plus)in enumerate(amps):colmap.update({out:'TIA'+str(i),minus:'COL_SENSE'+str(i),plus:'VCM'})
add('U2','OPA4388IDR',2,220,260,colmap)
for i in range(4):
 y=150+125*i
 r('R_COL_SENSE'+str(i),2,470,y,'COL'+str(i),'COL_SENSE'+str(i),'10k 0.1%',role='Input clamp current limiting; added pole requires macro-model verification')
 r('RF'+str(i),2,730,y,'TIA'+str(i),'COL'+str(i),'4.99k 0.1%','RT0603BRD074K99L')
 c('CF'+str(i),2,970,y,'TIA'+str(i),'COL'+str(i),'2.2nF C0G','GRM1885C1H222JA01D')
 r('R_ADC'+str(i),2,730,y+55,'TIA'+str(i),'ADC_IN'+str(i),'100R 1%','0603WAF1000T5E')
 c('C_ADC'+str(i),2,970,y+55,'ADC_IN'+str(i),'GND','10nF X7R','GRM188R71C103KA01D')
c('C_TIA_OP',2,220,480,'V5','GND','100nF')
# Page 4: ADC, MCU and programming/UART interfaces.
adc={1:'SPI_MOSI',2:'ADC_RESET_N',3:'GND',4:'GND',5:'ADC_REFIO',6:'GND',7:'ADC_REFCAP',8:'GND',9:'V5',10:'GND',11:'GND',12:None,13:None,14:None,15:None,16:'ADC_IN0',17:'GND',18:'ADC_IN1',19:'GND',20:'GND',21:'ADC_IN2',22:'GND',23:'ADC_IN3',24:None,25:None,26:None,27:None,28:'GND',29:'GND',30:'V5',31:'GND',32:'GND',33:'GND',34:'V3V3',35:None,36:'SPI_MISO',37:'SPI_SCLK',38:'ADC_CS_N'}
add('U5','ADS8684IDBTR',3,270,260,adc)
mcu={i:None for i in range(1,33)}
mcu.update({4:'V3V3',5:'GND',6:'MCU_NRST',7:'ROW_SEL0',8:'ROW_SEL1',9:'ROW_SEL2',10:'ROW_SEL3',11:'ADC_CS_N',12:'SPI_SCLK',13:'SPI_MISO',14:'SPI_MOSI',15:'ADC_RESET_N',19:'UART_TX',21:'UART_RX',24:'SWDIO',25:'SWCLK'})
add('U7','STM32G031K8T6',3,650,260,mcu)
add('J3','HDR-M_2.54_1x6P',3,100,620,{1:'V3V3',2:'GND',3:'SWDIO',4:'SWCLK',5:'MCU_NRST',6:None},role='SWD/programming;3V3 sense, no external5V')
add('J4','HDR-M_2.54_1x4P',3,390,620,{1:'V3V3',2:'GND',3:'UART_TX',4:'UART_RX'},role='3V3 UART logic only; no directRS232/5V UART')
r('R_RST',3,930,125,'V3V3','MCU_NRST','10k 0.1%')
c('C_RST',3,930,195,'MCU_NRST','GND','100nF')
r('R_CS_PU',3,930,265,'V3V3','ADC_CS_N','10k 0.1%')
r('R_ADC_RESET_PD',3,930,335,'ADC_RESET_N','GND','100k 1%','0603WAF1003T5E')
c('C_ADC_REFIO',3,680,545,'ADC_REFIO','GND','22uF 25V X7R','GRM32ER71E226KE15L','Effective>=10uF pending bias curve; hold')
c('C_ADC_REFCAP',3,930,545,'ADC_REFCAP','GND','1uF','GRM188R61C105KA93D')
for ref,x,y,supply in [('C_ADCA1',80,440,'V5'),('C_ADCA2',280,440,'V5'),('C_ADCD',480,440,'V3V3'),('C_MCU1',680,440,'V3V3')]:c(ref,3,x,y,supply,'GND','100nF')
c('C_MCU_BULK',3,930,440,'V3V3','GND','1uF','GRM188R61C105KA93D')
assert len(parts)==len(set(q['ref']for q in parts))
plan={'project_uuid':'74e664f7c1193aad2a35d2db078a1f226377acc149fbbc11d8b1a9f9638bea07','schematic_uuid':'0ccfdd809e468881','initial_page_uuid':'9965fd7b16015eaf','page_names':['Power_Reference','Row_Drive_Interface','Column_TIA','ADC_MCU_Interfaces'],'parts':parts,'notes':[
['Independent first-build0.8-8kohm, 0.25V excitation; regulated5V/3V3','VCM=2.5V; VEXC=2.25V. Divider bottom9x10k=90k','DYNAMIC_VALIDATION_HOLD / FAULT_PROTECTION_HOLD / BENCH_NOT_RELEASED','NoPCB/manufacturing release. Effective reference capacitance pending'],
['TMUX1134:SEL0 ->B=VCM (idle);SEL1 ->A=VEXC (active)','Row ISO changed10R ->1k. Feedback senses board ROW after resistor','J2:1..4 ROW0..3;5..8 COL0..3; external fixed8-electrode array','GPIO reset/HiZ SEL pulldowns; fault safe-state/10ms detection not bench verified'],
['Four TIA feedback loops always closed; VCM to all noninverting inputs','10k sense resistors added at opamp input; sensor current flows throughRF/CF','External lead/contact resistance is not canceled by board-end feedback','DYNAMIC_VALIDATION_HOLD: no vendor macro simulation executed'],
['ADS8684 internal4.096V reference; REFSEL/DAISY low;35DNC strictly NC','AIN0/1=16/18;AIN2/3=21/23. AllAIN_GND toGND, notVCM','100fps target;20kSPS total;4MHz SPI; pipelined channel labels must be checked','FAULT_PROTECTION_HOLD: supply collapse/backfeed/recovery not closed']
]}
(p/'PLANNED_NATIVE_DESIGN.json').write_bytes((json.dumps(plan,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
pinrows=[{'ref':q['ref'],'part':q['device'],'page':plan['page_names'][q['page']],'physical_pin':n,'net':net,'NC':net is None}for q in parts for n,net in q['nets'].items()]
with(p/'PLANNED_PIN_NET.csv').open('w',encoding='utf-8-sig',newline='')as f:w=csv.DictWriter(f,fieldnames=list(pinrows[0]));w.writeheader();w.writerows(pinrows)
print(json.dumps({'parts':len(parts),'physical_pin_entries':len(pinrows),'NC':sum(r['NC']for r in pinrows),'nets':len(set(r['net']for r in pinrows if r['net'])),'page_counts':{n:sum(q['page']==i for q in parts)for i,n in enumerate(plan['page_names'])}}))
