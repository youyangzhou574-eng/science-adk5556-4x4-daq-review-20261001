const ids=['9965fd7b16015eaf','1baf912db250d2de','a51b95c47c70bc0e','cd673e3782e532f6'];
const p=await eda.dmt_Project.getCurrentProjectInfo();if(!['74e664f7c1193aad2a35d2db078a1f226377acc149fbbc11d8b1a9f9638bea07','07975f0da1517bcd267595cda8361726b99324274473489c5a2f7c0530f33402'].includes(p?.uuid))throw Error('Wrong independent project');
const sch=await eda.dmt_Schematic.getAllSchematicsInfo();if(sch.length!==1||sch[0].uuid!=='0ccfdd809e468881'||sch[0].parentProjectUuid!==p.uuid||sch[0].page.length!==4||sch[0].page.some(v=>!ids.includes(v.uuid)||v.parentSchematicUuid!==sch[0].uuid))throw Error('Cold reopen parent/page provenance');
const pages=[];
for(const id of ids){
 await eda.dmt_EditorControl.openDocument(id);
 const pg=await eda.dmt_Schematic.getCurrentSchematicPageInfo();if(pg?.uuid!==id)throw Error('Wrong capture page');
 const cs=await eda.sch_PrimitiveComponent.getAll(),parts=[];
 for(const c of cs)parts.push({id:c.getState_PrimitiveId(),ref:c.getState_Designator(),type:c.getState_ComponentType(),name:c.getState_Name(),sub:c.getState_SubPartName(),association:c.getState_Component(),footprint:c.getState_Footprint(),props:c.getState_OtherProperty(),pins:(await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId())).map(v=>({number:String(v.getState_PinNumber()),name:v.getState_PinName(),x:v.getState_X(),y:v.getState_Y(),nc:v.getState_NoConnected()}))});
 pages.push({page:pg,parts,nets:await eda.sch_Net.getAllNets(),source:await eda.sys_FileManager.getDocumentSource()});
}
const file=await eda.sch_ManufactureData.getNetlistFile('FIRST_BUILD_ACTUAL','Protel2');
let actualFile=null;
if(file){const bytes=new Uint8Array(await file.arrayBuffer());actualFile={name:file.name,size:file.size,type:file.type,constructor:file.constructor.name,tag:Object.prototype.toString.call(file),text:await file.text(),bytes:Array.from(bytes)};}
return {project:p,pages,actualFile,netlistDefined:file!==undefined&&file!==null};
