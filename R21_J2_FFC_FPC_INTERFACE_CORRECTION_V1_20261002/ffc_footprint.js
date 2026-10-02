const pr=await eda.dmt_Project.getCurrentProjectInfo();if(pr.uuid!=='33bea4d378d43e15e958ffe0eb3058ea5cedff592b3de7cb3eb882844cd142d6')throw Error('Wrong FFC copy');
const source=await eda.sys_FileManager.getDocumentSource();const head=JSON.parse(source.split('||')[1].split('|')[0]);if(head.uuid!=='87b2e6ab0bf2243f')throw Error('Only isolated J2 footprint editor allowed');
const pads=await eda.pcb_PrimitivePad.getAll();if(pads.length!==8)throw Error('Expected old J2 eightpad template');
if(!await eda.pcb_PrimitivePad.delete(pads))throw Error('Delete old J2 pad template');
const polys=await eda.pcb_PrimitivePolyline.getAll();if(polys.length)await eda.pcb_PrimitivePolyline.delete(polys);
const mm=v=>v/.0254;const createdPads=[];
for(let i=0;i<8;i++){const p=await eda.pcb_PrimitivePad.create(1,String(i+1),mm(-3.5+i),0,0,['RECT',mm(.4),mm(1),0],'',null,0,0,0,false);if(!p)throw Error('FFC signalpad');createdPads.push(p.getState_PrimitiveId());}
for(const [n,x]of[['MP1',-6.3],['MP2',6.3]]){const p=await eda.pcb_PrimitivePad.create(1,n,mm(x),mm(2.7),0,['RECT',mm(2),mm(1.3),0],'',null,0,0,0,false);if(!p)throw Error('FFC fitting nail');createdPads.push(p.getState_PrimitiveId());}
async function poly(layer,xy,w=.15){const p=await eda.pcb_PrimitivePolyline.create('',layer,eda.pcb_MathPolygon.createPolygon(xy.map(v=>typeof v==='number'?mm(v):v)),mm(w),false);if(!p)throw Error('FFC outline');return p.getState_PrimitiveId();}
const createdPolys=[];
// Source front/bottom-view mirrored vertically into native positive-y insertion direction; no signal-row mirror.
createdPolys.push(await poly(9,[-6.6,-.5,'L',6.6,-.5,6.6,4.8,-6.6,4.8,-6.6,-.5],.1));
createdPolys.push(await poly(48,[-7.8,-1,'L',7.8,-1,7.8,5.3,-7.8,5.3,-7.8,-1],.05));
createdPolys.push(await poly(3,[-6.7,-.65,'L',-6.7,1.7],.12));createdPolys.push(await poly(3,[6.7,-.65,'L',6.7,1.7],.12));
createdPolys.push(await poly(3,[-5.9,4.95,'L',5.9,4.95],.12));
createdPolys.push(await poly(3,[-4.25,-.75,'L',-3.75,-1.3,-3.25,-.75,-4.25,-.75],.12));
// Insertion arrow, conductor faces board; rear signal1 end labelled ROW side.
createdPolys.push(await poly(3,[0,6.5,'L',0,5.55,-.3,5.9,0,5.55,.3,5.9],.12));
const texts=[];for(const [txt,x,y]of[['J2',0,1.6],['1',-4.45,-1.4],['ROW',-3.5,-2.2],['COL',.5,-2.2],['FFC INSERT',-3.3,7.2],['CONTACT PCB',-3.5,8.2]]){const t=await eda.pcb_PrimitiveString.create(3,mm(x),mm(y),txt,'default',mm(.65),mm(.12),3,0,false,0,false,false);if(!t)throw Error('FFC native silktext');texts.push(t.getState_PrimitiveId());}
const attrs=await eda.pcb_PrimitiveAttribute.getAll();for(const a of attrs){if(a.getState_Key()==='Footprint')await a.setState_Value('MOLEX_2005290081_MFR_2005291002B_R20').done();}
return {createdPads,createdPolys,texts,source:await eda.sys_FileManager.getDocumentSource(),explicitSaveCalled:false};
