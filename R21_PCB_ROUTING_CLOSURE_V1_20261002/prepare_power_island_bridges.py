exec((__import__('pathlib').Path(__file__).parent/'filled_geometry.py').read_text('utf8').replace('FILLED_CAPTURE.json','WARM_CAPTURE.json'))
p1paths=[];p1vias=[]
def copperPorts(net,p):
 reached=[(p['geometry'],p['layer'])];pending=[(t['geometry'],t['layer'],None)for t in traces if t['net']==net]+[(q['geometry'],12,q)for q in vias if q['net']==net];rv=[]
 while True:
  found=[]
  for i,(g,l,q)in enumerate(pending):
   if any((l==a or l==12 or a==12)and g.intersects(h)for h,a in reached):found.append(i);reached.append((g,l));rv.extend([q]if q else [])
  if not found:break
  pending=[q for i,q in enumerate(pending)if i not in found]
 return rv
keys={p['key']:p for p in pads}
selected=['C_ADCA2-1','U11_TOP0-1','C_MCU1-1','U10_BLEED-1','U10_PG_T-1','U10-6']
badIds=set(q['id']for key in selected for q in copperPorts(keys[key]['net'],keys[key]))
results=[]
for key in selected:
 p=keys[key];net=p['net'];current=copperPorts(net,p)
 # After each selected bridge, if already reaches a non-island landing, skip.
 if any(q['id']not in badIds for q in current):results.append({'key':key,'alreadyBridged':True});continue
 pairs=sorted((math.hypot(a['x']-b['x'],a['y']-b['y']),a['id'],b['id'],a,b)for a in current for b in vias if b['net']==net and b['id']not in badIds)
 made=False
 for dist,ai,bi,a,b in pairs[:120]:
  for width in(20,12,6):
   for layer in(2,16):
    for pts in candidates((a['x'],a['y']),(b['x'],b['y'])):
     if clear(pts,net,layer,width):
      t={'net':net,'layer':layer,'width':width,'points':pts,'from':key,'to':bi,'geometry':LineString(pts).buffer(width/2)};traces.append(t);p1paths.append(t);made=True;break
    if made:break
   if made:break
  if made:break
 if not made:
  for dist,ai,bi,a,b in pairs[:50]:
   mx,my=(a['x']+b['x'])/2,(a['y']+b['y'])/2
   mids=[(mx+d,my)for d in(0,80,-80,160,-160,300,-300)]+[(mx,my+d)for d in(80,-80,160,-160,300,-300)]
   for q in mids:
    if not viaFree(*q,net)or any(math.hypot(q[0]-v['x'],q[1]-v['y'])<23.9 for v in vias):continue
    for width in(20,12,6):
     for l1,l2 in((2,16),(16,2)):
      ca=[pts for pts in candidates((a['x'],a['y']),q)if clear(pts,net,l1,width)];cb=[pts for pts in candidates(q,(b['x'],b['y']))if clear(pts,net,l2,width)]
      if not ca or not cb:continue
      addvia(q,net)
      for layer,pts in((l1,ca[0]),(l2,cb[0])):
       t={'net':net,'layer':layer,'width':width,'points':pts,'from':key,'to':bi,'geometry':LineString(pts).buffer(width/2)};traces.append(t);p1paths.append(t)
      made=True;break
     if made:break
    if made:break
   if made:break
 results.append({'key':key,'prepared':made,'fromVia':ai if made else None,'toVia':bi if made else None,'width':width if made else None,'ports':[(q['id'],q['x'],q['y'])for q in current]})
out={'scope':'Six selected native DRC power-island pads to existing non-island landings','results':results,'vias':[],'segments':[{'net':t['net'],'layer':t['layer'],'width':t['width'],'x1':a[0],'y1':a[1],'x2':b[0],'y2':b[1]}for t in p1paths for a,b in zip(t['points'],t['points'][1:])]}
out['vias']=[{k:v for k,v in q.items()if k!='geometry'}for q in p1vias]
(P/'POWER_ISLAND_BRIDGES_PLAN.json').write_text(json.dumps(out,indent=2),'utf8')
assert all(x.get('alreadyBridged')or x.get('prepared')for x in results),results
base="const pr=await eda.dmt_Project.getCurrentProjectInfo();if(pr.uuid!=='315433ef1f45b1184319722b4f2939c77ef021639b42a2c9559dabe747dba45a')throw Error('Wrong copy');await eda.dmt_EditorControl.openDocument('268e6597399ebcce');const ids=[];"
code=base+'const vs='+json.dumps(out['vias'],separators=(',',':'))+';for(const q of vs){const t=await eda.pcb_PrimitiveVia.create(q.net,q.x,q.y,q.hole,q.diameter);if(!t)throw Error("via");ids.push(t.getState_PrimitiveId());}const ss='+json.dumps(out['segments'],separators=(',',':'))+';for(const s of ss){const t=await eda.pcb_PrimitiveLine.create(s.net,s.layer,s.x1,s.y1,s.x2,s.y2,s.width,true);if(!t)throw Error("Power bridge");ids.push(t.getState_PrimitiveId());}return {created:ids,fillPending:true};'
(P/'apply_power_island_bridges.js').write_text(code,'utf8')
print(json.dumps({'results':results,'segments':len(out['segments']),'segmentsDetail':out['segments']}))
