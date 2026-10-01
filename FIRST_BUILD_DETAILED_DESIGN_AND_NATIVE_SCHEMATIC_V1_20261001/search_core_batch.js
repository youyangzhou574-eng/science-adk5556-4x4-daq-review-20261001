const libraryUuid=await eda.lib_LibrariesList.getSystemLibraryUuid();
const results=[];
for(const key of __CLI__.args.keys){const items=await eda.lib_Device.search(key,libraryUuid,undefined,undefined,12,1);results.push({key,items});}
return {time:new Date().toISOString(),libraryUuid,results};
