const lib=await eda.lib_LibrariesList.getSystemLibraryUuid();
const f=await eda.sys_FileManager.getDeviceFileByDeviceUuid(__CLI__.args.uuids,lib,'elibz2');
if(!f)return {defined:false,time:new Date().toISOString()};
const bytes=new Uint8Array(await f.arrayBuffer());let binary='';for(let i=0;i<bytes.length;i+=8192)binary+=String.fromCharCode(...bytes.slice(i,i+8192));
return {defined:true,name:f.name,size:f.size,type:f.type,tag:Object.prototype.toString.call(f),base64:btoa(binary)};
