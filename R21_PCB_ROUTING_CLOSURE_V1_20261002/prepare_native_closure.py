exec((__import__('pathlib').Path(__file__).parent/'filled_geometry.py').read_text('utf8'))
deleted=[];seen={}
for q in vias:
 key=(q['net'],q['x'],q['y'],q['diameter'],q['hole'])
 if key in seen:deleted.append(q['id'])
 else:seen[key]=q
vias[:]=[q for q in vias if q['id']not in deleted]
result=[]
selected=['MCU_ROW0','ROW_SEL3','U12_CT','V5_IN']
for net in selected:
 while len(allgroups(net))>1:
  gs=allgroups(net);pairs=sorted((math.hypot(a['x']-b['x'],a['y']-b['y']),a['key'],b['key'],a,b)for i,g in enumerate(gs)for h in gs[:i]for a in g for b in h);made=False
  for dist,ak,bk,a,b in pairs:
   for pts in candidates((a['x'],a['y']),(b['x'],b['y'])):
    if clear(pts,net,1):commit(net,1,pts,ak,bk);made=True;break
   if made:break
   for aq,av,ae in dogEsc(a):
    for bq,bv,be in dogEsc(b):
     for layer in(2,16):
      for pts in candidates(aq,bq):
       if not clear(pts,net,layer):continue
       if av:commit(net,1,ae,ak,'via');addvia(aq,net)
       if bv:commit(net,1,be,bk,'via');addvia(bq,net)
       commit(net,layer,pts,ak,bk);made=True;break
      if made:break
     if made:break
    if made:break
   if made:break
  if not made:break
 result.append({'net':net,'groups':[[p['key']for p in g]for g in allgroups(net)],'escapeCounts':{p['key']:len(dogEsc(p))for g in allgroups(net)for p in g}})
out={'deleteExactDuplicateVias':deleted,'swapPowerPourPriorities':True,'results':result,'paths':[{k:v for k,v in t.items()if k!='geometry'}for t in p1paths],'vias':[{k:v for k,v in q.items()if k!='geometry'}for q in p1vias],'segments':[{'net':t['net'],'layer':t['layer'],'width':6,'x1':a[0],'y1':a[1],'x2':b[0],'y2':b[1]}for t in p1paths for a,b in zip(t['points'],t['points'][1:])]}
(P/'NATIVE_CLOSURE_PLAN.json').write_text(json.dumps(out,indent=2),'utf8')
print(json.dumps({'exactDuplicateVias':len(deleted),'vias':len(p1vias),'segments':len(out['segments']),'results':result}))
