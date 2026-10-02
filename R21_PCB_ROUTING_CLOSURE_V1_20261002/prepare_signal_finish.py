exec((__import__('pathlib').Path(__file__).parent/'current_geometry.py').read_text('utf8'))
exec((P/'prepare_dogleg_escapes.py').read_text('utf8').split('def dogEsc(p):',1)[1].split("selected=['DIV_SEG8'",1)[0].join(['def dogEsc(p):','']))
selected=['MCU_ADC_RESET','ROW_SEL1','ROW_SEL3','MCU_ROW0','U9_OV_M','U11_CT','U12_CT'];results=[]
for net in selected:
 while len(allgroups(net))>1:
  gs=allgroups(net);pairs=sorted((math.hypot(a['x']-b['x'],a['y']-b['y']),a['key'],b['key'],a,b)for i,g in enumerate(gs)for h in gs[:i]for a in g for b in h);made=False
  for dist,ak,bk,a,b in pairs:
   for pts in candidates((a['x'],a['y']),(b['x'],b['y'])):
    if clear(pts,net,1):commit(net,1,pts,ak,bk);made=True;break
   if made:break
   for aq,av,ae in dogEsc(a):
    for bq,bv,be in dogEsc(b):
     routes=[]
     for layer in(2,16):
      for pts in candidates(aq,bq):
       if clear(pts,net,layer):routes=[(layer,pts)];break
      if routes:break
     if not routes:
      ax,ay=aq;bx,by=bq;mx,my=(ax+bx)/2,(ay+by)/2
      for mid in[(mx,my),(ax,by),(bx,ay)]+[(mx+d,my)for d in(100,-100,200,-200,400,-400)]+[(mx,my+d)for d in(100,-100,200,-200,400,-400)]:
       if not viaFree(*mid,net):continue
       for f,s in((2,16),(16,2)):
        ca=[q for q in candidates(aq,mid)if clear(q,net,f)];cb=[q for q in candidates(mid,bq)if clear(q,net,s)]
        if ca and cb:routes=[(f,ca[0]),(s,cb[0])];break
       if routes:break
     if not routes:continue
     if av:commit(net,1,ae,ak,'via');addvia(aq,net)
     if bv:commit(net,1,be,bk,'via');addvia(bq,net)
     for layer,pts in routes:commit(net,layer,pts,ak,bk)
     if len(routes)==2:addvia(routes[0][1][-1],net)
     made=True;break
    if made:break
   if made:break
  if not made:break
 results.append({'net':net,'remaining':[[p['key']for p in g]for g in allgroups(net)]})
out={'scope':'Seven specifically blocked control/RC links after approved local placement adjustment','results':results,'paths':[{k:v for k,v in t.items()if k!='geometry'}for t in p1paths],'vias':[{k:v for k,v in q.items()if k!='geometry'}for q in p1vias],'segments':[{'net':t['net'],'layer':t['layer'],'width':6,'x1':a[0],'y1':a[1],'x2':b[0],'y2':b[1]}for t in p1paths for a,b in zip(t['points'],t['points'][1:])]}
(P/'P1_FINISH_PLAN.json').write_text(json.dumps(out,indent=2),'utf8')
print(json.dumps({'vias':len(p1vias),'segments':len(out['segments']),'results':results}))
