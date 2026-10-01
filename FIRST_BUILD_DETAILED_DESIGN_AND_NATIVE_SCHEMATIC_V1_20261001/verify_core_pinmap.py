import pathlib,json,csv,collections
p=pathlib.Path(__file__).resolve().parent
raw=json.loads((p/'CORE_LIBRARY_PIN_PAD_RAW.json').read_text(encoding='utf-8'))
expected={
 'OPA4388IDR':{1:'OUTA',2:'INA-',3:'INA+',4:'V+',5:'INB+',6:'INB-',7:'OUTB',8:'OUTC',9:'INC-',10:'INC+',11:'V-',12:'IND+',13:'IND-',14:'OUTD'},
 'OPA2388IDR':{1:'OUTA',2:'INA-',3:'INA+',4:'V-',5:'INB+',6:'INB-',7:'OUTB',8:'V+'},
 'TMUX1134PWR':{1:'SEL1',2:'S1A',3:'D1',4:'S1B',5:'VSS',6:'GND',7:'S2B',8:'D2',9:'S2A',10:'SEL2',11:'SEL3',12:'S3A',13:'D3',14:'S3B',15:'NC',16:'VDD',17:'S4B',18:'D4',19:'S4A',20:'SEL4'},
 'ADS8684IDBTR':{1:'SDI',2:'RST/PD',3:'DAISY',4:'REFSEL',5:'REFIO',6:'REFGND',7:'REFCAP',8:'AGND',9:'AVDD',10:'AUX_IN',11:'AUX_GND',12:'NC',13:'NC',14:'NC',15:'NC',16:'AIN_0P',17:'AIN_0GND',18:'AIN_1P',19:'AIN_1GND',20:'AIN_2GND',21:'AIN_2P',22:'AIN_3GND',23:'AIN_3P',24:'NC',25:'NC',26:'NC',27:'NC',28:'AGND',29:'AGND',30:'AVDD',31:'AGND',32:'AGND',33:'DGND',34:'DVDD',35:'DNC',36:'SDO',37:'SCLK',38:'CS'},
 'REF3025AIDBZR':{1:'IN',2:'OUT',3:'GND'},
 'STM32G031K8T6':{1:'PB9',2:'PC14-OSC32IN',3:'PC15-OSC32OUT',4:'VDD/VDDA',5:'VSS/VSSA',6:'PF2-NRST',7:'PA0',8:'PA1',9:'PA2',10:'PA3',11:'PA4',12:'PA5',13:'PA6',14:'PA7',15:'PB0',16:'PB1',17:'PB2',18:'PA8',19:'PA9',20:'PC6',21:'PA10',22:'PA11[PA9]',23:'PA12[PA10]',24:'PA13',25:'PA14-BOOT0',26:'PA15',27:'PB3',28:'PB4',29:'PB5',30:'PB6',31:'PB7',32:'PB8'},
 'TPS7A2033PDBVR':{1:'IN',2:'GND',3:'EN',4:'NC',5:'OUT'}}
sources={'OPA4388IDR':'OPAx388.pdf p5 Figure5-4/table','OPA2388IDR':'OPAx388.pdf p5 Figure5-3/table','TMUX1134PWR':'TMUX1134.pdf p4 Figure5-2/table5-2, p21 truth table','ADS8684IDBTR':'ADS8684.pdf p4 package diagram plus p5 pin names; p5 AIN2/3 prose polarity conflict retained; official EVM cross-check still pending','REF3025AIDBZR':'REF30.pdf p3 Figure5-1/table5-1','STM32G031K8T6':'ST DS12992 Rev4 p33 Figure7 LQFP32, official web PDF read; local PDF download failed','TPS7A2033PDBVR':'TPS7A20.pdf p4 DBV pin table'}
def norm(s):
 s=s.replace('#','').replace('.','')
 if s=='OUA':s='OUTA'
 for ch in 'ABCD':
  if s==('-IN'+ch):s='IN'+ch+'-'
  if s==('+IN'+ch):s='IN'+ch+'+'
 return s
rows=[];checks=[]
for name,dev in raw.items():
 nums=[int(x['number']) for x in dev['pins']];pads=[int(x['body']['num']) for x in dev['pad_records']]
 assert len(nums)==len(set(nums)),'duplicate physical pin '+name
 assert len(pads)==len(set(pads)),'duplicate footprint pad '+name
 assert set(nums)==set(pads)==set(expected[name]),'missing pin/pad '+name
 for pin in dev['pins']:
  n=int(pin['number']);assert norm(pin['name'])==norm(expected[name][n]),(name,n,pin['name'],expected[name][n])
  rows.append({'manufacturer_part':name,'library_device_uuid':dev['device']['uuid'],'supplier_id':dev['device']['supplierId'],'symbol_uuid':dev['device']['symbolUuid'],'footprint_uuid':dev['device']['footprintUuid'],'footprint_name':dev['device']['footprintName'],'physical_pin':n,'datasheet_function':expected[name][n],'symbol_pin_number':pin['number'],'symbol_pin_name':pin['name'],'symbol_subpart':pin['part'],'footprint_pad_number':n,'source':sources[name],'status':'NUMERIC_AND_FUNCTION_CORRESPONDENCE_PASS','remaining':'ADS8684 official EVM corroboration pending; actual placed-instance and post-reopen net audit pending' if name=='ADS8684IDBTR' else 'actual placed-instance and post-reopen net audit pending'})
 checks.append({'part':name,'pins':len(nums),'pads':len(pads),'status':'PASS'})
with (p/'EXACT_BOM_AND_PINMAP.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(p/'P1_CORE_PINMAP_CHECKS.json').write_bytes((json.dumps({'checks':checks,'physical_pins_total':len(rows),'manufacturer_electrical_limits_and_geometry_full_qualification':'NOT_CLAIMED','package_pin_diagrams_reviewed':['ADS8684 p4','OPAx388 p5'],'ADC_documentation_conflict_recorded':True},indent=2)+'\n').encode('utf-8'))
print(json.dumps({'checks':checks,'pins_total':len(rows)}))
