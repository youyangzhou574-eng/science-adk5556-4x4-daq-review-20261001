const libraryUuid=await eda.lib_LibrariesList.getSystemLibraryUuid();
const searches={};
for(const mpn of ['OPA388IDBVR','TMUX1109PWR','LP5912-3.3DRVR','BAT54XY','TPD4E05U06DQAR']) searches[mpn]=await eda.lib_Device.search(mpn,libraryUuid,undefined,undefined,5,1);
return {project:await eda.dmt_Project.getCurrentProjectInfo(),schematics:await eda.dmt_Schematic.getAllSchematicsInfo(),libraryUuid,searches};
