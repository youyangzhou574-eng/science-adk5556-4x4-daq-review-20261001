const d={"project": "b771f646994e1e87ccac719bcaeddd7f79898452652eb8c78e76c7463539d085", "page": {"uuid": "49bb518d907ff185", "index": 2, "name": "Continuous_Column_TIAs"}, "added": [{"ref": "C_TIA_HF0", "device": "GRM1885C1H220JA01D", "device_uuid": "3d240fa64e4f48b1bdeb9f0c19efceb7", "library_uuid": "0819f05c4eef4c71ace90d822a990e87", "page": 2, "x": 280, "y": 1780, "rotation": 0, "subpart": "GRM1885C1H220JA01D.1", "nets": {"1": "TIA_DRV0", "2": "COL_SENSE0"}, "value": "22pF 50V C0G", "role": "08 approved mature feedback ECO; actual bench pending"}, {"ref": "C_TIA_HF1", "device": "GRM1885C1H220JA01D", "device_uuid": "3d240fa64e4f48b1bdeb9f0c19efceb7", "library_uuid": "0819f05c4eef4c71ace90d822a990e87", "page": 2, "x": 730, "y": 1780, "rotation": 0, "subpart": "GRM1885C1H220JA01D.1", "nets": {"1": "TIA_DRV1", "2": "COL_SENSE1"}, "value": "22pF 50V C0G", "role": "08 approved mature feedback ECO; actual bench pending"}, {"ref": "C_TIA_HF2", "device": "GRM1885C1H220JA01D", "device_uuid": "3d240fa64e4f48b1bdeb9f0c19efceb7", "library_uuid": "0819f05c4eef4c71ace90d822a990e87", "page": 2, "x": 1180, "y": 1780, "rotation": 0, "subpart": "GRM1885C1H220JA01D.1", "nets": {"1": "TIA_DRV2", "2": "COL_SENSE2"}, "value": "22pF 50V C0G", "role": "08 approved mature feedback ECO; actual bench pending"}, {"ref": "C_TIA_HF3", "device": "GRM1885C1H220JA01D", "device_uuid": "3d240fa64e4f48b1bdeb9f0c19efceb7", "library_uuid": "0819f05c4eef4c71ace90d822a990e87", "page": 2, "x": 1630, "y": 1780, "rotation": 0, "subpart": "GRM1885C1H220JA01D.1", "nets": {"1": "TIA_DRV3", "2": "COL_SENSE3"}, "value": "22pF 50V C0G", "role": "08 approved mature feedback ECO; actual bench pending"}], "reset": {"ref": "R_J3_5", "device": "0603WAF1001T5E", "device_uuid": "18db11499a04403ba8c98e2f7a687fbc", "library_uuid": "0819f05c4eef4c71ace90d822a990e87", "page": 4, "x": 280, "y": 1040, "rotation": 0, "subpart": "0603WAF1001T5E.1", "nets": {"1": "MCU_NRST_EXT", "2": "PGOOD"}, "value": "1k 1%", "role": "Direct external OD/OC reset, VOL<=0.4V, release HiZ; no push-pull high"}};
const pr=await eda.dmt_Project.getCurrentProjectInfo();if(pr.uuid!==d.project)throw Error('Wrong workcopy');
await eda.dmt_EditorControl.openDocument(d.page.uuid);
const result={page:d.page,changes:[]};
const all=await eda.sch_PrimitiveComponent.getAll();
function close(a,b){return Math.abs(a-b)<1e-5;}
async function pinWire(pin){
 const x=pin.getState_X(),y=pin.getState_Y();const found=[];
 for(const w of await eda.sch_PrimitiveWire.getAll()){
 const raw=w.getState_Line();for(const line of (Array.isArray(raw[0])?raw:[raw])){
  if(close(line[0],x)&&close(line[1],y))found.push({wire:w,line,far:[line.at(-2),line.at(-1)]});
  else if(close(line.at(-2),x)&&close(line.at(-1),y))found.push({wire:w,line,far:[line[0],line[1]]});
 }
 }
 if(found.length!==1)throw Error('Expected one existing pin stub');return found[0];
}
async function add(q){
 let c=await eda.sch_PrimitiveComponent.create({libraryUuid:q.library_uuid,uuid:q.device_uuid},q.x,q.y,q.subpart,0,false,true,true);
 if(!c)throw Error('Create '+q.ref);
 let pins=await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId());
 if(pins.length!==2)throw Error('New passive pin count');
 if(close(pins[0].getState_X(),pins[1].getState_X())){c=await eda.sch_PrimitiveComponent.modify(c,{rotation:90});pins=await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId());}
 if(!close(pins[0].getState_Y(),pins[1].getState_Y()))throw Error('Passive must be horizontal');
 c=await eda.sch_PrimitiveComponent.modify(c,{designator:q.ref,name:q.value,otherProperty:{...c.getState_OtherProperty(),Value:q.value,'Circuit Role':q.role,'Review Status':'R2.1 engineering review; BENCH_PENDING'}});
 for(const pin of pins){const number=String(pin.getState_PinNumber()),net=q.nets[number];if(!net)throw Error('New pin net');
  const x=pin.getState_X(),y=pin.getState_Y(),ex=x+(x<q.x?-55:55);
  const port=await eda.sch_PrimitiveComponent.createNetPort('BI',net,ex,y,ex<x?180:0,false);if(!port)throw Error('New port');
  const anchor=(await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(port.getState_PrimitiveId()))[0];
  if(!close(anchor.getState_X(),ex)||!close(anchor.getState_Y(),y))throw Error('Port anchor mismatch');
  if(!await eda.sch_PrimitiveWire.create([[x,y,ex,y]],net))throw Error('New wire');
 }
 result.changes.push({ref:q.ref,action:'created',association:c.getState_Component(),footprint:c.getState_Footprint()});return c;
}
if(d.page.index===0){
 const c=all.find(x=>x.getState_Designator()==='U3'&&x.getState_ComponentType()==='part');if(!c)throw Error('Missing U3');
 for(const [number,net] of [['2','VCM_FB'],['6','VEXC_FB']]){
  const pin=(await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId())).find(p=>String(p.getState_PinNumber())===number);const stub=await pinWire(pin);
  const ports=[];for(const p of all)if(p.getState_ComponentType()==='netport'){
   const pp=(await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(p.getState_PrimitiveId()))[0];if(close(pp.getState_X(),stub.far[0])&&close(pp.getState_Y(),stub.far[1]))ports.push(p);
  }
  if(ports.length!==1)throw Error('Feedback port identity');const rot=ports[0].getState_Rotation();if(!await eda.sch_PrimitiveComponent.delete(ports[0]))throw Error('Delete old feedback port');const rebuilt=await eda.sch_PrimitiveComponent.createNetPort('BI',net,stub.far[0],stub.far[1],rot,false);if(!rebuilt)throw Error('Rebuild feedback port');const a=(await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(rebuilt.getState_PrimitiveId()))[0];if(!close(a.getState_X(),stub.far[0])||!close(a.getState_Y(),stub.far[1]))throw Error('Feedback anchor changed');await stub.wire.setState_Net(net).done();result.changes.push({ref:'U3',pin:number,net});
 }
}
if(d.page.index===4){
 const old=all.find(x=>x.getState_Designator()==='R_J3_5'&&x.getState_ComponentType()==='part');if(!old)throw Error('Missing reset resistor');
 const q=d.reset;const stubs={};for(const p of await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(old.getState_PrimitiveId()))stubs[String(p.getState_PinNumber())]=await pinWire(p);
 if(!await eda.sch_PrimitiveComponent.delete(old))throw Error('Remove old4k99 reset');
 let c=await eda.sch_PrimitiveComponent.create({libraryUuid:q.library_uuid,uuid:q.device_uuid},q.x,q.y,q.subpart,0,false,true,true);
 c=await eda.sch_PrimitiveComponent.modify(c,{designator:q.ref,name:q.value,otherProperty:{...c.getState_OtherProperty(),Value:q.value,'Circuit Role':q.role}});
 for(const p of await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId())){const stub=stubs[String(p.getState_PinNumber())];if(!stub)throw Error('Reset pin mismatch');const x=p.getState_X(),y=p.getState_Y(),[fx,fy]=stub.far;const line=close(y,fy)?[x,y,fx,fy]:[x,y,fx,y,fx,fy];if(!await eda.sch_PrimitiveWire.modify(stub.wire,{line:[line]}))throw Error('Reset stub edit');}
 result.changes.push({ref:q.ref,action:'physical device4k99->1k',association:c.getState_Component(),footprint:c.getState_Footprint()});
}
for(const q of d.added){if(all.some(x=>x.getState_Designator()===q.ref))throw Error('Duplicate new ref');await add(q);}
if(d.page.index===2)for(const c of all)if(/^C_ADC[0-3]$/.test(c.getState_Designator())){await eda.sch_PrimitiveComponent.modify(c,{name:'10nF X7R',otherProperty:{...c.getState_OtherProperty(),Value:'10nF X7R'}});result.changes.push({ref:c.getState_Designator(),action:'repair native Value'});}

result.saved=await eda.sch_Document.save();if(result.saved!==true)throw Error('Save failed');return result;
