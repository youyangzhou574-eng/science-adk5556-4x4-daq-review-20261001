const pr=await eda.dmt_Project.getCurrentProjectInfo();if(pr.uuid!=='e58f223d256cd14d13a6fb04a0e150585301864f01c50827f9241f5945cf2801')throw Error('Wrong PCB copy');
await eda.dmt_EditorControl.openDocument('268e6597399ebcce');if((await eda.pcb_PrimitiveComponent.getAll()).length!==0)throw Error('Expected empty');
const c=await eda.pcb_PrimitiveComponent.create({libraryUuid:'0819f05c4eef4c71ace90d822a990e87',uuid:'eab4a8150b6d4918927e38d645cd50f2'},1,200,200,0,false);if(!c)throw Error('Create failed');
await eda.pcb_PrimitiveComponent.modify(c,{designator:'J1'});
const pads=await eda.pcb_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId());
for(const p of pads){const number=String(p.getState_PadNumber());if(!['1','2'].includes(number))throw Error('Unknown J1 pad');await p.setState_Net(number==='1'?'V5_IN':'GND').done();}
return {id:c.getState_PrimitiveId(),ref:c.getState_Designator(),pads:(await eda.pcb_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId())).map(p=>({number:p.getState_PadNumber(),net:p.getState_Net(),x:p.getState_X(),y:p.getState_Y()})),saved:await eda.pcb_Document.save(),source:await eda.sys_FileManager.getDocumentSource()};
