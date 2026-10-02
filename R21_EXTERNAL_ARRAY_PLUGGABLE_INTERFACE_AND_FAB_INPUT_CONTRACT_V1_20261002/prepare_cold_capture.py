from pathlib import Path
P=Path(__file__).parent
s=(P/'capture_baseline.js').read_text('utf-8-sig').replace('return {schematic,pcb};','const capture={schematic,pcb};')
s+='''\nconst f=await eda.sys_FileManager.getProjectFile("SCIENCE_ADK5556_4X4_R21_J2_PLUGGABLE_REVIEW","","epro2");if(!f)throw Error("No actual native File");const bytes=new Uint8Array(await f.arrayBuffer());let s="";for(let i=0;i<bytes.length;i+=16384)s+=String.fromCharCode(...bytes.subarray(i,i+16384));return {capture,nativeFile:{name:f.name,bytes:f.size,base64:btoa(s),constructor:f.constructor.name,tag:Object.prototype.toString.call(f),explicitSaveCalled:false},scope:"Final independent cold full schematic+PCB/source/rules audit and actual native File, no edits"};\n'''
(P/'capture_cold_and_native.js').write_text(s,'utf8')
