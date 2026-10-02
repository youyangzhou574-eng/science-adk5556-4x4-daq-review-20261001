const pr=await eda.dmt_Project.getCurrentProjectInfo();if(pr.uuid!=='33bea4d378d43e15e958ffe0eb3058ea5cedff592b3de7cb3eb882844cd142d6')throw Error('Wrong FFC project');
let src=await eda.sys_FileManager.getDocumentSource();const head=JSON.parse(src.split('||')[1].split('|')[0]);if(head.uuid!=='87b2e6ab0bf2243f')throw Error('J2-only editor');
const fills=await eda.pcb_PrimitiveFill.getAll();if(fills.length!==9)throw Error('Expected old mechanical drawing fills');await eda.pcb_PrimitiveFill.delete(fills);
src=await eda.sys_FileManager.getDocumentSource();const out=[];
for(const ln of src.split('\n')){if(!ln.includes('||')){if(ln.trim())out.push(ln);continue;}const [hs,bs]=ln.split('||'),h=JSON.parse(hs),b=JSON.parse(bs.replace(/\|$/,''));
 if(h.type==='D3_ATTRIBUTE')continue; // Wrong historical KK model removed, no invented3D.
 if(h.type==='ATTR'&&b.key==='Footprint')b.value='MOLEX_2005290081_MFR_2005291002B_R20';
 if(h.type==='STRING'&&b.text==='FFC INSERT')b.y=-3.2/.0254;
 if(h.type==='STRING'&&b.text==='CONTACT PCB')b.y=-4.2/.0254;
 // Native-only arrow kept inside board: origin6.5mm minus arrow6.5mm isedge0; bodycourtyard otherwise within.
 out.push(JSON.stringify(h)+'||'+JSON.stringify(b)+'|');}
const ok=await eda.sys_FileManager.setDocumentSource(out.join('\n'));if(!ok)throw Error('FFC exact local source apply failed');return{ok,removedLegacyFills:9,removedLegacy3D:true,source:await eda.sys_FileManager.getDocumentSource(),explicitSaveCalled:false};
