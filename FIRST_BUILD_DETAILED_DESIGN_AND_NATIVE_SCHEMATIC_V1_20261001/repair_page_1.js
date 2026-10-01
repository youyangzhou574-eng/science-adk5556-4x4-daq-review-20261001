
const plan={"project": "74e664f7c1193aad2a35d2db078a1f226377acc149fbbc11d8b1a9f9638bea07", "page": {"uuid": "1baf912db250d2de", "name": "Row_Drive_Interface", "index": 1}, "parts": [{"ref": "U4", "x": 180, "y": 250, "nets": {"1": "ROW_SEL0", "2": "VEXC", "3": "ROW_CMD0", "4": "VCM", "5": "GND", "6": "GND", "7": "VCM", "8": "ROW_CMD1", "9": "VEXC", "10": "ROW_SEL1", "11": "ROW_SEL2", "12": "VEXC", "13": "ROW_CMD2", "14": "VCM", "15": null, "16": "V5", "17": "VCM", "18": "ROW_CMD3", "19": "VEXC", "20": "ROW_SEL3"}}, {"ref": "U1", "x": 450, "y": 250, "nets": {"4": "V5", "11": "GND", "1": "ROW_DRV0", "2": "ROW_FB0", "3": "ROW_CMD0", "7": "ROW_DRV1", "6": "ROW_FB1", "5": "ROW_CMD1", "8": "ROW_DRV2", "9": "ROW_FB2", "10": "ROW_CMD2", "14": "ROW_DRV3", "13": "ROW_FB3", "12": "ROW_CMD3"}}, {"ref": "R_ISO0", "x": 680, "y": 145, "nets": {"1": "ROW_DRV0", "2": "ROW0"}}, {"ref": "R_ROW_FB0", "x": 900, "y": 145, "nets": {"1": "ROW0", "2": "ROW_FB0"}}, {"ref": "C_ROW_HF0", "x": 680, "y": 200, "nets": {"1": "ROW_DRV0", "2": "ROW_FB0"}}, {"ref": "R_SEL_PD0", "x": 900, "y": 200, "nets": {"1": "ROW_SEL0", "2": "GND"}}, {"ref": "R_ISO1", "x": 680, "y": 270, "nets": {"1": "ROW_DRV1", "2": "ROW1"}}, {"ref": "R_ROW_FB1", "x": 900, "y": 270, "nets": {"1": "ROW1", "2": "ROW_FB1"}}, {"ref": "C_ROW_HF1", "x": 680, "y": 325, "nets": {"1": "ROW_DRV1", "2": "ROW_FB1"}}, {"ref": "R_SEL_PD1", "x": 900, "y": 325, "nets": {"1": "ROW_SEL1", "2": "GND"}}, {"ref": "R_ISO2", "x": 680, "y": 395, "nets": {"1": "ROW_DRV2", "2": "ROW2"}}, {"ref": "R_ROW_FB2", "x": 900, "y": 395, "nets": {"1": "ROW2", "2": "ROW_FB2"}}, {"ref": "C_ROW_HF2", "x": 680, "y": 450, "nets": {"1": "ROW_DRV2", "2": "ROW_FB2"}}, {"ref": "R_SEL_PD2", "x": 900, "y": 450, "nets": {"1": "ROW_SEL2", "2": "GND"}}, {"ref": "R_ISO3", "x": 680, "y": 520, "nets": {"1": "ROW_DRV3", "2": "ROW3"}}, {"ref": "R_ROW_FB3", "x": 900, "y": 520, "nets": {"1": "ROW3", "2": "ROW_FB3"}}, {"ref": "C_ROW_HF3", "x": 680, "y": 575, "nets": {"1": "ROW_DRV3", "2": "ROW_FB3"}}, {"ref": "R_SEL_PD3", "x": 900, "y": 575, "nets": {"1": "ROW_SEL3", "2": "GND"}}, {"ref": "C_ROW_OP", "x": 180, "y": 480, "nets": {"1": "V5", "2": "GND"}}, {"ref": "C_MUX", "x": 450, "y": 480, "nets": {"1": "V5", "2": "GND"}}, {"ref": "J2", "x": 200, "y": 635, "nets": {"1": "ROW0", "2": "ROW1", "3": "ROW2", "4": "ROW3", "5": "COL0", "6": "COL1", "7": "COL2", "8": "COL3"}}]};
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
