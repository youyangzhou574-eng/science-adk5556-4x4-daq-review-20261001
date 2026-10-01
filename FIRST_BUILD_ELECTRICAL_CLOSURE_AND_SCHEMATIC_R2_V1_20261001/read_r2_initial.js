const p=await eda.dmt_Project.getCurrentProjectInfo();
if(p?.uuid!=='f584056ea8f7cc74a210f932891fde19f1d1518be7e7f4466d0c7acd11c29efe')throw Error('Wrong R2');
return {project:p,schematics:await eda.dmt_Schematic.getAllSchematicsInfo(),current:await eda.dmt_Schematic.getCurrentSchematicPageInfo()};
