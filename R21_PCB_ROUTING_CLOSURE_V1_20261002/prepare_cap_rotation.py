exec((__import__('pathlib').Path(__file__).parent/'prepare_p0.py').read_text('utf8').split("out={'scope'")[0])
selected=['C_TIA_HF1','C_TIA_HF2','C_ROW_HF1','C_ROW_HF2'];dropNets=['COL_SENSE1','COL_SENSE2','ROW_FB1','ROW_FB2']
dropped=[t['id']for t in traces if t.get('id')and t['net']in dropNets];traces[:]=[t for t in traces if t['net']not in dropNets]
for ref in selected:
 c=next(c for c in v['parts']if c['ref']==ref)
 for p in pads:
  if p['ref']!=ref:continue
  old=(p['x'],p['y']);p['x']=2*c['x']-old[0];p['y']=2*c['y']-old[1];p['geometry']=translate(p['geometry'],p['x']-old[0],p['y']-old[1]);p['rotation']=180
created=[];failure=[]
for net in dropNets+['TIA_DRV1','TIA_DRV2','ROW_DRV1','ROW_DRV2']:
 while len(groups(net))>1:
  gs=groups(net);pairs=sorted((math.hypot(a['x']-b['x'],a['y']-b['y']),a['key'],b['key'],a,b)for i,g in enumerate(gs)for h in gs[:i]for a in g for b in h);made=False
  for dist,ak,bk,a,b in pairs:
   for pts in candidates((a['x'],a['y']),(b['x'],b['y'])):
    pts=[q for k,q in enumerate(pts)if k==0 or q!=pts[k-1]]
    if not free(pts,net):continue
    t={'net':net,'layer':1,'width':6,'points':pts,'from':ak,'to':bk,'geometry':LineString(pts).buffer(3,cap_style=1)};traces.append(t);created.append(t);made=True;break
   if made:break
  if not made:failure.append({'net':net,'groups':[[p['key']for p in g]for g in groups(net)]});break
out={'rotations':[{'ref':ref,'id':next(c['id']for c in v['parts']if c['ref']==ref),'rotation':180}for ref in selected],'deleteLines':dropped,'segments':[{'net':t['net'],'layer':1,'width':6,'x1':a[0],'y1':a[1],'x2':b[0],'y2':b[1]}for t in created for a,b in zip(t['points'],t['points'][1:])],'failures':failure}
(P/'P0_CAP_ROTATION_PLAN.json').write_text(json.dumps(out,indent=2),'utf8')
assert not failure, 'Do not apply rotation without fully connected short feedback paths'
code="const pr=await eda.dmt_Project.getCurrentProjectInfo();if(pr.uuid!=='315433ef1f45b1184319722b4f2939c77ef021639b42a2c9559dabe747dba45a')throw Error('Wrong copy');await eda.dmt_EditorControl.openDocument('268e6597399ebcce');if((await eda.pcb_PrimitiveLine.getAll()).length!==161)throw Error('Unexpected routes');"
code+='const dels='+json.dumps(dropped)+';for(const id of dels)await eda.pcb_PrimitiveLine.delete(id);const rotations='+json.dumps(out['rotations'])+';const capPins=[];for(const q of rotations){const c=await eda.pcb_PrimitiveComponent.modify(q.id,{rotation:180});if(!c)throw Error("Rotation failed");capPins.push({ref:q.ref,rotation:c.getState_Rotation(),pads:(await eda.pcb_PrimitiveComponent.getAllPinsByPrimitiveId(q.id)).map(p=>({number:p.getState_PadNumber(),net:p.getState_Net(),x:p.getState_X(),y:p.getState_Y()}))});}'
code+='const ss='+json.dumps(out['segments'])+';const ids=[];for(const s of ss){const t=await eda.pcb_PrimitiveLine.create(s.net,1,s.x1,s.y1,s.x2,s.y2,6,true);if(!t)throw Error("route");ids.push(t.getState_PrimitiveId());}return {capPins,deleted:dels,created:ids,saved:await eda.pcb_Document.save()};'
(P/'apply_cap_rotation.js').write_text(code,'utf8')
print(json.dumps({'rotate':selected,'removeLines':len(dropped),'newSegments':len(out['segments']),'failures':failure}))
