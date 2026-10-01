
const plan={"project": "74e664f7c1193aad2a35d2db078a1f226377acc149fbbc11d8b1a9f9638bea07", "page": {"uuid": "cd673e3782e532f6", "name": "ADC_MCU_Interfaces", "index": 3}, "parts": [{"ref": "U5", "x": 270, "y": 260, "nets": {"1": "SPI_MOSI", "2": "ADC_RESET_N", "3": "GND", "4": "GND", "5": "ADC_REFIO", "6": "GND", "7": "ADC_REFCAP", "8": "GND", "9": "V5", "10": "GND", "11": "GND", "12": null, "13": null, "14": null, "15": null, "16": "ADC_IN0", "17": "GND", "18": "ADC_IN1", "19": "GND", "20": "GND", "21": "ADC_IN2", "22": "GND", "23": "ADC_IN3", "24": null, "25": null, "26": null, "27": null, "28": "GND", "29": "GND", "30": "V5", "31": "GND", "32": "GND", "33": "GND", "34": "V3V3", "35": null, "36": "SPI_MISO", "37": "SPI_SCLK", "38": "ADC_CS_N"}}, {"ref": "U7", "x": 650, "y": 260, "nets": {"1": null, "2": null, "3": null, "4": "V3V3", "5": "GND", "6": "MCU_NRST", "7": "ROW_SEL0", "8": "ROW_SEL1", "9": "ROW_SEL2", "10": "ROW_SEL3", "11": "ADC_CS_N", "12": "SPI_SCLK", "13": "SPI_MISO", "14": "SPI_MOSI", "15": "ADC_RESET_N", "16": null, "17": null, "18": null, "19": "UART_TX", "20": null, "21": "UART_RX", "22": null, "23": null, "24": "SWDIO", "25": "SWCLK", "26": null, "27": null, "28": null, "29": null, "30": null, "31": null, "32": null}}, {"ref": "J3", "x": 100, "y": 620, "nets": {"1": "V3V3", "2": "GND", "3": "SWDIO", "4": "SWCLK", "5": "MCU_NRST", "6": null}}, {"ref": "J4", "x": 390, "y": 620, "nets": {"1": "V3V3", "2": "GND", "3": "UART_TX", "4": "UART_RX"}}, {"ref": "R_RST", "x": 930, "y": 125, "nets": {"1": "V3V3", "2": "MCU_NRST"}}, {"ref": "C_RST", "x": 930, "y": 195, "nets": {"1": "MCU_NRST", "2": "GND"}}, {"ref": "R_CS_PU", "x": 930, "y": 265, "nets": {"1": "V3V3", "2": "ADC_CS_N"}}, {"ref": "R_ADC_RESET_PD", "x": 930, "y": 335, "nets": {"1": "ADC_RESET_N", "2": "GND"}}, {"ref": "C_ADC_REFIO", "x": 680, "y": 545, "nets": {"1": "ADC_REFIO", "2": "GND"}}, {"ref": "C_ADC_REFCAP", "x": 930, "y": 545, "nets": {"1": "ADC_REFCAP", "2": "GND"}}, {"ref": "C_ADCA1", "x": 80, "y": 440, "nets": {"1": "V5", "2": "GND"}}, {"ref": "C_ADCA2", "x": 280, "y": 440, "nets": {"1": "V5", "2": "GND"}}, {"ref": "C_ADCD", "x": 480, "y": 440, "nets": {"1": "V3V3", "2": "GND"}}, {"ref": "C_MCU1", "x": 680, "y": 440, "nets": {"1": "V3V3", "2": "GND"}}, {"ref": "C_MCU_BULK", "x": 930, "y": 440, "nets": {"1": "V3V3", "2": "GND"}}]};
const result={page:plan.page,repair:'ACTUAL_PIN_ROTATION_OUTWARD_AND_QUANTIZED_STUBS',parts:[],wires:[],ports:[]};
const project=await eda.dmt_Project.getCurrentProjectInfo();if(project?.uuid!==plan.project)throw Error('Wrong project');
await eda.dmt_EditorControl.openDocument(plan.page.uuid);if((await eda.dmt_Schematic.getCurrentSchematicPageInfo())?.uuid!==plan.page.uuid)throw Error('Wrong page');
let cs=await eda.sch_PrimitiveComponent.getAll();
const actualParts=cs.filter(c=>c.getState_ComponentType()==='part');
if(actualParts.length!==plan.parts.length)throw Error('Unexpected part count');
const ws=await eda.sch_PrimitiveWire.getAll();result.removedWires=ws.map(w=>w.getState_PrimitiveId());
if(ws.length&&!(await eda.sch_PrimitiveWire.delete(result.removedWires)))throw Error('Delete generated wires');
const ports=cs.filter(c=>c.getState_ComponentType()==='netport');result.removedPorts=ports.map(c=>c.getState_PrimitiveId());
if(ports.length&&!(await eda.sch_PrimitiveComponent.delete(result.removedPorts)))throw Error('Delete generated ports');
for(const q of plan.parts){
 const c=actualParts.find(v=>v.getState_Designator()===q.ref);if(!c)throw Error('Missing '+q.ref);
 let ps=await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId());
 if(q.ref.startsWith('C')&&ps.some(v=>[90,270].includes(v.getState_Rotation()))){
  const rotated=await eda.sch_PrimitiveComponent.modify(c,{rotation:90});if(!rotated)throw Error('Passive orientation');
  ps=await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId());
  (result.rotatedPassives??=[]).push(q.ref);
 }
 if(ps.length!==Object.keys(q.nets).length)throw Error('Pin count');
 for(const pin of ps){const n=String(pin.getState_PinNumber()),net=q.nets[n];if(net===null){if(!pin.getState_NoConnected())throw Error('NC drift');continue;}
 const x=pin.getState_X(),y=pin.getState_Y(),rot=pin.getState_Rotation();
 if(![0,90,180,270].includes(rot))throw Error('Unreviewed actual pin angle '+rot);
 const ox=rot===0?40:rot===180?-40:0,oy=ox===0?Math.sign(y-q.y)*40:0;
 if(ox===0&&oy===0)throw Error('Undefined vertical outward coordinate');
 const ex=x+ox,ey=y+oy;
 const port=await eda.sch_PrimitiveComponent.createNetPort('BI',net,ex,ey,ox<0?180:ox>0?0:oy>0?90:270,false);if(!port)throw Error('Port');
 const pp=await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(port.getState_PrimitiveId());if(pp.length!==1)throw Error('Port pin');
 const ax=Math.round(pp[0].getState_X()*1e6)/1e6,ay=Math.round(pp[0].getState_Y()*1e6)/1e6;
 if(Math.abs(ax-ex)>1e-5||Math.abs(ay-ey)>1e-5)throw Error('Actual port anchor mismatch');
 const line=[x,y,ax,ay];const w=await eda.sch_PrimitiveWire.create([line],net);if(!w)throw Error('Wire');
 for(const a of await eda.sch_PrimitiveAttribute.getAll(port.getState_PrimitiveId()))if(a.getState_ValueVisible())await eda.sch_PrimitiveAttribute.modify(a,{fontSize:6,rotation:0,x:ex+(ox>=0?18:-18),y:ey,alignMode:ox>=0?2:8});
 result.wires.push({ref:q.ref,pin:n,id:w.getState_PrimitiveId(),net,line});result.ports.push({ref:q.ref,pin:n,id:port.getState_PrimitiveId(),net,x:ax,y:ay});
 }
 result.parts.push({ref:q.ref,id:c.getState_PrimitiveId()});
}
result.status='REPAIR_COMPLETED_UNSAVED';return result;
