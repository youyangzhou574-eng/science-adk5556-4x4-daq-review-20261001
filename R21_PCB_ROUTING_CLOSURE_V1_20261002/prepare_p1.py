exec((__import__('pathlib').Path(__file__).parent/'prepare_p0_transitions.py').read_text('utf8').split("out={'scope'")[0])
from shapely.geometry import Point
p1paths=[];p1vias=[];p1results=[]
def allgroups(net):
 ps=byNet[net];objs=[(p['geometry'],p['layer'])for p in ps]+[(t['geometry'],t['layer'])for t in traces if t['net']==net]+[(q['geometry'],12)for q in vias if q['net']==net]
 parent=list(range(len(objs)))
 def root(i):
  while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
  return i
 for i,(g,l)in enumerate(objs):
  for j,(h,m)in enumerate(objs[:i]):
   if (l==m or l==12 or m==12)and g.intersects(h):parent[root(i)]=root(j)
 out=collections.defaultdict(list)
 for i,p in enumerate(ps):out[root(i)].append(p)
 return list(out.values())
def commit(net,layer,pts,a,b):
 pts=[q for k,q in enumerate(pts)if k==0 or q!=pts[k-1]]
 if len(pts)<2:return
 t={'net':net,'layer':layer,'width':6,'points':pts,'from':a,'to':b,'geometry':LineString(pts).buffer(3,cap_style=1)};traces.append(t);p1paths.append(t)
def addvia(q,net):
 obj={'net':net,'x':q[0],'y':q[1],'hole':12,'diameter':24,'geometry':Point(*q).buffer(12)};vias.append(obj);p1vias.append(obj)
# Engineer-defined signal set/layer assignments. Local L1 may be used if clear.
# Clock never enters the TIA input island or ADC reference-capacitor region.
selected=['VCM','VEXC']+['ROW_CMD'+str(i)for i in range(4)]+['ROW'+str(i)for i in range(4)]+['COL'+str(i)for i in range(4)]+['DIV_SEG8']
selected+=['ADC_RESET_N','ADC_CS_N','MCU_ENABLE','HW_ENABLE','PG_OK_FAST','MCU_ADC_RESET','PGOOD']+['ROW_SEL'+str(i)for i in range(4)]+['MCU_ROW'+str(i)for i in range(4)]
selected+=['SPI_SCLK','SPI_MOSI','SPI_MISO','SWDIO','SWCLK','UART_TX','UART_RX','MCU_NRST_EXT','SWCLK_EXT','SWDIO_EXT','V3V3_EXT_SWD','V3V3_EXT_UART','UART_TX_EXT','UART_RX_EXT']
for u in(9,10):selected += ['U'+str(u)+'_EN','U'+str(u)+'_PGTH','U'+str(u)+'_OV','U'+str(u)+'_OV_M']
for u,n in((11,4),(12,3)):selected += ['U'+str(u)+'_SENSE','U'+str(u)+'_CT']+['U'+str(u)+'_DIV'+str(i)for i in range(1,n+1)]
layers={n:([2,16] if n.startswith(('MCU_','SPI_','ROW_SEL','SW','UART','PG','ADC_','HW_')) else [16,2]) for n in selected}
layers.update({n:[2,16]for n in selected if n.startswith(('COL','ROW_CMD','ROW0','ROW1','ROW2','ROW3','VCM','VEXC'))})
clockKeepouts=[box(18/.0254,40/.0254,36/.0254,67/.0254),box(48/.0254,55/.0254,65/.0254,68/.0254)]
for net in selected:
 initial=len(allgroups(net));connections=[]
 while len(allgroups(net))>1:
  gs=allgroups(net);pairs=sorted((math.hypot(a['x']-b['x'],a['y']-b['y']),a['key'],b['key'],a,b)for i,g in enumerate(gs)for h in gs[:i]for a in g for b in h);made=False
  for dist,ak,bk,a,b in pairs:
   # Same-layer local implementation is limited to a functional island.
   if dist*.0254<12:
    for pts in candidates((a['x'],a['y']),(b['x'],b['y'])):
     pts=[q for k,q in enumerate(pts)if k==0 or q!=pts[k-1]]
     if len(pts)<2 or not clear(pts,net,1):continue
     if net=='SPI_SCLK'and any(LineString(pts).intersects(k)for k in clockKeepouts):continue
     commit(net,1,pts,ak,bk);connections.append({'from':ak,'to':bk,'layer':1});made=True;break
   if made:break
   for aq,av in escapes(a):
    for bq,bv in escapes(b):
     # Check both proposed via locations against one another/foreign copper.
     for layer in layers[net]:
      options=list(candidates(aq,bq))
      # Explicit ordinary orthogonal channels around the selected functional region.
      ax,ay=aq;bx,by=bq
      for d in(200,-200,350,-350,500,-500):options += [[aq,(ax,ay+d),(bx,ay+d),bq],[aq,(ax+d,ay),(ax+d,by),bq]]
      for pts in options:
       pts=[q for k,q in enumerate(pts)if k==0 or q!=pts[k-1]]
       if len(pts)<2 or not all(20<=x<=100/.0254-20 and 20<=y<=90/.0254-20 for x,y in pts)or not clear(pts,net,layer):continue
       if net=='SPI_SCLK'and any(LineString(pts).intersects(k)for k in clockKeepouts):continue
       if av:commit(net,1,[(a['x'],a['y']),aq],ak,'via');addvia(aq,net)
       if bv:commit(net,1,[(b['x'],b['y']),bq],bk,'via');addvia(bq,net)
       commit(net,layer,pts,ak,bk);connections.append({'from':ak,'to':bk,'layer':layer});made=True;break
      if made:break
     if made:break
    if made:break
   if made:break
  if not made:break
 p1results.append({'net':net,'initialGroups':initial,'finalGroups':len(allgroups(net)),'connections':connections,'remaining':[[p['key']for p in g]for g in allgroups(net)]})
out={'scope':'Controlled engineer-selected ordinary signal connections; no editor/global autorouter','layerAssignments':layers,'clockKeepouts_mm':[[18,40,36,67],[48,55,65,68]],'results':p1results,'vias':[{k:v for k,v in q.items()if k!='geometry'}for q in p1vias],'paths':[{k:v for k,v in t.items()if k!='geometry'}for t in p1paths],'segments':[{'net':t['net'],'layer':t['layer'],'width':t['width'],'x1':a[0],'y1':a[1],'x2':b[0],'y2':b[1]}for t in p1paths for a,b in zip(t['points'],t['points'][1:])]}
(P/'P1_SIGNAL_ROUTE_PLAN.json').write_text(json.dumps(out,indent=2),'utf8')
code="const pr=await eda.dmt_Project.getCurrentProjectInfo();if(pr.uuid!=='315433ef1f45b1184319722b4f2939c77ef021639b42a2c9559dabe747dba45a')throw Error('Wrong copy');await eda.dmt_EditorControl.openDocument('268e6597399ebcce');if((await eda.pcb_PrimitiveLine.getAll()).length!==222)throw Error('Unexpected initial routes');const ids=[];\n"
code+='const vs='+json.dumps(out['vias'])+';for(const q of vs){const x=await eda.pcb_PrimitiveVia.create(q.net,q.x,q.y,q.hole,q.diameter);if(!x)throw Error("via");ids.push(x.getState_PrimitiveId());}\n'
code+='const ss='+json.dumps(out['segments'])+';for(const s of ss){const t=await eda.pcb_PrimitiveLine.create(s.net,s.layer,s.x1,s.y1,s.x2,s.y2,s.width,true);if(!t)throw Error("route");ids.push(t.getState_PrimitiveId());}return {created:ids,saved:await eda.pcb_Document.save()};'
(P/'apply_p1.js').write_text(code,'utf8')
print(json.dumps({'selectedNets':len(selected),'completedNets':sum(r['finalGroups']==1 for r in p1results),'paths':len(p1paths),'segments':len(out['segments']),'vias':len(p1vias),'remaining':[(r['net'],r['finalGroups'])for r in p1results if r['finalGroups']>1]}))
