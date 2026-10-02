exec((__import__('pathlib').Path(__file__).parent/'prepare_p1.py').read_text('utf8').split('for net in selected:')[0])
for label in('P1_SIGNAL_ROUTE_PLAN','P1_RESIDUAL_PLAN'):
 prev=json.loads((P/(label+'.json')).read_text('utf8'))
 for t in prev['paths']:traces.append(dict(t,geometry=LineString(t['points']).buffer(3,cap_style=1)))
 for q in prev['vias']:vias.append(dict(q,geometry=Point(q['x'],q['y']).buffer(12)))
p1paths=[];p1vias=[];finalResults=[]
def dogEsc(p):
 x,y=p['x'],p['y'];out=[(q,vi,[(x,y),q])for q,vi in escapes(p)]
 if p['layer']==12:return out
 for lead in(20,30,45,60):
  for side in(1,-1):
   for step in(35,60,90,130):
    for sign in(1,-1):
     for pts in([ (x,y),(x,y+side*lead),(x+sign*step,y+side*(lead+step))],[(x,y),(x+side*lead,y),(x+side*(lead+step),y+sign*step)]):
      if clear(pts,p['net'],1)and viaFree(*pts[-1],p['net']):out.append((pts[-1],True,pts))
      if len(out)>=18:return out
 return out
selected=['DIV_SEG8','MCU_ADC_RESET','ROW_SEL0','ROW_SEL1','ROW_SEL3','MCU_ROW0','U9_OV_M','U11_CT','U12_CT']
for net in selected:
 while len(allgroups(net))>1:
  gs=allgroups(net);pairs=sorted((math.hypot(a['x']-b['x'],a['y']-b['y']),a['key'],b['key'],a,b)for i,g in enumerate(gs)for h in gs[:i]for a in g for b in h);made=False
  for dist,ak,bk,a,b in pairs:
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
 finalResults.append({'net':net,'remaining':[[p['key']for p in g]for g in allgroups(net)],'escapeCounts':{p['key']:len(dogEsc(p))for g in allgroups(net)for p in g}})
out={'scope':'Nine selected blocked pad fanouts, local doglegs','results':finalResults,'paths':[{k:v for k,v in t.items()if k!='geometry'}for t in p1paths],'vias':[{k:v for k,v in q.items()if k!='geometry'}for q in p1vias],'segments':[{'net':t['net'],'layer':t['layer'],'width':6,'x1':a[0],'y1':a[1],'x2':b[0],'y2':b[1]}for t in p1paths for a,b in zip(t['points'],t['points'][1:])]}
(P/'P1_DOGLEG_PLAN.json').write_text(json.dumps(out,indent=2),'utf8')
base="const pr=await eda.dmt_Project.getCurrentProjectInfo();if(pr.uuid!=='315433ef1f45b1184319722b4f2939c77ef021639b42a2c9559dabe747dba45a')throw Error('Wrong copy');await eda.dmt_EditorControl.openDocument('268e6597399ebcce');const ids=[];"
chunks=[('VIA',out['vias'],[])]+[('LINE_'+str(i//90),[],out['segments'][i:i+90])for i in range(0,len(out['segments']),90)]
for i,(label,vs,ss)in enumerate(chunks):
 code=base+'const vs='+json.dumps(vs,separators=(',',':'))+';for(const q of vs){const x=await eda.pcb_PrimitiveVia.create(q.net,q.x,q.y,q.hole,q.diameter);if(!x)throw Error("via");ids.push(x.getState_PrimitiveId());}'
 code+='const ss='+json.dumps(ss,separators=(',',':'))+';for(const s of ss){const t=await eda.pcb_PrimitiveLine.create(s.net,s.layer,s.x1,s.y1,s.x2,s.y2,6,true);if(!t)throw Error("route");ids.push(t.getState_PrimitiveId());}return {created:ids'+(',saved:await eda.pcb_Document.save()'if i==len(chunks)-1 else '')+'};'
 (P/('dogleg_'+label+'.js')).write_text(code,'utf8')
print(json.dumps({'vias':len(p1vias),'segments':len(out['segments']),'results':finalResults}))
