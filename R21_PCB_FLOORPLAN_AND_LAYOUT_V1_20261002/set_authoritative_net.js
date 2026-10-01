const pr=await eda.dmt_Project.getCurrentProjectInfo();if(pr.uuid!=='e58f223d256cd14d13a6fb04a0e150585301864f01c50827f9241f5945cf2801')throw Error('Wrong copy');await eda.dmt_EditorControl.openDocument('595d5f2f11dee03d');
const file=await eda.sch_ManufactureData.getNetlistFile('ACCEPTED_SCHEMATIC_JLC_NETLIST','JLCEDA');if(!file)throw Error('No actual File');const text=await file.text();await eda.dmt_EditorControl.openDocument('268e6597399ebcce');
const updated=await eda.pcb_Net.setNetlist('JLCEDA',text);if(!updated)throw Error('Native netlist not updated');
return {updated,saved:await eda.pcb_Document.save(),parts:(await eda.pcb_PrimitiveComponent.getAll()).length,comparison:await eda.sys_Tool.netlistComparison('32047f874e6d71ce','268e6597399ebcce')};
