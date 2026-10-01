const pr=await eda.dmt_Project.getCurrentProjectInfo();if(pr.uuid!=='b771f646994e1e87ccac719bcaeddd7f79898452652eb8c78e76c7463539d085')throw Error('Wrong new09');
const pages=[];
for(const uuid of ['595d5f2f11dee03d','49bb518d907ff185']){
 await eda.dmt_EditorControl.openDocument(uuid);
 const parts=[];
 for(const c of await eda.sch_PrimitiveComponent.getAll()){
 const pins=await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId());
 parts.push({id:c.getState_PrimitiveId(),type:c.getState_ComponentType(),ref:c.getState_Designator(),x:c.getState_X(),y:c.getState_Y(),pins:pins.map(v=>({x:v.getState_X(),y:v.getState_Y()}))});
 }
 pages.push({uuid,parts,wires:(await eda.sch_PrimitiveWire.getAll()).map(w=>({id:w.getState_PrimitiveId(),line:w.getState_Line()})),source:await eda.sys_FileManager.getDocumentSource()});
}
return {project:pr.uuid,pages};
