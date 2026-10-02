const lib=await eda.lib_LibrariesList.getSystemLibraryUuid();const result={};
for(const name of ['RT0603BRD0718KL','RT0603BRD07162KL','RT0603BRD0738K7L','RT0603BRD0712K1L','RT0603BRD0734K8L','RT0603BRD072KL']) result[name]=await eda.lib_Device.search(name,lib,undefined,undefined,3,1);
return result;
