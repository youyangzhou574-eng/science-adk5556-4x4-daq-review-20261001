const pr=await eda.dmt_Project.getCurrentProjectInfo();if(pr.uuid!=='b771f646994e1e87ccac719bcaeddd7f79898452652eb8c78e76c7463539d085')throw Error('Wrong09');
return {project:pr.uuid,warnings:await eda.sch_Drc.check(true,false,true)};
