const lib=await eda.lib_LibrariesList.getSystemLibraryUuid(),results=[];
for(const key of ['TPS389001DSET','BAT54S,215'])results.push({key,items:await eda.lib_Device.search(key,lib,undefined,undefined,8,1)});
return {libraryUuid:lib,results,time:new Date().toISOString()};
