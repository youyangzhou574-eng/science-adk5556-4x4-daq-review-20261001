
const plan={"project": "f584056ea8f7cc74a210f932891fde19f1d1518be7e7f4466d0c7acd11c29efe", "page": {"uuid": "802bf258e0d38cab", "index": 1, "name": "Rows_8lead_Interface"}, "parts": [{"ref": "J2", "device": "HDR-M_2.54_1x8P", "device_uuid": "fd554b15b6eb4d6f90f5fd338a8ff700", "library_uuid": "0819f05c4eef4c71ace90d822a990e87", "page": 1, "x": 1180, "y": 1180, "rotation": 0, "subpart": "Header-Male-2.54_1x8.1", "nets": {"1": "ROW0", "2": "ROW1", "3": "ROW2", "4": "ROW3", "5": "COL0", "6": "COL1", "7": "COL2", "8": "COL3"}, "value": null, "role": "FIXED8-wire external4x4 array; no16 sensor resistors mounted on this board"}, {"ref": "D_ROW0", "device": "BAT54S,215", "device_uuid": "862039df28364e9395be8ec3e804cf6f", "library_uuid": "0819f05c4eef4c71ace90d822a990e87", "page": 1, "x": 1630, "y": 1180, "rotation": 0, "subpart": "BAT54S,215.1", "nets": {"1": "GND", "2": "V5", "3": "ROW_DRV0"}, "value": null, "role": "Output/connector rail clamp; leakage and Vf/thermal corners remain HOLD"}, {"ref": "D_ROW1", "device": "BAT54S,215", "device_uuid": "862039df28364e9395be8ec3e804cf6f", "library_uuid": "0819f05c4eef4c71ace90d822a990e87", "page": 1, "x": 280, "y": 1320, "rotation": 0, "subpart": "BAT54S,215.1", "nets": {"1": "GND", "2": "V5", "3": "ROW_DRV1"}, "value": null, "role": "Output/connector rail clamp; leakage and Vf/thermal corners remain HOLD"}, {"ref": "D_ROW2", "device": "BAT54S,215", "device_uuid": "862039df28364e9395be8ec3e804cf6f", "library_uuid": "0819f05c4eef4c71ace90d822a990e87", "page": 1, "x": 730, "y": 1320, "rotation": 0, "subpart": "BAT54S,215.1", "nets": {"1": "GND", "2": "V5", "3": "ROW_DRV2"}, "value": null, "role": "Output/connector rail clamp; leakage and Vf/thermal corners remain HOLD"}, {"ref": "D_ROW3", "device": "BAT54S,215", "device_uuid": "862039df28364e9395be8ec3e804cf6f", "library_uuid": "0819f05c4eef4c71ace90d822a990e87", "page": 1, "x": 1180, "y": 1320, "rotation": 0, "subpart": "BAT54S,215.1", "nets": {"1": "GND", "2": "V5", "3": "ROW_DRV3"}, "value": null, "role": "Output/connector rail clamp; leakage and Vf/thermal corners remain HOLD"}, {"ref": "U14", "device": "SN74LVC08APWR", "device_uuid": "17ad71c980e24dfb9b9615c96c192408", "library_uuid": "0819f05c4eef4c71ace90d822a990e87", "page": 1, "x": 1590, "y": 260, "rotation": 0, "subpart": "SN74LVC08APWR.1", "nets": {"1": "HW_ENABLE", "2": "MCU_ROW0", "3": "ROW_SEL0", "4": "HW_ENABLE", "5": "MCU_ROW1", "6": "ROW_SEL1", "7": "GND", "8": "ROW_SEL2", "9": "HW_ENABLE", "10": "MCU_ROW2", "11": "ROW_SEL3", "12": "HW_ENABLE", "13": "MCU_ROW3", "14": "V3V3"}, "value": null, "role": ""}, {"ref": "C_U14", "device": "GRM188R71C104KA01D", "device_uuid": "582e6743b52f4d549473833313fcf026", "library_uuid": "0819f05c4eef4c71ace90d822a990e87", "page": 1, "x": 1630, "y": 1320, "rotation": 0, "subpart": "GRM188R71C104KA01D.1", "nets": {"1": "V3V3", "2": "GND"}, "value": "100nF", "role": ""}], "height": 1500, "notes": ["Rs1k / Rb4.99k / Ch100pF candidate; ideal 300us screening PASS", "SEL = MCU_ROW AND HW_ENABLE; HW_ENABLE = PGOOD AND MCU_ENABLE", "Eight sensor leads only; no mounted16 sensor resistors; clamps do not establish whole-board fault PASS"], "first": false, "last": true};
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
   if(a.rotation===0)ox=length;else if(a.rotation===180)ox=-length;else oy=Math.sign(a.y-q.y)*length;
   const mark=await eda.sch_PrimitiveComponent.createNetPort('BI',net,a.x+ox,a.y+oy,ox<0?180:ox>0?0:oy>0?90:270,false);if(!mark)throw Error('Port');
   const mp=await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(mark.getState_PrimitiveId());if(mp.length!==1)throw Error('Port anchor');
   const rnd=v=>Math.round(v*1e6)/1e6,mx=rnd(mp[0].getState_X()),my=rnd(mp[0].getState_Y());const line=[rnd(a.x),rnd(a.y),mx,my];
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
