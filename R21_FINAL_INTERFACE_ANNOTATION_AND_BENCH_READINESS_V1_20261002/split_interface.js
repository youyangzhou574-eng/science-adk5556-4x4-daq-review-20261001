const pr=await eda.dmt_Project.getCurrentProjectInfo();if(pr.uuid!=="02ea8fb2e66040299c1c16192899224e7332b1b47147f009f3b0e759a20328af")throw Error('Wrong10');
await eda.dmt_EditorControl.openDocument('52a8a60e5711e55b');
const all=await eda.sch_PrimitiveComponent.getAll(),wires=await eda.sch_PrimitiveWire.getAll();const plans=[];
const close=(a,b)=>Math.abs(a-b)<1e-5;
const ports=[];for(const c of all)if(c.getState_ComponentType()==='netport'){
 const p=(await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId()))[0];ports.push({c,x:p.getState_X(),y:p.getState_Y()});
}
for(const [ref,net]of [['J3','V3V3_EXT_SWD'],['R_J3_1','V3V3_EXT_SWD'],['J4','V3V3_EXT_UART'],['R_J4_1','V3V3_EXT_UART']]){
 const c=all.find(c=>c.getState_ComponentType()==='part'&&c.getState_Designator()===ref);if(!c)throw Error('Missing'+ref);
 const p=(await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId())).find(p=>String(p.getState_PinNumber())==='1');const x=p.getState_X(),y=p.getState_Y(),found=[];
 for(const w of wires){const raw=w.getState_Line();for(const line of(Array.isArray(raw[0])?raw:[raw])){
 if(close(line[0],x)&&close(line[1],y))found.push({w,far:[line.at(-2),line.at(-1)]});
 else if(close(line.at(-2),x)&&close(line.at(-1),y))found.push({w,far:[line[0],line[1]]});
 }}
 if(found.length!==1)throw Error('Expected unique stub '+ref);
 const stub=found[0],port=ports.filter(q=>close(q.x,stub.far[0])&&close(q.y,stub.far[1]));
 if(port.length!==1)throw Error('Expected unique exact endpoint NetPort '+ref);
 plans.push({ref,net,w:stub.w,old:port[0].c,x:stub.far[0],y:stub.far[1],rot:port[0].c.getState_Rotation()});
}
if(new Set(plans.map(p=>p.old.getState_PrimitiveId())).size!==4)throw Error('Not four unique ports');
const changes=[];
for(const p of plans){
 const oldId=p.old.getState_PrimitiveId();if(!await eda.sch_PrimitiveComponent.delete(p.old))throw Error('Portdelete '+p.ref);
 const rebuilt=await eda.sch_PrimitiveComponent.createNetPort('BI',p.net,p.x,p.y,p.rot,false);if(!rebuilt)throw Error('Portcreate '+p.ref);
 const pin=(await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(rebuilt.getState_PrimitiveId()))[0];if(!close(pin.getState_X(),p.x)||!close(pin.getState_Y(),p.y))throw Error('Anchor changed');
 await p.w.setState_Net(p.net).done();changes.push({ref:p.ref,pin:'1',net:p.net,x:p.x,y:p.y,oldId,newId:rebuilt.getState_PrimitiveId()});
}
const saved=await eda.sch_Document.save();if(saved!==true)throw Error('Savefailed');return {project:pr.uuid,changes,saved};
