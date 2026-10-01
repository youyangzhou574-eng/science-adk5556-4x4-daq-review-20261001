
const plan={"project": "f584056ea8f7cc74a210f932891fde19f1d1518be7e7f4466d0c7acd11c29efe", "page": {"uuid": "52a8a60e5711e55b", "index": 4, "name": "MCU_Protected_Interfaces"}, "parts": [{"ref": "U7", "device": "STM32G031K8T6", "device_uuid": "d6b55ece5afe47718d825be9cafc6dc2", "library_uuid": "0819f05c4eef4c71ace90d822a990e87", "page": 4, "x": 350, "y": 260, "rotation": 0, "subpart": "STM32G031K8T6.1", "nets": {"1": null, "2": null, "3": null, "4": "V3V3", "5": "GND", "6": "PGOOD", "7": "MCU_ROW0", "8": "MCU_ROW1", "9": "MCU_ROW2", "10": "MCU_ROW3", "11": "ADC_CS_N", "12": "SPI_SCLK", "13": "SPI_MISO", "14": "SPI_MOSI", "15": "MCU_ADC_RESET", "16": "MCU_ENABLE", "17": null, "18": null, "19": "UART_TX", "20": null, "21": "UART_RX", "22": null, "23": null, "24": "SWDIO", "25": "SWCLK", "26": null, "27": null, "28": null, "29": null, "30": null, "31": null, "32": null}, "value": null, "role": ""}, {"ref": "J3", "device": "HDR-M_2.54_1x6P", "device_uuid": "8713123b624d4455bcbe38688209bdf0", "library_uuid": "0819f05c4eef4c71ace90d822a990e87", "page": 4, "x": 280, "y": 620, "rotation": 0, "subpart": "Header-Male-2.54_1x6.1", "nets": {"1": "V3V3_EXT", "2": "GND", "3": "SWDIO_EXT", "4": "SWCLK_EXT", "5": "MCU_NRST_EXT", "6": null}, "value": null, "role": "SWD/programming;3V3 sense, no external5V"}, {"ref": "J4", "device": "HDR-M_2.54_1x4P", "device_uuid": "d5e86a4f70d24c6c950b9ff10d30894b", "library_uuid": "0819f05c4eef4c71ace90d822a990e87", "page": 4, "x": 730, "y": 620, "rotation": 0, "subpart": "PZ254V-11-04P.1", "nets": {"1": "V3V3_EXT", "2": "GND", "3": "UART_TX_EXT", "4": "UART_RX_EXT"}, "value": null, "role": "3V3 UART logic only; no directRS232/5V UART"}, {"ref": "R_RST", "device": "RT0603BRD0710KL", "device_uuid": "3840b7e554aa441f90223c083eebd79a", "library_uuid": "0819f05c4eef4c71ace90d822a990e87", "page": 4, "x": 1180, "y": 620, "rotation": 0, "subpart": "RT0603BRD0710KL.1", "nets": {"1": "V3V3", "2": "PGOOD"}, "value": "10k 0.1%", "role": ""}, {"ref": "C_RST", "device": "GRM188R71C104KA01D", "device_uuid": "582e6743b52f4d549473833313fcf026", "library_uuid": "0819f05c4eef4c71ace90d822a990e87", "page": 4, "x": 1630, "y": 620, "rotation": 0, "subpart": "GRM188R71C104KA01D.1", "nets": {"1": "V3V3", "2": "GND"}, "value": "100nF", "role": "Moved reset RC capacitor to auxiliary supply decoupling; supervisor CT supplies reset delay"}, {"ref": "C_MCU1", "device": "GRM188R71C104KA01D", "device_uuid": "582e6743b52f4d549473833313fcf026", "library_uuid": "0819f05c4eef4c71ace90d822a990e87", "page": 4, "x": 280, "y": 760, "rotation": 0, "subpart": "GRM188R71C104KA01D.1", "nets": {"1": "V3V3", "2": "GND"}, "value": "100nF", "role": ""}, {"ref": "C_MCU_BULK", "device": "GRM188R61C105KA93D", "device_uuid": "1db1d485da63414a91f474e833691800", "library_uuid": "0819f05c4eef4c71ace90d822a990e87", "page": 4, "x": 730, "y": 760, "rotation": 0, "subpart": "GRM188R61C105KA93D.1", "nets": {"1": "V3V3", "2": "GND"}, "value": "1uF", "role": ""}, {"ref": "R_J3_1", "device": "RT0603BRD074K99L", "device_uuid": "e3fb4324469a40728b83810eaa907b40", "library_uuid": "0819f05c4eef4c71ace90d822a990e87", "page": 4, "x": 1180, "y": 760, "rotation": 0, "subpart": "RT0603BRD074K99L.1", "nets": {"1": "V3V3_EXT", "2": "V3V3"}, "value": "4.99k 0.1%", "role": "External probe/programmer no board power input; current limited even on sense pins"}, {"ref": "D_J3_1", "device": "BAT54S,215", "device_uuid": "862039df28364e9395be8ec3e804cf6f", "library_uuid": "0819f05c4eef4c71ace90d822a990e87", "page": 4, "x": 1630, "y": 760, "rotation": 0, "subpart": "BAT54S,215.1", "nets": {"1": "GND", "2": "V3V3", "3": "V3V3"}, "value": null, "role": "Output/connector rail clamp; leakage and Vf/thermal corners remain HOLD"}, {"ref": "R_J3_3", "device": "RT0603BRD074K99L", "device_uuid": "e3fb4324469a40728b83810eaa907b40", "library_uuid": "0819f05c4eef4c71ace90d822a990e87", "page": 4, "x": 280, "y": 900, "rotation": 0, "subpart": "RT0603BRD074K99L.1", "nets": {"1": "SWDIO_EXT", "2": "SWDIO"}, "value": "4.99k 0.1%", "role": "External probe/programmer no board power input; current limited even on sense pins"}], "height": 1360, "notes": ["GPIO PB1 pin16 = MCU_ENABLE; PGOOD resets MCU; Schmitt reshapes hardware gate edge", "External SWD/UART/sense lines all4.99k current limited, clamps and rail sink", "Offline SPI: 0-5.12V range0x06, tagged48clk frames, 40kSPS / hardware timing HOLD"], "first": true, "last": false};
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
