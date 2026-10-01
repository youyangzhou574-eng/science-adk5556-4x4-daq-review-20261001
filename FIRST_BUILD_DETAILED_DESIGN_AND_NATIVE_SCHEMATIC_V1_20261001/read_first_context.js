const project=await eda.dmt_Project.getCurrentProjectInfo();
return {project,schematics:await eda.dmt_Schematic.getAllSchematicsInfo(),time:new Date().toISOString()};
