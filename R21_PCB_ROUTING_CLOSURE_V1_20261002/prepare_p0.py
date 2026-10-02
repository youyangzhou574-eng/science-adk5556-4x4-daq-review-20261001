import pathlib,json,math,collections
from shapely.geometry import Polygon,LineString,box
from shapely.affinity import rotate,translate
from shapely.ops import unary_union
P=pathlib.Path(__file__).resolve().parent
v=json.loads((P/'START_CAPTURE.json').read_text('utf8'))['parsed']['value']
pads=[];traces=[]
for c in v['parts']:
 for p in c['pads']:
  s=p['pad'];x,y=p['x'],p['y']
  if s[0]=='POLYGON':
   co=[q for q in s[1] if isinstance(q,(int,float))];g=Polygon(list(zip(co[::2],co[1::2])))
  else:g=translate(rotate(box(-s[1]/2,-s[2]/2,s[1]/2,s[2]/2),p['rotation'],origin=(0,0)),x,y)
  pads.append(dict(p,ref=c['ref'],key=c['ref']+'-'+p['number'],geometry=g))
for ln in v['source'].splitlines():
 if '||' not in ln:continue
 h,b=ln.split('||',1)
 try:h=json.loads(h);b=json.loads(b.rstrip('|'))
 except ValueError:continue
 if h['type']=='LINE':
  pts=[(b['startX'],b['startY']),(b['endX'],b['endY'])]
  traces.append({'id':h.get('id'),'net':b['netName'],'layer':b['layerId'],'width':b['width'],'points':pts,'geometry':LineString(pts).buffer(b['width']/2,cap_style=1)})
byNet=collections.defaultdict(list)
for p in pads:
 if p['net']:byNet[p['net']].append(p)
width=6;clearance=6.2;new=[];results=[]
def groups(net):
 ps=byNet[net];objects=[p['geometry'] for p in ps]+[t['geometry'] for t in traces if t['layer']==1 and t['net']==net]
 parent=list(range(len(objects)))
 def root(i):
  while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
  return i
 for i,g in enumerate(objects):
  for j,h in enumerate(objects[:i]):
   if g.intersects(h):parent[root(i)]=root(j)
 out=collections.defaultdict(list)
 for i,p in enumerate(ps):out[root(i)].append(p)
 return list(out.values())
def free(pts,net):
 g=LineString(pts).buffer(width/2+clearance,cap_style=1,join_style=2)
 return not any(g.intersects(p['geometry'])for p in pads if p['layer']in(1,12)and p['net']!=net) and not any(g.intersects(t['geometry'])for t in traces if t['layer']==1 and t['net']!=net)
def candidates(a,b):
 ax,ay=a;bx,by=b;dd=min(abs(bx-ax),abs(by-ay));sx=1 if bx>=ax else -1;sy=1 if by>=ay else -1
 yield[a,(ax+sx*dd,ay+sy*dd),b];yield[a,(bx-sx*dd,by-sy*dd),b]
 yield[a,(ax,by),b];yield[a,(bx,ay),b]
 for d in(20,-20,40,-40,65,-65,100,-100,150,-150):
  yield[a,(ax,ay+d),(bx,ay+d),b];yield[a,(ax+d,ay),(ax+d,by),b]
# Explicit sensitive local work only: distant connector/ADC takeoffs are a separate controlled pass.
nets=['COL_SENSE'+str(i)for i in range(4)]+['TIA_DRV'+str(i)for i in range(4)]+['VCM_FB','VEXC_FB','VCM_DRV','VEXC_DRV']+['ROW_FB'+str(i)for i in range(4)]+['ROW_DRV'+str(i)for i in range(4)]+['COL'+str(i)for i in range(4)]+['TIA'+str(i)for i in range(4)]+['ADC_IN'+str(i)for i in range(4)]+['ADC_REFIO','ADC_REFCAP','DIV_2V25','REF_2V5']+['DIV_SEG'+str(i)for i in range(1,9)]
for net in nets:
 before=len(groups(net))
 while len(groups(net))>1:
  gs=groups(net);pairs=sorted((math.hypot(a['x']-b['x'],a['y']-b['y']),a['key'],b['key'],a,b)for i,g in enumerate(gs)for h in gs[:i]for a in g for b in h)
  made=False
  for dist,ak,bk,a,b in pairs:
   if dist*.0254>13:continue
   for pts in candidates((a['x'],a['y']),(b['x'],b['y'])):
    pts=[q for k,q in enumerate(pts)if k==0 or q!=pts[k-1]]
    if not free(pts,net):continue
    t={'net':net,'layer':1,'width':width,'points':pts,'from':ak,'to':bk,'length_mm':LineString(pts).length*.0254,'geometry':LineString(pts).buffer(width/2,cap_style=1)}
    traces.append(t);new.append(t);made=True;break
   if made:break
  if not made:break
 results.append({'net':net,'beforeGroups':before,'afterGroups':len(groups(net)),'remainingGroups':[[p['key']for p in g]for g in groups(net)]})
out={'scope':'Engineer-selected sensitive local routes only; no global autorouter','paths':[{k:v for k,v in t.items()if k!='geometry'}for t in new],'results':results,'segments':[{'net':t['net'],'layer':1,'width':width,'x1':a[0],'y1':a[1],'x2':b[0],'y2':b[1]}for t in new for a,b in zip(t['points'],t['points'][1:])]}
(P/'P0_LOCAL_ROUTE_PLAN.json').write_text(json.dumps(out,indent=2),'utf8')
code="const pr=await eda.dmt_Project.getCurrentProjectInfo();if(pr.uuid!=='315433ef1f45b1184319722b4f2939c77ef021639b42a2c9559dabe747dba45a')throw Error('Wrong copy');await eda.dmt_EditorControl.openDocument('268e6597399ebcce');if((await eda.pcb_PrimitiveLine.getAll()).length!==93)throw Error('Unexpected initial routes');const ids=[];\n"
code+='const segs='+json.dumps(out['segments'])+';for(const s of segs){const t=await eda.pcb_PrimitiveLine.create(s.net,s.layer,s.x1,s.y1,s.x2,s.y2,s.width,true);if(!t)throw Error("Route failed");ids.push(t.getState_PrimitiveId());}return {created:ids,saved:await eda.pcb_Document.save()};'
(P/'apply_p0.js').write_text(code,'utf8')
print(json.dumps({'paths':len(new),'segments':len(out['segments']),'netsComplete':sum(r['afterGroups']==1 for r in results),'nets':len(results),'remaining':[(r['net'],r['afterGroups'])for r in results if r['afterGroups']>1]}))
