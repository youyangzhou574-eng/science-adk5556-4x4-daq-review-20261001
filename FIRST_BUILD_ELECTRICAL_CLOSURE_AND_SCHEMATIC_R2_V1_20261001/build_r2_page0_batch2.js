
const plan={"project": "f584056ea8f7cc74a210f932891fde19f1d1518be7e7f4466d0c7acd11c29efe", "page": {"uuid": "595d5f2f11dee03d", "index": 0, "name": "Power_Reference"}, "parts": [{"ref": "R_VCM_ISO", "device": "0603WAF1001T5E", "device_uuid": "18db11499a04403ba8c98e2f7a687fbc", "library_uuid": "0819f05c4eef4c71ace90d822a990e87", "page": 0, "x": 730, "y": 1180, "rotation": 0, "subpart": "0603WAF1001T5E.1", "nets": {"1": "VCM_DRV", "2": "VCM"}, "value": "1k 1%", "role": "Feedback senses VCM after isolation"}, {"ref": "R_VEX_ISO", "device": "0603WAF1001T5E", "device_uuid": "18db11499a04403ba8c98e2f7a687fbc", "library_uuid": "0819f05c4eef4c71ace90d822a990e87", "page": 0, "x": 1180, "y": 1180, "rotation": 0, "subpart": "0603WAF1001T5E.1", "nets": {"1": "VEXC_DRV", "2": "VEXC"}, "value": "1k 1%", "role": "Feedback senses VEXC after isolation"}, {"ref": "D_VCM", "device": "BAT54S,215", "device_uuid": "862039df28364e9395be8ec3e804cf6f", "library_uuid": "0819f05c4eef4c71ace90d822a990e87", "page": 0, "x": 1630, "y": 1180, "rotation": 0, "subpart": "BAT54S,215.1", "nets": {"1": "GND", "2": "V5", "3": "VCM_DRV"}, "value": null, "role": "Output/connector rail clamp; leakage and Vf/thermal corners remain HOLD"}, {"ref": "D_VEX", "device": "BAT54S,215", "device_uuid": "862039df28364e9395be8ec3e804cf6f", "library_uuid": "0819f05c4eef4c71ace90d822a990e87", "page": 0, "x": 280, "y": 1320, "rotation": 0, "subpart": "BAT54S,215.1", "nets": {"1": "GND", "2": "V5", "3": "VEXC_DRV"}, "value": null, "role": "Output/connector rail clamp; leakage and Vf/thermal corners remain HOLD"}], "height": 1500, "notes": ["R2 REVIEW ONLY: 4x4 / 8 leads; VCM2.5V, VEXC2.25V, E0.25V, Rf4.99k", "Feedback senses VCM/VEXC after 1k isolation; macro stability HOLD", "Reference/supply capacitance and rail qualification: see page4/6 and report"], "first": false, "last": true};
const result={page:plan.page,parts:[],markers:[],wires:[],nc:[],status:'STARTED'};
try {
 const project=await eda.dmt_Project.getCurrentProjectInfo();if(project?.uuid!==plan.project)throw Error('Wrong R2 context');
 await eda.dmt_EditorControl.openDocument(plan.page.uuid);
 const pg=await eda.dmt_Schematic.getCurrentSchematicPageInfo();if(pg?.uuid!==plan.page.uuid)throw Error('Wrong page');
 if(plan.first){
  const initial=await eda.sch_PrimitiveComponent.getAll();if(initial.some(c=>c.getState_ComponentType()!=='sheet'))throw Error('Expected empty new page');
  await eda.dmt_Schematic.modifySchematicPageTitleBlock(false);
  // DMT custom-size edits returned a known error; use the real frame's existing Border attribute.
  // Suppress decorative frame only, while all explicit net labels, pin numbers and page headings remain.
  for(const c of initial)if(c.getState_ComponentType()==='sheet'){
   const attrs=await eda.sch_PrimitiveAttribute.getAll(c.getState_PrimitiveId());
   const border=attrs.find(a=>a.getState_Key()==='Border');if(!border)throw Error('No real Border property');
   const updated=await eda.sch_PrimitiveAttribute.modify(border.getState_PrimitiveId(),{value:'0'});if(!updated)throw Error('Border edit failed');
  }
  for(let i=0;i<plan.notes.length;i++)await eda.sch_PrimitiveText.create(80,55+i*23,plan.notes[i],0,null,null,12,i===0);
  await eda.sch_PrimitiveText.create(80,25,'R2 REVIEW ONLY - '+plan.page.name+' - '+(plan.page.index+1)+'/6',0,null,null,16,true);
 }
 const existing=new Set((await eda.sch_PrimitiveComponent.getAll()).map(c=>c.getState_Designator()));
 for(const q of plan.parts){
  if(existing.has(q.ref))throw Error('Duplicate ref '+q.ref);
  const c=await eda.sch_PrimitiveComponent.create({libraryUuid:q.library_uuid,uuid:q.device_uuid},q.x,q.y,q.subpart,0,false,true,true);if(!c)throw Error('Create '+q.ref);
  const m=await eda.sch_PrimitiveComponent.modify(c.getState_PrimitiveId(),{designator:q.ref,name:q.value||q.device,otherProperty:{...c.getState_OtherProperty(),'Review Status':'R2 REVIEW / DYNAMIC_VALIDATION_HOLD / FAULT_PROTECTION_HOLD',...(q.value?{Value:q.value}:{}),'Circuit Role':q.role}});if(!m)throw Error('Modify '+q.ref);
  const ps=await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(m.getState_PrimitiveId());
  const actual=ps.map(v=>({number:String(v.getState_PinNumber()),name:v.getState_PinName(),x:v.getState_X(),y:v.getState_Y(),rotation:v.getState_Rotation()}));
  if(actual.length!==Object.keys(q.nets).length||new Set(actual.map(x=>x.number)).size!==actual.length||actual.some(x=>!(x.number in q.nets)))throw Error('Real pin mismatch '+q.ref);
  result.parts.push({ref:q.ref,id:m.getState_PrimitiveId(),association:m.getState_Component(),footprint:m.getState_Footprint(),pins:actual});
  for(let i=0;i<ps.length;i++){
   const pin=ps[i],a=actual[i],net=q.nets[a.number];
   if(net===null){await pin.setState_NoConnected(true).done();result.nc.push({ref:q.ref,pin:a.number});continue;}
   let ox=0,oy=0;
   // Use actual inward pin direction and real net-port anchor; never infer opposite-angle semantics.
   const length=q.ref.startsWith('U')?110:55;
   if(a.rotation===0)ox=-length;else if(a.rotation===180)ox=length;else if(a.rotation===90)oy=-length;else if(a.rotation===270)oy=length;else throw Error('Unsupported pin angle');
   const mark=await eda.sch_PrimitiveComponent.createNetPort('BI',net,a.x+ox,a.y+oy,ox<0?180:oy<0?90:oy>0?270:0,false);if(!mark)throw Error('Port');
   const mp=await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(mark.getState_PrimitiveId());if(mp.length!==1)throw Error('Port anchor');
   const mx=mp[0].getState_X(),my=mp[0].getState_Y();const line=[a.x,a.y,mx,a.y];if(my!==a.y)line.push(mx,my);
   const w=await eda.sch_PrimitiveWire.create([line],net);if(!w)throw Error('Wire');
   // Ports retain visible net names. Remove only duplicated automatic wire text, not pin numbers or explicit network labels.
   for(const attr of await eda.sch_PrimitiveAttribute.getAll(w.getState_PrimitiveId())){
    if(attr.getState_Key()==='NET'||attr.getState_Key()==='Net')await eda.sch_PrimitiveAttribute.modify(attr.getState_PrimitiveId(),{valueVisible:false,keyVisible:false});
   }
   result.markers.push({ref:q.ref,pin:a.number,net,id:mark.getState_PrimitiveId(),x:mx,y:my});result.wires.push({ref:q.ref,pin:a.number,net,id:w.getState_PrimitiveId(),line});
  }
 }
 if(plan.last){result.saved=await eda.sch_Document.save();if(result.saved!==true)throw Error('Save did not return true');}
 result.status='BATCH_CREATED';return result;
}catch(e){result.status='STOP_NATIVE_BUILD_ERROR';result.error={name:e?.name,message:e?.message,stack:e?.stack};return result;}
