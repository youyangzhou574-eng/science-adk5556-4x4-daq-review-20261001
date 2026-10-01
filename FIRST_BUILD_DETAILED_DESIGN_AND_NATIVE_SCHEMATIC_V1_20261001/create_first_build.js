const uuid=await eda.dmt_Project.createProject('SCIENCE_ADK5556_4X4_FIRST_BUILD_V1','science-adk5556-4x4-first-build-v1',undefined,undefined,'Independent 0.8-8kohm array first-build review schematic; bench/dynamic/fault validation pending');
if(!uuid)throw Error('Official createProject returned no uuid');
return {uuid,info:await eda.dmt_Project.getProjectInfo(uuid),time:new Date().toISOString()};
