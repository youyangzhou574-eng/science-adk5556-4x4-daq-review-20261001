const pr=await eda.dmt_Project.getCurrentProjectInfo();if(pr.uuid!=='e58f223d256cd14d13a6fb04a0e150585301864f01c50827f9241f5945cf2801')throw Error('Wrong copy');await eda.dmt_EditorControl.openDocument('268e6597399ebcce');
const all=await eda.pcb_PrimitiveComponent.getAll();const w=100/.0254,h=90/.0254;
const p=eda.pcb_MathPolygon.createPolygon([0,0,'L',w,0,w,h,0,h,0,0]);if(!p)throw Error('Outline polygon');
const outline=await eda.pcb_PrimitivePolyline.create('',11,p,4,false);if(!outline)throw Error('Outline');
return {outline:outline.getState_PrimitiveId(),saved:await eda.pcb_Document.save(),positions:all.map(c=>({ref:c.getState_Designator(),x:c.getState_X(),y:c.getState_Y(),rotation:c.getState_Rotation()})),source:await eda.sys_FileManager.getDocumentSource()};
