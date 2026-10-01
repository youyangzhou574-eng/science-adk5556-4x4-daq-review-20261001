const uuid=await eda.dmt_Project.createProject('SCIENCE_ADK5556_4X4_FIRST_BUILD_ELECTRICAL_CLOSURE_AND_SCHEMATIC_R2_V1','science-adk5556-4x4-electrical-closure-r2-v1',undefined,undefined,'Independent R2 review; dynamic/fault/effective-capacity/bench holds retained');
if(!uuid)throw Error('Official createProject returned no UUID');
return {uuid,info:await eda.dmt_Project.getProjectInfo(uuid),time:new Date().toISOString()};
