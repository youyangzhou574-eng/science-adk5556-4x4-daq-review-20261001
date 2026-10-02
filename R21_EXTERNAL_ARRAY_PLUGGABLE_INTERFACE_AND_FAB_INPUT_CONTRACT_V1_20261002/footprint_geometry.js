const pr=await eda.dmt_Project.getCurrentProjectInfo();if(pr.uuid!=='ee4f96f0b67e0b9c85e719fedce50790f5a49c47e4db3392e90aea8fef4c93c9')throw Error('Wrong J2 copy');
const before=await eda.sys_FileManager.getDocumentSource();if(!before.includes('268e6597399ebcce_1cca92df09a37573'))throw Error('Only the isolated J2 footprint editor is allowed');
const old=await eda.pcb_PrimitivePolyline.getAll();
const removed=[];for(const p of old){const id=p.getState_PrimitiveId();if(!['e10','e11','e12','e13','e14','e15'].includes(id))throw Error('Unexpected footprint outline');if(!await eda.pcb_PrimitivePolyline.delete(p))throw Error('Delete old generic outline');removed.push(id);}
const mm=v=>v/.0254;
async function poly(layer,pts,width){const polygon=eda.pcb_MathPolygon.createPolygon(pts.map(v=>typeof v==='number'?mm(v):v));const p=await eda.pcb_PrimitivePolyline.create('',layer,polygon,mm(width),false);if(!p)throw Error('J2 outline creation');return p.getState_PrimitiveId();}
const created=[];
// Manufacturer body envelope 20.17 x 6.35; pin row is 3.10 from lock wall.
created.push(await poly(9,[-10.085,-3.25,'L',10.085,-3.25,10.085,3.10,-10.085,3.10,-10.085,-3.25],.10));
// Board-design courtyard includes mated housing 20.88 length plus .50 each end.
created.push(await poly(48,[-10.94,-3.77,'L',10.94,-3.77,10.94,3.60,-10.94,3.60,-10.94,-3.77],.05));
created.push(await poly(3,[-10.20,-3.37,'L',10.20,-3.37,10.20,3.22,-10.20,3.22,-10.20,-3.37],.15));
// Lock-side stroke, plus explicit triangular pin1 mark outside pad copper.
created.push(await poly(3,[-9.80,2.70,'L',9.80,2.70],.15));
created.push(await poly(3,[-9.55,-1.65,'L',-8.23,-1.65,-8.89,-.95,-9.55,-1.65],.15));
return {removed,created,manufacturerDimensions:{bodyLength:20.17,bodyWidth:6.35,lockSideFromPin:3.10},boardChoices:{copper:1.70,courtyardMargin:0.50},source:await eda.sys_FileManager.getDocumentSource(),explicitSaveCalled:false};
