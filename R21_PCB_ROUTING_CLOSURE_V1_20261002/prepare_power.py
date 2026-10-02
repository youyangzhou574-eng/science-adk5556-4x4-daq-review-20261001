exec((__import__('pathlib').Path(__file__).parent/'prepare_ground.py').read_text('utf8').rsplit("\nout={'scope'",1)[0])
from shapely.geometry import Polygon
p1paths=[];p1vias=[];results=[]
v3pts=[(67,1),(99,1),(99,89),(56,89),(56,74),(67,74),(67,54),(54,54),(54,43),(58,43),(58,30),(67,30),(67,1)]
v3=Polygon([(x/.0254,y/.0254)for x,y in v3pts]);v5=box(20,20,100/.0254-20,90/.0254-20).difference(v3)
def powerCommit(net,layer,pts,ak,bk,width):
 pts=[q for k,q in enumerate(pts)if k==0 or q!=pts[k-1]]
 if len(pts)<2:return
 t={'net':net,'layer':layer,'width':width,'points':pts,'from':ak,'to':bk,'geometry':LineString(pts).buffer(width/2,cap_style=1)};traces.append(t);p1paths.append(t)
for net,plane in(('V5',v5),('V3V3',v3)):
 # Local ties reduce ground/via congestion; each remaining group lands on its power copper.
 while True:
  gs=allgroups(net);made=False
  pairs=sorted((math.hypot(a['x']-b['x'],a['y']-b['y']),a['key'],b['key'],a,b)for i,g in enumerate(gs)for h in gs[:i]for a in g for b in h)
  for dist,ak,bk,a,b in pairs:
   if dist*.0254>3:break
   for pts in candidates((a['x'],a['y']),(b['x'],b['y'])):
    if not clear(pts,net,1,w=12):continue
    powerCommit(net,1,pts,ak,bk,12);made=True;break
   if made:break
  if not made:break
 gs=allgroups(net);ok=[];blocked=[]
 for g in gs:
  choices=sorted((LineString([(p['x'],p['y']),q]).length,p['key'],q,p)for p in g for q,vi in escapes(p))
  landed=False
  for dist,ak,q,p in choices:
   if plane.contains(Point(*q).buffer(20)):
    stub=[(p['x'],p['y']),q]
    powerCommit(net,1,stub,ak,'power plane',12 if clear(stub,net,1,w=12) else 6)
    addvia(q,net);ok.append({'pads':[p['key']for p in g],'via':q});landed=True;break
   # Rare supply nodes outside the dominant region use a short wider bridge to its copper.
   for dx,dy in[(0,-150),(0,150),(-150,0),(150,0),(0,-300),(0,300),(-300,0),(300,0),(-500,0),(500,0)]:
    r=(q[0]+dx,q[1]+dy)
    if not plane.contains(Point(*r).buffer(20))or not viaFree(*r,net):continue
    for pts in candidates(q,r):
     if not clear(pts,net,2,w=12):continue
     powerCommit(net,1,[(p['x'],p['y']),q],ak,'via',6);addvia(q,net);powerCommit(net,2,pts,ak,'plane landing',12);addvia(r,net);ok.append({'pads':[p['key']for p in g],'bridge':pts});landed=True;break
    if landed:break
   if landed:break
  if not landed:blocked.append([p['key']for p in g])
 results.append({'net':net,'landed':ok,'blocked':blocked})
# The raw input and pre-protection LDO rails remain explicit wide routes, no accidental plane merge.
for net in('V5_IN','V3_LDO'):
 while len(allgroups(net))>1:
  gs=allgroups(net);pairs=sorted((math.hypot(a['x']-b['x'],a['y']-b['y']),a['key'],b['key'],a,b)for i,g in enumerate(gs)for h in gs[:i]for a in g for b in h);made=False
  for dist,ak,bk,a,b in pairs:
   for pts in candidates((a['x'],a['y']),(b['x'],b['y'])):
    if clear(pts,net,1,w=16):powerCommit(net,1,pts,ak,bk,16);made=True;break
   if made:break
   for aq,av in escapes(a):
    for bq,bv in escapes(b):
     for layer in(16,2):
      for pts in candidates(aq,bq):
       if not clear(pts,net,layer,w=20):continue
       if av:powerCommit(net,1,[(a['x'],a['y']),aq],ak,'via',6);addvia(aq,net)
       if bv:powerCommit(net,1,[(b['x'],b['y']),bq],bk,'via',6);addvia(bq,net)
       powerCommit(net,layer,pts,ak,bk,20);made=True;break
      if made:break
     if made:break
    if made:break
   if made:break
  if not made:break
 results.append({'net':net,'remaining':[[p['key']for p in g]for g in allgroups(net)]})
out={'scope':'Wider supply copper and local power landings; native fill still required','V5Pour_mm':[[.508,.508],[99.492,.508],[99.492,89.492],[.508,89.492],[.508,.508]],'V3V3Pour_mm':v3pts,'results':results,'paths':[{k:v for k,v in t.items()if k!='geometry'}for t in p1paths],'vias':[{k:v for k,v in q.items()if k!='geometry'}for q in p1vias],'segments':[{'net':t['net'],'layer':t['layer'],'width':t['width'],'x1':a[0],'y1':a[1],'x2':b[0],'y2':b[1]}for t in p1paths for a,b in zip(t['points'],t['points'][1:])]}
(P/'P2_POWER_PLAN.json').write_text(json.dumps(out,indent=2),'utf8')
print(json.dumps({'vias':len(p1vias),'segments':len(out['segments']),'blocked':[{k:r[k]for k in('net','blocked','remaining')if k in r}for r in results]}))
