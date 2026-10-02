exec((__import__('pathlib').Path(__file__).parent/'current_geometry.py').read_text('utf8'))
net='GND';groundLinks=[]
# Short ties only within each local ground cluster; do not route ground across board.
while True:
 gs=allgroups(net);made=False
 pairs=sorted((math.hypot(a['x']-b['x'],a['y']-b['y']),a['key'],b['key'],a,b)for i,g in enumerate(gs)for h in gs[:i]for a in g for b in h)
 for dist,ak,bk,a,b in pairs:
  if dist*.0254>3:break
  for pts in candidates((a['x'],a['y']),(b['x'],b['y'])):
   if not clear(pts,net,1):continue
   commit(net,1,pts,ak,bk);groundLinks.append([ak,bk]);made=True;break
  if made:break
 if not made:break
groundGroups=allgroups(net);connectedGroups=[];blocked=[]
for g in groundGroups:
 if any(p['layer']==12 for p in g):connectedGroups.append({'pads':[p['key']for p in g],'throughHole':True});continue
 choices=sorted((LineString([(p['x'],p['y']),q]).length,p['key'],q,p)for p in g for q,vi in escapes(p))
 if not choices:blocked.append([p['key']for p in g]);continue
 dist,ak,q,p=choices[0];commit(net,1,[(p['x'],p['y']),q],ak,'L2 ground via');addvia(q,net);connectedGroups.append({'pads':[p['key']for p in g],'via':q,'stub_mm':dist*.0254})
# A modest perimeter set supplements returns near the connectors/power/analog islands.
stitch=[]
for x,y in [(3,3),(50,3),(97,3),(3,20),(97,40),(3,67),(97,87),(50,87),(3,87)]:
 q=(x/.0254,y/.0254)
 if viaFree(*q,net):addvia(q,net);stitch.append(q)
out={'scope':'Local GND return ties + continuous L2 landing/stitching, no split ground','localTies':groundLinks,'connectedGroups':connectedGroups,'blockedGroups':blocked,'stitching':stitch,'paths':[{k:v for k,v in t.items()if k!='geometry'}for t in p1paths],'vias':[{k:v for k,v in q.items()if k!='geometry'}for q in p1vias],'segments':[{'net':t['net'],'layer':t['layer'],'width':6,'x1':a[0],'y1':a[1],'x2':b[0],'y2':b[1]}for t in p1paths for a,b in zip(t['points'],t['points'][1:])]}
(P/'P2_GROUND_PLAN.json').write_text(json.dumps(out,indent=2),'utf8')
print(json.dumps({'groups':len(groundGroups),'connectedGroups':len(connectedGroups),'groundVias':len(p1vias),'segments':len(out['segments']),'blocked':blocked}))
