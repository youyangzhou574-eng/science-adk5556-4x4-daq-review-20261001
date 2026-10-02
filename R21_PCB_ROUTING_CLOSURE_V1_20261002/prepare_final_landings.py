exec((__import__('pathlib').Path(__file__).parent/'prepare_fanout_pockets.py').read_text('utf8').split("(P/'FANOUT_POCKETS_PLAN.json')",1)[0])
fan=out;p1paths=[];p1vias=[]
exec((P/'prepare_dogleg_escapes.py').read_text('utf8').split('def dogEsc(p):',1)[1].split("selected=['DIV_SEG8'",1)[0].replace('(20,30,45,60)','(20,30,45,60,90,120,160)').join(['def dogEsc(p):','']))
def ports(net,g):
 reached=[(p['geometry'],p['layer'])for p in g];pending=[(t['geometry'],t['layer'],None)for t in traces if t['net']==net]+[(q['geometry'],12,q)for q in vias if q['net']==net]
 port=[]
 while True:
  found=[]
  for i,(geom,layer,q)in enumerate(pending):
   if any((layer==l or layer==12 or l==12)and geom.intersects(x)for x,l in reached):found.append(i);reached.append((geom,layer));port += [(q,False,[(q['x'],q['y'])])]if q else []
  if not found:break
  pending=[q for i,q in enumerate(pending)if i not in found]
 return [( (q['x'],q['y']),False,ae)for q,vi,ae in port]+[t for p in g for t in dogEsc(p)]
results=[]
for net in('MCU_ROW0','ROW_SEL3','U12_CT','V5_IN'):
 while len(allgroups(net))>1:
  gs=allgroups(net);made=False
  for i,g in enumerate(gs):
   for h in gs[:i]:
    for aq,av,ae in ports(net,g):
     for bq,bv,be in ports(net,h):
      route=[]
      for layer in(2,16):
       for pts in candidates(aq,bq):
        if clear(pts,net,layer):route=[(layer,pts)];break
       if route:break
      if not route:
       ax,ay=aq;bx,by=bq;mx,my=(ax+bx)/2,(ay+by)/2
       for mid in[(mx,my),(ax,by),(bx,ay)]+[(mx+d,my)for d in(100,-100,200,-200,400,-400)]+[(mx,my+d)for d in(100,-100,200,-200,400,-400)]:
        if not viaFree(*mid,net):continue
        for f,s in((2,16),(16,2)):
         ca=[q for q in candidates(aq,mid)if clear(q,net,f)];cb=[q for q in candidates(mid,bq)if clear(q,net,s)]
         if ca and cb:route=[(f,ca[0]),(s,cb[0])];break
        if route:break
      if not route:continue
      if av:commit(net,1,ae,'pad','via');addvia(aq,net)
      if bv:commit(net,1,be,'pad','via');addvia(bq,net)
      for layer,pts in route:commit(net,layer,pts,'known landing','known landing')
      if len(route)==2:addvia(route[0][1][-1],net)
      made=True;break
     if made:break
    if made:break
   if made:break
  if not made:break
 results.append({'net':net,'groups':[[p['key']for p in g]for g in allgroups(net)]})
out={'scope':'Native-DRC targeted four residual nets with explicitly prepared fanout pockets','results':results,'paths':[{k:v for k,v in t.items()if k!='geometry'}for t in p1paths],'vias':[{k:v for k,v in q.items()if k!='geometry'}for q in p1vias],'segments':[{'net':t['net'],'layer':t['layer'],'width':6,'x1':a[0],'y1':a[1],'x2':b[0],'y2':b[1]}for t in p1paths for a,b in zip(t['points'],t['points'][1:])]}
(P/'FINAL_LANDINGS_PLAN.json').write_text(json.dumps(out,indent=2),'utf8')
print(json.dumps({'segments':len(out['segments']),'vias':len(out['vias']),'results':results}))
