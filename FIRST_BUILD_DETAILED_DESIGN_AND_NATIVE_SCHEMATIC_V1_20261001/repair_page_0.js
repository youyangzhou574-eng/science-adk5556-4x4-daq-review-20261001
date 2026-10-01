
const plan={"project": "74e664f7c1193aad2a35d2db078a1f226377acc149fbbc11d8b1a9f9638bea07", "page": {"uuid": "9965fd7b16015eaf", "name": "Power_Reference", "index": 0}, "parts": [{"ref": "J1", "x": 120, "y": 150, "nets": {"1": "V5", "2": "GND"}}, {"ref": "U6", "x": 330, "y": 150, "nets": {"1": "V5", "2": "REF_2V5", "3": "GND"}}, {"ref": "U8", "x": 770, "y": 150, "nets": {"1": "V5", "2": "GND", "3": "V5", "4": null, "5": "V3V3"}}, {"ref": "U3", "x": 300, "y": 340, "nets": {"1": "VCM", "2": "VCM", "3": "REF_2V5", "4": "GND", "5": "DIV_2V25", "6": "VEXC", "7": "VEXC", "8": "V5"}}, {"ref": "RD_TOP", "x": 100, "y": 510, "nets": {"1": "VCM", "2": "DIV_2V25"}}, {"ref": "RD_B1", "x": 320, "y": 480, "nets": {"1": "DIV_2V25", "2": "DIV_SEG1"}}, {"ref": "RD_B2", "x": 520, "y": 480, "nets": {"1": "DIV_SEG1", "2": "DIV_SEG2"}}, {"ref": "RD_B3", "x": 720, "y": 480, "nets": {"1": "DIV_SEG2", "2": "DIV_SEG3"}}, {"ref": "RD_B4", "x": 920, "y": 480, "nets": {"1": "DIV_SEG3", "2": "DIV_SEG4"}}, {"ref": "RD_B5", "x": 320, "y": 555, "nets": {"1": "DIV_SEG4", "2": "DIV_SEG5"}}, {"ref": "RD_B6", "x": 520, "y": 555, "nets": {"1": "DIV_SEG5", "2": "DIV_SEG6"}}, {"ref": "RD_B7", "x": 720, "y": 555, "nets": {"1": "DIV_SEG6", "2": "DIV_SEG7"}}, {"ref": "RD_B8", "x": 920, "y": 555, "nets": {"1": "DIV_SEG7", "2": "DIV_SEG8"}}, {"ref": "RD_B9", "x": 320, "y": 630, "nets": {"1": "DIV_SEG8", "2": "GND"}}, {"ref": "C_DIV", "x": 100, "y": 620, "nets": {"1": "DIV_2V25", "2": "GND"}}, {"ref": "C_PWR", "x": 120, "y": 260, "nets": {"1": "V5", "2": "GND"}}, {"ref": "C_REF", "x": 480, "y": 150, "nets": {"1": "V5", "2": "GND"}}, {"ref": "C_BUF", "x": 520, "y": 340, "nets": {"1": "V5", "2": "GND"}}, {"ref": "C_LDO_IN", "x": 690, "y": 265, "nets": {"1": "V5", "2": "GND"}}, {"ref": "C_LDO_OUT", "x": 950, "y": 265, "nets": {"1": "V3V3", "2": "GND"}}]};
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
