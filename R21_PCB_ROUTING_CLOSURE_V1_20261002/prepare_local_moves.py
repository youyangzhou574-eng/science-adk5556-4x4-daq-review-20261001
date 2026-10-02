exec((__import__('pathlib').Path(__file__).parent/'current_geometry.py').read_text('utf8'))
from shapely.affinity import rotate as geomrotate
moves=[('C_U14',65,40.5,0),('C_U13',68,40.5,0),('U11_CT_C',75,75.5,90),('U12_CT_C',82,74.5,90),('R_SEL_PD1',49.5,35,90),('U9_OV_B2',18,85.5,0)]
records=[]
for ref,x,y,rot in moves:
 if ref=='U12_CT_C':
  c=next(c for c in v['parts']if c['ref']==ref)
  for tx,ty in[(82,74.5),(81,74),(81,75),(82,75),(83,75),(85,76),(86,78),(83,73),(82,72),(80,74),(80,76)]:
   proposed=[translate(geomrotate(p['geometry'],rot-c['rotation'],origin=(c['x'],c['y'])),tx/.0254-c['x'],ty/.0254-c['y'])for p in pads if p['ref']==ref]
   if any(g.buffer(6.2).intersects(q['geometry'])for g in proposed for q in pads if q['ref']!=ref):continue
   if any(g.buffer(6.2).intersects(t['geometry'])for g in proposed for t in traces if t['layer']==1):continue
   if any(g.buffer(6.2).intersects(q['geometry'])for g in proposed for q in vias):continue
   x,y=tx,ty;break
 c=next(c for c in v['parts']if c['ref']==ref);nx,ny=x/.0254,y/.0254;delta=rot-c['rotation'];angle=math.radians(delta)
 updates=[]
 for p in pads:
  if p['ref']!=ref:continue
  dx,dy=p['x']-c['x'],p['y']-c['y'];px=nx+dx*math.cos(angle)-dy*math.sin(angle);py=ny+dx*math.sin(angle)+dy*math.cos(angle)
  g=translate(geomrotate(p['geometry'],delta,origin=(c['x'],c['y'])),nx-c['x'],ny-c['y'])
  padcollision=[(q['key'],round(q['x']*.0254,3),round(q['y']*.0254,3))for q in pads if q['ref']!=ref and g.buffer(6.2).intersects(q['geometry'])]
  assert not padcollision,'Pad collision '+ref+' '+str(padcollision)
  assert not any(g.buffer(6.2).intersects(t['geometry'])for t in traces if t['layer']in(1,12)and t['net']!=p['net']),'Trace collision '+ref
  collision=[(q['net'],round(q['x']*.0254,3),round(q['y']*.0254,3))for q in vias if q['net']!=p['net']and g.buffer(6.2).intersects(q['geometry'])]
  assert not collision,'Via collision '+ref+' '+str(collision)
  updates.append({'key':p['key'],'x':px,'y':py,'rotation':p['rotation']+delta})
 records.append({'ref':ref,'id':c['id'],'x':nx,'y':ny,'rotation':rot,'before':{'x':c['x'],'y':c['y'],'rotation':c['rotation']},'pads':updates})
(P/'P1_LOCAL_MOVES_PLAN.json').write_text(json.dumps(records,indent=2),'utf8')
code="const pr=await eda.dmt_Project.getCurrentProjectInfo();if(pr.uuid!=='315433ef1f45b1184319722b4f2939c77ef021639b42a2c9559dabe747dba45a')throw Error('Wrong copy');await eda.dmt_EditorControl.openDocument('268e6597399ebcce');const moves="+json.dumps(records,separators=(',',':'))+";const actual=[];for(const q of moves){const c=await eda.pcb_PrimitiveComponent.modify(q.id,{x:q.x,y:q.y,rotation:q.rotation});if(!c)throw Error('move');actual.push({ref:q.ref,x:c.getState_X(),y:c.getState_Y(),rotation:c.getState_Rotation(),pads:(await eda.pcb_PrimitiveComponent.getAllPinsByPrimitiveId(q.id)).map(p=>({number:String(p.getState_PadNumber()),net:p.getState_Net(),x:p.getState_X(),y:p.getState_Y(),rotation:p.getState_Rotation(),pad:p.getState_Pad()}))});}return {actual};"
(P/'apply_local_moves.js').write_text(code,'utf8')
print(json.dumps({'moveCount':len(records),'padAndCopperClearanceScreen':'PASS'}))
