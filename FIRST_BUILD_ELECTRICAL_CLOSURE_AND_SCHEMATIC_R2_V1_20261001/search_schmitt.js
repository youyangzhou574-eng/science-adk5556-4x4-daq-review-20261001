const lib=await eda.lib_LibrariesList.getSystemLibraryUuid();
return {libraryUuid:lib,items:await eda.lib_Device.search('SN74LVC1G17DBVR',lib,undefined,undefined,6,1)};
