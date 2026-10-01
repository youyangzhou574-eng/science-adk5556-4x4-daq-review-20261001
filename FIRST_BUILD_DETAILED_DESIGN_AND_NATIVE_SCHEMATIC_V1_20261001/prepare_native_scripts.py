import json,pathlib
p=pathlib.Path(__file__).resolve().parent
plan=json.loads((p/'PLANNED_NATIVE_DESIGN.json').read_text(encoding='utf-8'))
pages=json.loads((p/'CREATE_FOUR_PAGES.json').read_text(encoding='utf-8'))['parsed']['value']['pages']
(p/'NATIVE_PAGE_IDS.json').write_text(json.dumps(pages,indent=2)+'\n',encoding='utf-8')
template='''
const plan=PLAN;
const result={page:plan.page,parts:[],markers:[],wires:[],nc:[],status:'STARTED'};
try{
const project=await eda.dmt_Project.getCurrentProjectInfo();
if(project?.uuid!==plan.project)throw Error('Wrong independent project context');
await eda.dmt_EditorControl.openDocument(plan.page.uuid);
const pg=await eda.dmt_Schematic.getCurrentSchematicPageInfo();
if(pg?.uuid!==plan.page.uuid)throw Error('Wrong page');
await eda.dmt_Schematic.modifySchematicPageTitleBlock(false);
const initial=await eda.sch_PrimitiveComponent.getAll();if(initial.some(c=>c.getState_ComponentType()!=='sheet'))throw Error('Expected empty new page apart from official default sheet');
for(const q of plan.parts){
const c=await eda.sch_PrimitiveComponent.create({libraryUuid:q.library_uuid,uuid:q.device_uuid},q.x,q.y,q.subpart,0,false,true,true);
if(!c)throw Error('Create '+q.ref);
const m=await eda.sch_PrimitiveComponent.modify(c.getState_PrimitiveId(),{designator:q.ref,name:q.value||q.device,otherProperty:{...c.getState_OtherProperty(),'Review Status':'DYNAMIC_VALIDATION_HOLD / FAULT_PROTECTION_HOLD',...(q.value?{Value:q.value}:{}),'Circuit Role':q.role}});
if(!m)throw Error('Modify '+q.ref);
const ps=await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(m.getState_PrimitiveId());
const actual=ps.map(v=>({number:String(v.getState_PinNumber()),name:v.getState_PinName(),x:v.getState_X(),y:v.getState_Y(),rotation:v.getState_Rotation()}));
if(new Set(actual.map(v=>v.number)).size!==actual.length||actual.length!==Object.keys(q.nets).length||actual.some(v=>!(v.number in q.nets)))throw Error('Actual pin identity '+q.ref);
result.parts.push({ref:q.ref,id:m.getState_PrimitiveId(),association:m.getState_Component(),footprint:m.getState_Footprint(),pins:actual});
for(let i=0;i<ps.length;i++){
const pin=ps[i],a=actual[i],net=q.nets[a.number];
if(net===null){const n=await pin.setState_NoConnected(true).done();result.nc.push({ref:q.ref,pin:a.number,actual_noConnected:n?.getState_NoConnected?.()??pin.getState_NoConnected()});continue;}
const dx=a.x-q.x,dy=a.y-q.y;
let ox=0,oy=0;
// Horizontal pins in the actual symbol use inward angles0/180; vertical90/270.
if(a.rotation===0)ox=-30;else if(a.rotation===180)ox=30;else if(a.rotation===90)oy=-30;else if(a.rotation===270)oy=30;else if(Math.abs(dx)>Math.abs(dy))ox=dx<0?-30:30;else oy=dy<0?-30:30;
const ex=a.x+ox,ey=a.y+oy;
const mark=await eda.sch_PrimitiveComponent.createNetPort('BI',net,ex,ey,ox<0?180:oy<0?90:oy>0?270:0,false);
if(!mark)throw Error('Port '+q.ref+'.'+a.number);
const mp=await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(mark.getState_PrimitiveId());if(mp.length!==1)throw Error('Port anchor');
const mx=mp[0].getState_X(),my=mp[0].getState_Y();
const line=[a.x,a.y,mx,a.y];if(my!==a.y)line.push(mx,my);
const w=await eda.sch_PrimitiveWire.create([line],net);if(!w)throw Error('Wire '+q.ref+'.'+a.number);
result.markers.push({ref:q.ref,pin:a.number,net,id:mark.getState_PrimitiveId(),x:mx,y:my});result.wires.push({ref:q.ref,pin:a.number,net,id:w.getState_PrimitiveId(),line});
}
}
for(let i=0;i<plan.notes.length;i++)await eda.sch_PrimitiveText.create(55,30+i*18,plan.notes[i],0,null,null,10,i===0);
if(plan.page.index>0){result.saved=await eda.sch_Document.save();if(result.saved!==true)throw Error('Save did not return true');result.status='PAGE_CREATED_AND_SAVE_TRUE';}else result.status='PAGE_CREATED_NO_SAVE';return result;
}catch(e){result.status='STOP_NATIVE_BUILD_ERROR';result.error={name:e?.name,message:e?.message,stack:e?.stack};return result;}
'''
for i,page in enumerate(pages):
 data={'project':plan['project_uuid'],'page':page,'parts':[q for q in plan['parts']if q['page']==i],'notes':plan['notes'][i]}
 (p/('build_page_'+str(i)+'.js')).write_text(template.replace('PLAN',json.dumps(data,ensure_ascii=False)),encoding='utf-8')
print(json.dumps({'pages':pages,'scripts':4}))
