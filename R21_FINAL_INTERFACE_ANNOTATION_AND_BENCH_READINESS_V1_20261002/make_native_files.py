import pathlib,json
P=pathlib.Path(__file__).resolve().parent;O=P.parent/'R21_NATIVE_PIN_NET_CORRECTION_AND_FINAL_DRAWING_V1'
h=json.loads((P/'CONTEXT_A.json').read_text('utf8'))['parsed']['value'];pr=h['project']['uuid']
assert h['project']['friendlyName']=='SCIENCE_ADK5556_4X4_R21_FINAL_INTERFACE_WORK'
ctx={'project_uuid':pr,'pages':[dict(uuid=q['uuid'],index=i,name=q['name'])for i,q in enumerate(h['schematics'][0]['page'])]}
(P/'PROJECT_CONTEXT.json').write_text(json.dumps(ctx,indent=2)+'\n','utf8')
for a,b in [('capture.js','capture_warm.js'),('capture_cold_final.js','capture_cold_final.js'),('preclose_snapshot.js','preclose_snapshot.js'),('export_pdf.js','export_pdf.js')]:
 s=(O/a).read_text('utf8').replace('b771f646994e1e87ccac719bcaeddd7f79898452652eb8c78e76c7463539d085',pr)
 if b=='capture_cold_final.js':
  # all three actual File exports share the single cold-final capture invocation;
  # PDF predebit is charged separately before this invocation.
  extra="const pf=await eda.sch_ManufactureData.getExportDocumentFile('SCIENCE_ADK5556_4X4_R21_FINAL_INTERFACE_REVIEW','PDF',{theme:'Black on White',lineWidth:'Default',size:'Original Size'},'Current Schematic',{range:'All',outputMethod:'Merged sheet'});if(!pf)throw Error('No PDF');const pb=new Uint8Array(await pf.arrayBuffer());let ps='';for(let i=0;i<pb.length;i+=16384)ps+=String.fromCharCode(...pb.subarray(i,i+16384));const pdf={name:pf.name,size:pf.size,constructor:pf.constructor.name,tag:Object.prototype.toString.call(pf),base64:btoa(ps)};"
  s=s.replace('const file=',extra+'const file=',1).replace('return {project,pages,native,actualFile:', 'return {project,pages,native,pdf,actualFile:')
 (P/b).write_text(s,'utf8')
script="""const pr=await eda.dmt_Project.getCurrentProjectInfo();if(pr.uuid!==PROJECT)throw Error('Wrong10');
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
"""
(P/'split_interface.js').write_text(script.replace('PROJECT',json.dumps(pr),1),'utf8')
notes="""const pr=await eda.dmt_Project.getCurrentProjectInfo();if(pr.uuid!==PROJECT)throw Error('Wrong10');
await eda.dmt_EditorControl.openDocument('52a8a60e5711e55b');
const t=(await eda.sch_PrimitiveText.getAll()).sort((a,b)=>a.getState_Y()-b.getState_Y());if(t.length!==4)throw Error('Expected4 notes');
const texts=['R2.1 REVIEW ONLY - MCU interfaces: independent SWD/UART 3V3 SENSE - 5/6','J3.1/J4.1 are sense only (NOT power inputs), each4.99k; NRST1k OD/OC VOL<=0.4V HiZ','8state/288transfers32dummy256valid; epoch/replay/progress/two good frames; 100fps BENCH_PENDING','SWD series4.99k retained: start about100kHz; normal1-7k/10%; 300us/calibration BENCH_PENDING'];
const before=await eda.sys_FileManager.getDocumentSource();
for(let i=0;i<4;i++)await eda.sch_PrimitiveText.modify(t[i],{value:texts[i]});
const saved=await eda.sch_Document.save();if(saved!==true)throw Error('Savefailed');return {project:pr.uuid,texts,before,after:await eda.sys_FileManager.getDocumentSource(),saved,attemptCount:1};
"""
(P/'notes_once.js').write_text(notes.replace('PROJECT',json.dumps(pr),1),'utf8')
print(json.dumps({'project':pr,'source_TEXT_property':'value','notesSingleAttempt':'modify(value), source authority; no fallback API research'}))
