const id='f584056ea8f7cc74a210f932891fde19f1d1518be7e7f4466d0c7acd11c29efe';
const opened=await eda.dmt_Project.openProject(id);if(!opened)throw Error('R2 open failed');
return {opened,project:await eda.dmt_Project.getCurrentProjectInfo(),schematics:await eda.dmt_Schematic.getAllSchematicsInfo()};
