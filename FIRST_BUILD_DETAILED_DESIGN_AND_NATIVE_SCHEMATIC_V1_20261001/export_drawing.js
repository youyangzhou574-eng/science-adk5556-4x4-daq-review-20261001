const p=await eda.dmt_Project.getCurrentProjectInfo();if(!['74e664f7c1193aad2a35d2db078a1f226377acc149fbbc11d8b1a9f9638bea07','07975f0da1517bcd267595cda8361726b99324274473489c5a2f7c0530f33402'].includes(p?.uuid))throw Error('Wrong independent project');
const f=await eda.sch_ManufactureData.getExportDocumentFile('FIRST_BUILD_REVIEW_ONLY','PDF',{theme:'Black on White',lineWidth:'Default',size:'Original Size'},'Current Schematic',{range:'All',outputMethod:'Merged sheet'});
if(!f)return {status:'DRAWING_FILE_UNAVAILABLE'};
const b=new Uint8Array(await f.arrayBuffer());let s='';for(let i=0;i<b.length;i+=16384)s+=String.fromCharCode(...b.subarray(i,i+16384));
return {status:'ACTUAL_PDF_FILE',name:f.name,size:f.size,constructor:f.constructor.name,base64:btoa(s)};
