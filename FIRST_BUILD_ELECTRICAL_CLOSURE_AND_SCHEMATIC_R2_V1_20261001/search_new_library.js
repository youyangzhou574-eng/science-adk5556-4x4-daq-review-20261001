const lib=await eda.lib_LibrariesList.getSystemLibraryUuid();
const results=[];
for(const key of ['LM73100RPWR','TPS3808G01DBVR','SN74LVC08APWR','BAT54S','GRM1885C1H101JA01D','GRM31CR71H225KA88L']){
 const items=await eda.lib_Device.search(key,lib,undefined,undefined,12,1);
 results.push({key,items});
}
return {libraryUuid:lib,results,time:new Date().toISOString()};
