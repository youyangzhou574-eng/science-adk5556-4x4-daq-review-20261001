const p=await eda.dmt_Project.getCurrentProjectInfo();
if(p?.uuid!=='74e664f7c1193aad2a35d2db078a1f226377acc149fbbc11d8b1a9f9638bea07')throw Error('Wrong independent project');
const names=['Power_Reference','Row_Drive_Interface','Column_TIA','ADC_MCU_Interfaces'];
const ids=['9965fd7b16015eaf'];
for(let i=1;i<4;i++){const id=await eda.dmt_Schematic.createSchematicPage('0ccfdd809e468881');if(!id)throw Error('Create page '+i);ids.push(id);}
for(let i=0;i<4;i++)if(!(await eda.dmt_Schematic.modifySchematicPageName(ids[i],names[i])))throw Error('Page rename '+i);
return {project:p,pages:ids.map((uuid,i)=>({uuid,name:names[i],index:i})),schematics:await eda.dmt_Schematic.getAllSchematicsInfo()};
