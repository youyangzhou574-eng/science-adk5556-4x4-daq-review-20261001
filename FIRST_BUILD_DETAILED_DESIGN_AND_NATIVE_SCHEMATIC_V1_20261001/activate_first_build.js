const uuid=__CLI__.args.uuid;
if(uuid!=='74e664f7c1193aad2a35d2db078a1f226377acc149fbbc11d8b1a9f9638bea07')throw Error('Unexpected target uuid');
return {uuid,opened:await eda.dmt_Project.openProject(uuid),time:new Date().toISOString()};
