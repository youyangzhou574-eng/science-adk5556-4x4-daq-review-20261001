const project=await eda.dmt_Project.getCurrentProjectInfo();if(project.uuid!=='e58f223d256cd14d13a6fb04a0e150585301864f01c50827f9241f5945cf2801')throw Error('Wrong dedicated PCB copy');
await eda.dmt_EditorControl.openDocument('268e6597399ebcce');
const before=await eda.pcb_PrimitiveComponent.getAll();if(before.length)throw Error('Expected empty inherited PCB');
const imported=await eda.pcb_Document.importChanges('32047f874e6d71ce');
if(!imported)throw Error('PCB import failed');
const layers=await eda.pcb_Layer.setTheNumberOfCopperLayers(4);if(!layers)throw Error('4 layers not set');
const saved=await eda.pcb_Document.save();
const parts=[];for(const c of await eda.pcb_PrimitiveComponent.getAll()){parts.push({id:c.getState_PrimitiveId(),ref:c.getState_Designator(),name:c.getState_Name(),footprint:c.getState_Footprint(),component:c.getState_Component(),x:c.getState_X(),y:c.getState_Y(),rot:c.getState_Rotation(),props:c.getState_OtherProperty(),pads:(await eda.pcb_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId())).map(p=>({number:p.getState_PadNumber(),net:p.getState_Net(),x:p.getState_X(),y:p.getState_Y(),layer:p.getState_Layer()}))});}
return {project:project.uuid,pcb:'268e6597399ebcce',imported,layers,saved,parts,source:await eda.sys_FileManager.getDocumentSource(),layerInfo:await eda.pcb_Layer.getAllLayers(),rules:await eda.pcb_Drc.getCurrentRuleConfiguration()};
