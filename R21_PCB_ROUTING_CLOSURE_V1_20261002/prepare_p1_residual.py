exec((__import__('pathlib').Path(__file__).parent/'prepare_p1.py').read_text('utf8').rsplit("\nout={'scope'",1)[0])
import time
started=time.monotonic();resPaths=[];resVias=[];resResults=[]
selected=['DIV_SEG8','MCU_ADC_RESET','ROW_SEL0','ROW_SEL1','ROW_SEL3','MCU_ROW0','MCU_ROW1','MCU_ROW2','MCU_ROW3','SPI_MISO','U9_OV_M','U11_CT','U12_CT']
basePaths=len(p1paths);baseVias=len(p1vias)
for net in selected:
 while len(allgroups(net))>1:
  gs=allgroups(net);pairs=sorted((math.hypot(a['x']-b['x'],a['y']-b['y']),a['key'],b['key'],a,b)for i,g in enumerate(gs)for h in gs[:i]for a in g for b in h);made=False
  for dist,ak,bk,a,b in pairs:
   aa=escapes(a);bb=escapes(b)
   for aq,av in aa:
    for bq,bv in bb:
     ax,ay=aq;bx,by=bq;mx,my=(ax+bx)/2,(ay+by)/2
     mids=[(mx,my),(ax,by),(bx,ay)]+[(mx+d,my)for d in(50,-50,100,-100,200,-200,400,-400,600,-600)]+[(mx,my+d)for d in(50,-50,100,-100,200,-200,400,-400,600,-600)]
     for mid in mids:
      if not viaFree(*mid,net):continue
      for first,second in((2,16),(16,2)):
       optionsA=[q for q in candidates(aq,mid)if clear(q,net,first)]
       if not optionsA:continue
       optionsB=[q for q in candidates(mid,bq)if clear(q,net,second)]
       if not optionsB:continue
       # Avoid introducing long digital paths into TIA input/reference islands.
       if net=='SPI_MISO'and any(LineString(q).intersects(k)for q in(optionsA[0],optionsB[0])for k in clockKeepouts):continue
       if av:commit(net,1,[(a['x'],a['y']),aq],ak,'via');addvia(aq,net)
       if bv:commit(net,1,[(b['x'],b['y']),bq],bk,'via');addvia(bq,net)
       commit(net,first,optionsA[0],ak,'transition');addvia(mid,net);commit(net,second,optionsB[0],'transition',bk);made=True;break
      if made:break
     if made:break
     if time.monotonic()-started>45:break
    if made or time.monotonic()-started>45:break
   if made or time.monotonic()-started>45:break
  if not made:break
 resResults.append({'net':net,'remainingGroups':[[p['key']for p in g]for g in allgroups(net)],'escapeCounts':{p['key']:len(escapes(p))for g in allgroups(net)for p in g}})
 if time.monotonic()-started>45:break
resPaths=p1paths[basePaths:];resVias=p1vias[baseVias:]
out={'scope':'Explicit residual layer-change pairs; bounded local construction','results':resResults,'paths':[{k:v for k,v in t.items()if k!='geometry'}for t in resPaths],'vias':[{k:v for k,v in q.items()if k!='geometry'}for q in resVias],'segments':[{'net':t['net'],'layer':t['layer'],'width':6,'x1':a[0],'y1':a[1],'x2':b[0],'y2':b[1]}for t in resPaths for a,b in zip(t['points'],t['points'][1:])]}
(P/'P1_RESIDUAL_PLAN.json').write_text(json.dumps(out,indent=2),'utf8')
base="const pr=await eda.dmt_Project.getCurrentProjectInfo();if(pr.uuid!=='315433ef1f45b1184319722b4f2939c77ef021639b42a2c9559dabe747dba45a')throw Error('Wrong copy');await eda.dmt_EditorControl.openDocument('268e6597399ebcce');const ids=[];"
chunks=[('VIA',out['vias'],[])]
for i in range(0,len(out['segments']),90):chunks.append(('LINE_'+str(i//90),[],out['segments'][i:i+90]))
for i,(label,vs,ss)in enumerate(chunks):
 code=base+'const vs='+json.dumps(vs,separators=(',',':'))+';for(const q of vs){const x=await eda.pcb_PrimitiveVia.create(q.net,q.x,q.y,q.hole,q.diameter);if(!x)throw Error("via");ids.push(x.getState_PrimitiveId());}'
 code+='const ss='+json.dumps(ss,separators=(',',':'))+';for(const s of ss){const t=await eda.pcb_PrimitiveLine.create(s.net,s.layer,s.x1,s.y1,s.x2,s.y2,6,true);if(!t)throw Error("route");ids.push(t.getState_PrimitiveId());}return {created:ids'+(',saved:await eda.pcb_Document.save()'if i==len(chunks)-1 else '')+'};'
 (P/('residual_'+label+'.js')).write_text(code,'utf8')
print(json.dumps({'seconds':time.monotonic()-started,'vias':len(resVias),'segments':len(out['segments']),'results':resResults}))
