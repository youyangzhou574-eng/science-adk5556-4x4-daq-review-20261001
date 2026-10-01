import json,pathlib
p=pathlib.Path(__file__).resolve().parent;plan=json.loads((p/'PLANNED_NATIVE_DESIGN.json').read_text(encoding='utf-8'));pages=json.loads((p/'NATIVE_PAGE_IDS.json').read_text())
template='''
const plan=PLAN;
const result={page:plan.page,repair:'ACTUAL_PIN_ROTATION_OUTWARD_AND_QUANTIZED_STUBS',parts:[],wires:[],ports:[]};
const project=await eda.dmt_Project.getCurrentProjectInfo();if(project?.uuid!==plan.project)throw Error('Wrong project');
await eda.dmt_EditorControl.openDocument(plan.page.uuid);if((await eda.dmt_Schematic.getCurrentSchematicPageInfo())?.uuid!==plan.page.uuid)throw Error('Wrong page');
let cs=await eda.sch_PrimitiveComponent.getAll();
const actualParts=cs.filter(c=>c.getState_ComponentType()==='part');
if(actualParts.length!==plan.parts.length)throw Error('Unexpected part count');
const ws=await eda.sch_PrimitiveWire.getAll();result.removedWires=ws.map(w=>w.getState_PrimitiveId());
if(ws.length&&!(await eda.sch_PrimitiveWire.delete(result.removedWires)))throw Error('Delete generated wires');
const ports=cs.filter(c=>c.getState_ComponentType()==='netport');result.removedPorts=ports.map(c=>c.getState_PrimitiveId());
if(ports.length&&!(await eda.sch_PrimitiveComponent.delete(result.removedPorts)))throw Error('Delete generated ports');
for(const q of plan.parts){
 const c=actualParts.find(v=>v.getState_Designator()===q.ref);if(!c)throw Error('Missing '+q.ref);
 let ps=await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId());
 if(q.ref.startsWith('C')&&ps.some(v=>[90,270].includes(v.getState_Rotation()))){
  const rotated=await eda.sch_PrimitiveComponent.modify(c,{rotation:90});if(!rotated)throw Error('Passive orientation');
  ps=await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId());
  (result.rotatedPassives??=[]).push(q.ref);
 }
 if(ps.length!==Object.keys(q.nets).length)throw Error('Pin count');
 for(const pin of ps){const n=String(pin.getState_PinNumber()),net=q.nets[n];if(net===null){if(!pin.getState_NoConnected())throw Error('NC drift');continue;}
 const x=pin.getState_X(),y=pin.getState_Y(),rot=pin.getState_Rotation();
 if(![0,90,180,270].includes(rot))throw Error('Unreviewed actual pin angle '+rot);
 const ox=rot===0?40:rot===180?-40:0,oy=ox===0?Math.sign(y-q.y)*40:0;
 if(ox===0&&oy===0)throw Error('Undefined vertical outward coordinate');
 const ex=x+ox,ey=y+oy;
 const port=await eda.sch_PrimitiveComponent.createNetPort('BI',net,ex,ey,ox<0?180:ox>0?0:oy>0?90:270,false);if(!port)throw Error('Port');
 const pp=await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(port.getState_PrimitiveId());if(pp.length!==1)throw Error('Port pin');
 const ax=Math.round(pp[0].getState_X()*1e6)/1e6,ay=Math.round(pp[0].getState_Y()*1e6)/1e6;
 if(Math.abs(ax-ex)>1e-5||Math.abs(ay-ey)>1e-5)throw Error('Actual port anchor mismatch');
 const line=[x,y,ax,ay];const w=await eda.sch_PrimitiveWire.create([line],net);if(!w)throw Error('Wire');
 for(const a of await eda.sch_PrimitiveAttribute.getAll(port.getState_PrimitiveId()))if(a.getState_ValueVisible())await eda.sch_PrimitiveAttribute.modify(a,{fontSize:6,rotation:0,x:ex+(ox>=0?18:-18),y:ey,alignMode:ox>=0?2:8});
 result.wires.push({ref:q.ref,pin:n,id:w.getState_PrimitiveId(),net,line});result.ports.push({ref:q.ref,pin:n,id:port.getState_PrimitiveId(),net,x:ax,y:ay});
 }
 result.parts.push({ref:q.ref,id:c.getState_PrimitiveId()});
}
result.status='REPAIR_COMPLETED_UNSAVED';return result;
'''
for i,page in enumerate(pages):
 d={'project':plan['project_uuid'],'page':page,'parts':[{'ref':q['ref'],'x':q['x'],'y':q['y'],'nets':q['nets']}for q in plan['parts']if q['page']==i]}
 (p/('repair_page_'+str(i)+'.js')).write_text(template.replace('PLAN',json.dumps(d)),encoding='utf-8')
(p/'NATIVE_GENERATION_CORRECTION.md').write_text('''# 生成纠正记录
首轮使用库导出角度推断放置后的引脚方向错误。实际放置R_ISO0 pin2=(700,145),rotation0，pin1=(660,145),rotation180；首轮向内延伸导致两端导线自动归并，真实Protel2显示多个原本不同网络合并。首轮网表/PDF/API证据保留，不作为交付。
按实际运行态角度0向右、180向左重建自有4页所有短导线/端口，并把原生端口浮点舍入到1e-6避免伪短分段；未知角度拒绝而非猜测。器件、physicalpin/net计划、NC不变。调整端口文本在图元外侧、字体6，提高图纸可读性。只删本包刚生成的导线/端口，不动旧工程/厂家库。
另：第一版新图页空检查把官方默认sheet当电路器件拒绝，保留BUILD_PAGE_0错误并据实际sheet-only检查修正；没有重复创建电路器件。DC首次KCL测试的期望符号错误，纠正为sink=(vrow−source)/lead，模型不变，8类复核通过。这些是执行端生成/断言错误，不裁定嘉立创不兼容。
''',encoding='utf-8')
print('four repair scripts prepared')
