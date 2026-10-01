
const plan={"project": "74e664f7c1193aad2a35d2db078a1f226377acc149fbbc11d8b1a9f9638bea07", "page": {"uuid": "a51b95c47c70bc0e", "name": "Column_TIA", "index": 2}, "parts": [{"ref": "U2", "x": 220, "y": 260, "nets": {"4": "V5", "11": "GND", "1": "TIA0", "2": "COL_SENSE0", "3": "VCM", "7": "TIA1", "6": "COL_SENSE1", "5": "VCM", "8": "TIA2", "9": "COL_SENSE2", "10": "VCM", "14": "TIA3", "13": "COL_SENSE3", "12": "VCM"}}, {"ref": "R_COL_SENSE0", "x": 470, "y": 150, "nets": {"1": "COL0", "2": "COL_SENSE0"}}, {"ref": "RF0", "x": 730, "y": 150, "nets": {"1": "TIA0", "2": "COL0"}}, {"ref": "CF0", "x": 970, "y": 150, "nets": {"1": "TIA0", "2": "COL0"}}, {"ref": "R_ADC0", "x": 730, "y": 205, "nets": {"1": "TIA0", "2": "ADC_IN0"}}, {"ref": "C_ADC0", "x": 970, "y": 205, "nets": {"1": "ADC_IN0", "2": "GND"}}, {"ref": "R_COL_SENSE1", "x": 470, "y": 275, "nets": {"1": "COL1", "2": "COL_SENSE1"}}, {"ref": "RF1", "x": 730, "y": 275, "nets": {"1": "TIA1", "2": "COL1"}}, {"ref": "CF1", "x": 970, "y": 275, "nets": {"1": "TIA1", "2": "COL1"}}, {"ref": "R_ADC1", "x": 730, "y": 330, "nets": {"1": "TIA1", "2": "ADC_IN1"}}, {"ref": "C_ADC1", "x": 970, "y": 330, "nets": {"1": "ADC_IN1", "2": "GND"}}, {"ref": "R_COL_SENSE2", "x": 470, "y": 400, "nets": {"1": "COL2", "2": "COL_SENSE2"}}, {"ref": "RF2", "x": 730, "y": 400, "nets": {"1": "TIA2", "2": "COL2"}}, {"ref": "CF2", "x": 970, "y": 400, "nets": {"1": "TIA2", "2": "COL2"}}, {"ref": "R_ADC2", "x": 730, "y": 455, "nets": {"1": "TIA2", "2": "ADC_IN2"}}, {"ref": "C_ADC2", "x": 970, "y": 455, "nets": {"1": "ADC_IN2", "2": "GND"}}, {"ref": "R_COL_SENSE3", "x": 470, "y": 525, "nets": {"1": "COL3", "2": "COL_SENSE3"}}, {"ref": "RF3", "x": 730, "y": 525, "nets": {"1": "TIA3", "2": "COL3"}}, {"ref": "CF3", "x": 970, "y": 525, "nets": {"1": "TIA3", "2": "COL3"}}, {"ref": "R_ADC3", "x": 730, "y": 580, "nets": {"1": "TIA3", "2": "ADC_IN3"}}, {"ref": "C_ADC3", "x": 970, "y": 580, "nets": {"1": "ADC_IN3", "2": "GND"}}, {"ref": "C_TIA_OP", "x": 220, "y": 480, "nets": {"1": "V5", "2": "GND"}}]};
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
