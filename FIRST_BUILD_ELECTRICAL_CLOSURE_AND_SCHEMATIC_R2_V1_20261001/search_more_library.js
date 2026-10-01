const lib=await eda.lib_LibrariesList.getSystemLibraryUuid(),results=[];
for(const key of ['BAT54S,215','BAT54S_C8598','RC2010FK-07100RL','RC1206FR-07100RL','TPS3890DSET'])results.push({key,items:await eda.lib_Device.search(key,lib,undefined,undefined,8,1)});
return {libraryUuid:lib,results,time:new Date().toISOString()};
