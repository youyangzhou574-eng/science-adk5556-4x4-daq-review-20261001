const plan={"project": "8da2f1e3f2c9045bf431c2cbe7ea31503e15ca88fefd5a6569f5a51a3d3c9788", "page": {"uuid": "5f9caa2aebdf4356", "index": 3, "name": "ADS8684_Decoupling"}, "parts": [{"id": "75152819ec31fd9b", "ref": "C_ADCA1", "type": "part", "name": "100nF", "sub": "GRM188R71C104KA01D.1", "association": {"libraryUuid": "0819f05c4eef4c71ace90d822a990e87", "uuid": "582e6743b52f4d549473833313fcf026"}, "footprint": {"uuid": "e1806bcee69fe169", "libraryUuid": "0819f05c4eef4c71ace90d822a990e87", "name": "C0603"}, "props": {"PCB Layer": "Default", "LCSC Part Name": "100nF ±10% 16V", "Supplier Footprint": "0603", "JLCPCB Part Class": "Extended Part", "Datasheet": "https://atta.szlcsc.com/upload/public/pdf/source/20161108/1478586365848.pdf", "Value": "100nF", "Tolerance": "±10%", "Voltage Rated": "16V", "Temperature Coefficient": "X7R", "Description": "容值:100nF;精度:±10%;额定电压:16V;材质(温度系数):X7R;", "Review Status": "R2 REVIEW / DYNAMIC_VALIDATION_HOLD / FAULT_PROTECTION_HOLD", "Circuit Role": ""}, "pins": [{"number": "1", "name": "1", "x": 265, "y": 760, "nc": false}, {"number": "2", "name": "2", "x": 295, "y": 760, "nc": false}], "page": 3, "nets": {"1": "V5", "2": "GND"}, "value": "100nF", "dnp": false, "layoutIndex": 16}, {"id": "3743f05c0eed984f", "ref": "C_ADCA2", "type": "part", "name": "100nF", "sub": "GRM188R71C104KA01D.1", "association": {"libraryUuid": "0819f05c4eef4c71ace90d822a990e87", "uuid": "582e6743b52f4d549473833313fcf026"}, "footprint": {"uuid": "e1806bcee69fe169", "libraryUuid": "0819f05c4eef4c71ace90d822a990e87", "name": "C0603"}, "props": {"PCB Layer": "Default", "LCSC Part Name": "100nF ±10% 16V", "Supplier Footprint": "0603", "JLCPCB Part Class": "Extended Part", "Datasheet": "https://atta.szlcsc.com/upload/public/pdf/source/20161108/1478586365848.pdf", "Value": "100nF", "Tolerance": "±10%", "Voltage Rated": "16V", "Temperature Coefficient": "X7R", "Description": "容值:100nF;精度:±10%;额定电压:16V;材质(温度系数):X7R;", "Review Status": "R2 REVIEW / DYNAMIC_VALIDATION_HOLD / FAULT_PROTECTION_HOLD", "Circuit Role": ""}, "pins": [{"number": "1", "name": "1", "x": 715, "y": 760, "nc": false}, {"number": "2", "name": "2", "x": 745, "y": 760, "nc": false}], "page": 3, "nets": {"1": "V5", "2": "GND"}, "value": "100nF", "dnp": false, "layoutIndex": 17}, {"id": "12fd8dd337710ec7", "ref": "C_ADCD", "type": "part", "name": "100nF", "sub": "GRM188R71C104KA01D.1", "association": {"libraryUuid": "0819f05c4eef4c71ace90d822a990e87", "uuid": "582e6743b52f4d549473833313fcf026"}, "footprint": {"uuid": "e1806bcee69fe169", "libraryUuid": "0819f05c4eef4c71ace90d822a990e87", "name": "C0603"}, "props": {"PCB Layer": "Default", "LCSC Part Name": "100nF ±10% 16V", "Supplier Footprint": "0603", "JLCPCB Part Class": "Extended Part", "Datasheet": "https://atta.szlcsc.com/upload/public/pdf/source/20161108/1478586365848.pdf", "Value": "100nF", "Tolerance": "±10%", "Voltage Rated": "16V", "Temperature Coefficient": "X7R", "Description": "容值:100nF;精度:±10%;额定电压:16V;材质(温度系数):X7R;", "Review Status": "R2 REVIEW / DYNAMIC_VALIDATION_HOLD / FAULT_PROTECTION_HOLD", "Circuit Role": ""}, "pins": [{"number": "1", "name": "1", "x": 1165, "y": 760, "nc": false}, {"number": "2", "name": "2", "x": 1195, "y": 760, "nc": false}], "page": 3, "nets": {"1": "V3V3", "2": "GND"}, "value": "100nF", "dnp": false, "layoutIndex": 18}], "clean": false, "save": false}; const result={page:plan.page,status:'STARTED',parts:[],deleted:{},saved:false};
try{
 const project=await eda.dmt_Project.getCurrentProjectInfo();if(project.uuid!==plan.project)throw Error('Wrong isolated C project');
 await eda.dmt_EditorControl.openDocument(plan.page.uuid);
 // Current working-copy page only; no PCB document and no old source session.
 const keep=new Set(plan.parts.filter(q=>q.ref==='J2').map(q=>q.ref));
 if(plan.clean){
 const all=await eda.sch_PrimitiveComponent.getAll();
 for(const c of all){if(c.getState_ComponentType()==='sheet'||keep.has(c.getState_Designator()))continue;if(!await eda.sch_PrimitiveComponent.delete(c))throw Error('Component delete failed');result.deleted.component=(result.deleted.component||0)+1;}
 for(const w of await eda.sch_PrimitiveWire.getAll()){if(!await eda.sch_PrimitiveWire.delete(w))throw Error('Wire delete failed');result.deleted.wire=(result.deleted.wire||0)+1;}
 for(const t of await eda.sch_PrimitiveText.getAll()){if(!await eda.sch_PrimitiveText.delete(t))throw Error('Text delete failed');result.deleted.text=(result.deleted.text||0)+1;}
 for(const c of await eda.sch_PrimitiveComponent.getAll())if(c.getState_ComponentType()==='sheet'){
  const border=(await eda.sch_PrimitiveAttribute.getAll(c.getState_PrimitiveId())).find(a=>a.getState_Key()==='Border');if(border)await eda.sch_PrimitiveAttribute.modify(border.getState_PrimitiveId(),{value:'0'});
 }
 await eda.sch_PrimitiveText.create(80,30,'C CANDIDATE - NOT FOR USE - '+plan.page.name+' / electrical and material HOLD');

}
 for(let i=0;i<plan.parts.length;i++){
  const q=plan.parts[i];let c;
  if(q.ref==='J2'){c=(await eda.sch_PrimitiveComponent.getAll()).find(v=>v.getState_Designator()==='J2');if(!c)throw Error('Inherited J2 missing');}
  else{c=await eda.sch_PrimitiveComponent.create(q.association,350+((q.layoutIndex)%4)*560,220+Math.floor(q.layoutIndex/4)*420,q.sub,0,false,true,true);if(!c)throw Error('Create '+q.ref);}
  const m=await eda.sch_PrimitiveComponent.modify(c.getState_PrimitiveId(),{designator:q.ref,name:q.value,otherProperty:{...c.getState_OtherProperty(),Value:q.value,'Review Status':'C CANDIDATE / NOT FOR USE / POWER_AND_DYNAMIC_HOLD','Add into BOM':q.dnp?'no':'yes','DNP':q.dnp?'yes':'no','Circuit Role':q.role||'C candidate; no PCB/bench release'}});if(!m)throw Error('Metadata '+q.ref);
  const ps=await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(m.getState_PrimitiveId());
  const actual=ps.map(v=>({number:String(v.getState_PinNumber()),name:v.getState_PinName(),x:v.getState_X(),y:v.getState_Y(),rotation:v.getState_Rotation()}));
  if(actual.length!==Object.keys(q.nets).length||new Set(actual.map(x=>x.number)).size!==actual.length||actual.some(x=>!(x.number in q.nets)))throw Error('Actual pin set mismatch '+q.ref+' '+JSON.stringify(actual));
  for(let z=0;z<ps.length;z++){
   const a=actual[z],net=q.nets[a.number];
   if(net===null){await ps[z].setState_NoConnected(true).done();continue;}
   await ps[z].setState_NoConnected(false).done();
   const length=q.ref.match(/^U\d+$/)?120:65;const delta={0:[length,0],180:[-length,0],90:[0,length],270:[0,-length]}[a.rotation];if(!delta)throw Error('Unknown pin rotation');
   const port=await eda.sch_PrimitiveComponent.createNetPort('BI',net,a.x+delta[0],a.y+delta[1],a.rotation,false);if(!port)throw Error('Port '+q.ref);
   const pp=await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(port.getState_PrimitiveId());if(pp.length!==1)throw Error('Port anchor');
   const w=await eda.sch_PrimitiveWire.create([[a.x,a.y,pp[0].getState_X(),pp[0].getState_Y()]],net);if(!w)throw Error('Wire '+q.ref);
   for(const attr of await eda.sch_PrimitiveAttribute.getAll(w.getState_PrimitiveId()))if(['NET','Net'].includes(attr.getState_Key()))await eda.sch_PrimitiveAttribute.modify(attr.getState_PrimitiveId(),{valueVisible:false,keyVisible:false});
  }
  result.parts.push({ref:q.ref,id:m.getState_PrimitiveId(),actualPins:actual,planned:q.nets,association:m.getState_Component(),footprint:m.getState_Footprint(),dnp:q.dnp});
 }
 if(plan.save){result.saved=await eda.sch_Document.save();if(result.saved!==true)throw Error('Save failed');}
 result.status='PAGE_CANDIDATE_CREATED';return result;
}catch(e){result.status='STOP_NATIVE_IMPLEMENTATION_ERROR';result.error={name:e.name,message:e.message,stack:e.stack};return result;}
