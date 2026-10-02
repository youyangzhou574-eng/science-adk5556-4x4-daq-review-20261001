const libraryUuid=await eda.lib_LibrariesList.getSystemLibraryUuid();const searches={};
for(const s of ['TPS7A3701DRVT','RT0603BRD0752K3L','RT0603BRD0730K1L','RT0603BRD0717KL','RT0603BRD0790KL','RT0603BRD07100KL'])searches[s]=await eda.lib_Device.search(s,libraryUuid,undefined,undefined,3,1);
return {project:await eda.dmt_Project.getCurrentProjectInfo(),schematics:await eda.dmt_Schematic.getAllSchematicsInfo(),libraryUuid,searches};
