import pathlib
P=pathlib.Path(__file__).resolve().parent
s=(P/'capture.js').read_text('utf8')
prefix=s[:s.index('const file=')]
(P/'preclose_snapshot.js').write_text(prefix+'return {project,pages};','utf8')
tail=s[s.index('const file='):]
native="const nf=await eda.sys_FileManager.getProjectFile('SCIENCE_ADK5556_4X4_R21_REVIEW','', 'epro2');if(!nf)throw Error('No native File');const nb=new Uint8Array(await nf.arrayBuffer());let ns='';for(let i=0;i<nb.length;i+=16384)ns+=String.fromCharCode(...nb.subarray(i,i+16384));const native={name:nf.name,size:nf.size,constructor:nf.constructor.name,tag:Object.prototype.toString.call(nf),base64:btoa(ns)};"
(P/'capture_cold_final.js').write_text(prefix+native+tail.replace('return {project,pages,actualFile:', 'return {project,pages,native,actualFile:'),'utf8')
