const libraryUuid=await eda.lib_LibrariesList.getSystemLibraryUuid(); return {libraryUuid,items:await eda.lib_Device.search('171856-0008',libraryUuid,undefined,undefined,12,1)};
