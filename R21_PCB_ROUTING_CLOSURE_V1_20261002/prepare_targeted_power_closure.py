exec((__import__('pathlib').Path(__file__).parent/'prepare_final_landings.py').read_text('utf8').split("(P/'FINAL_LANDINGS_PLAN.json')",1)[0])
# Selected native DRC power/ground residual pads only; no signal rerouting.
p1paths=[];p1vias=[];results=[]
bridgeChanges=[{'id':'004870631cdb8bbb','net':'VCM','points':[(1770.7,1360),(1693.9,1360)]},{'id':'2c98326fff7d7641','net':'VCM','points':[(1693.9,1360),(1693.9,1491)]},{'id':'91570b28085432ee','net':'VCM','points':[(1770.7,1491),(1770.7,1360)]}]
traces[:]=[t for t in traces if t.get('id')not in {x['id']for x in bridgeChanges}]
for t in bridgeChanges:
 assert clear(t['points'],'VCM',1),t
 traces.append(dict(t,layer=1,width=6,geometry=LineString(t['points']).buffer(3)))
targets=['U11-2','U11_CT_C-2','U11_BOT-2','U12_BOT-2','U12-2','U11_SENSE_C-2','U12_SENSE_C-2','R_SEL_PD2-2','R_SEL_PD0-2','C_TIA_OP-2','C_ROW_OP-2','D_ROW0-1','C_MUX-1','U4-16','C_ADCA2-1','U11_TOP0-1','U10_BLEED-1','U10_PG_T-1','U5-34']
keys={p['key']:p for p in pads}
for key in targets:
 p=keys[key];net=p['net'];made=False
 # Prefer the already existing same-net ground/power landing before a new via.
 near=sorted((q for q in vias if q['net']==net),key=lambda q:math.hypot(q['x']-p['x'],q['y']-p['y']))[:18]
 for q in near:
  for pts in candidates((p['x'],p['y']),(q['x'],q['y'])):
   if clear(pts,net,1):commit(net,1,pts,key,'existing plane via');made=True;break
  if made:break
 if not made:
  for q,av,pts in dogEsc(p):
   if av and any(math.hypot(q[0]-v['x'],q[1]-v['y'])<23.9 for v in vias):continue
   if av:commit(net,1,pts,key,'new plane landing');addvia(q,net)
   made=True;break
 if not made:
  # Bounded local three-vertex escape inside 160 mil of this selected pad.
  x,y=p['x'],p['y']
  for d in(25,35,45,55,70,90,120,160):
   for sx,sy in((1,0),(-1,0),(0,1),(0,-1)):
    mid=(x+sx*d,y+sy*d)
    if not clear([(x,y),mid],net,1):continue
    for side in(1,-1):
     for run in(35,55,75,100,140):
      q=(mid[0]+sy*side*run,mid[1]+sx*side*run)
      if not viaFree(*q,net)or any(math.hypot(q[0]-v['x'],q[1]-v['y'])<23.9 for v in vias):continue
      if clear([mid,q],net,1):
       commit(net,1,[(x,y),mid,q],key,'selected local elbow plane via');addvia(q,net);made=True;break
     if made:break
    if made:break
   if made:break
 results.append({'key':key,'net':net,'prepared':made})
out={'results':results,'vias':[{k:v for k,v in q.items()if k!='geometry'}for q in p1vias],'segments':[{'net':t['net'],'layer':t['layer'],'width':6,'x1':a[0],'y1':a[1],'x2':b[0],'y2':b[1]}for t in p1paths for a,b in zip(t['points'],t['points'][1:])]}
out['bridgeChanges']=bridgeChanges
(P/'TARGETED_POWER_CLOSURE_PLAN.json').write_text(json.dumps(out,indent=2),'utf8')
print(json.dumps({'vias':len(out['vias']),'segments':len(out['segments']),'results':results}))
