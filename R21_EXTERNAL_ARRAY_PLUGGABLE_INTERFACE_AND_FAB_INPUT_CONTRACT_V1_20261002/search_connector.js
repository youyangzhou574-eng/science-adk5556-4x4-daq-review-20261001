const libraryUuid=await eda.lib_LibrariesList.getSystemLibraryUuid(); return {libraryUuid,items:await eda.lib_Device.search('1718560008',libraryUuid,undefined,undefined,12,1)};
