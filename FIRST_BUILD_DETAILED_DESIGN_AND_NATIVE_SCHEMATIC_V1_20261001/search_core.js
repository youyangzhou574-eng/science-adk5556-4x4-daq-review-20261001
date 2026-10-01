const key=__CLI__.args.key;
const libraryUuid=await eda.lib_LibrariesList.getSystemLibraryUuid();
const items=await eda.lib_Device.search(key,libraryUuid,undefined,undefined,20,1);
return {time:new Date().toISOString(),key,libraryUuid,items};
