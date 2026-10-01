import pathlib,json,math,collections,itertools
from shapely.geometry import Polygon,Point,LineString,box
from shapely.affinity import rotate,translate
P=pathlib.Path(__file__).resolve().parent
v=json.loads((P/'PCB_FLOORPLAN_CAPTURE.json').read_text('utf8'))['parsed']['value'];pads=[]
for c in v['parts']:
 for p in c['pads']:
  sh=p['pad'];x,y=p['x'],p['y']
  if sh[0]=='POLYGON':
   co=[n for n in sh[1]if isinstance(n,(int,float))];g=Polygon(list(zip(co[::2],co[1::2])))
  else:
   w,h=sh[1:3];g=box(-w/2,-h/2,w/2,h/2);g=translate(rotate(g,p['rotation'],origin=(0,0)),x,y)
  pads.append(dict(p,ref=c['ref'],geometry=g))
byNet=collections.defaultdict(list)
for p in pads:
 if p['net']:byNet[p['net']].append(p)
width=6;clearance=6;traces=[];results=[]
def free(points,net):
 line=LineString(points);g=line.buffer(width/2+clearance,cap_style=2,join_style=2)
 if any(g.intersects(p['geometry'])for p in pads if p['net']!=net):return False
 if any(g.intersects(t['geometry'])for t in traces if t['net']!=net):return False
 return True
def candidates(a,b):
 ax,ay=a;bx,by=b;dx=bx-ax;dy=by-ay;sgx=1 if dx>=0 else -1;sgy=1 if dy>=0 else -1;dd=min(abs(dx),abs(dy))
 yield [a,(ax+sgx*dd,ay+sgy*dd),b];yield [a,(bx-sgx*dd,by-sgy*dd),b]
 yield [a,(ax,by),b];yield [a,(bx,ay),b]
 # Bounded ordinary local escape elbows, no new global routing engine.
 for d in (30,-30,60,-60,100,-100):
  yield[a,(ax,ay+d),(bx,ay+d),b];yield[a,(ax+d,ay),(ax+d,by),b]
nets=['VCM_FB','VEXC_FB','VCM_DRV','VEXC_DRV']
for i in range(4):nets +=['COL_SENSE'+str(i),'TIA_DRV'+str(i),'ROW_FB'+str(i),'ROW_DRV'+str(i)]
# Local feedback RF/CF endpoints are explicitly included after high-frequency compensation loops.
nets +=['TIA'+str(i)for i in range(4)]
for net in nets:
 ps=byNet[net];connected={0};unconnected=set(range(1,len(ps)));failed=[]
 while unconnected:
  pairs=sorted(((math.hypot(ps[i]['x']-ps[j]['x'],ps[i]['y']-ps[j]['y']),i,j)for i in connected for j in unconnected))
  made=False
  for dist,i,j in pairs:
   a=(ps[i]['x'],ps[i]['y']);b=(ps[j]['x'],ps[j]['y'])
   # Avoid routing to the distant ADC through the same-layer critical local pass.
   if dist*.0254>12:continue
   for points in candidates(a,b):
    points=[x for k,x in enumerate(points)if k==0 or x!=points[k-1]]
    if free(points,net):
     geom=LineString(points).buffer(width/2,cap_style=2,join_style=2)
     traces.append({'net':net,'layer':1,'width':width,'points':points,'from':ps[i]['ref']+'-'+ps[i]['number'],'to':ps[j]['ref']+'-'+ps[j]['number'],'geometry':geom});connected.add(j);unconnected.remove(j);made=True;break
   if made:break
  if not made:break
 results.append({'net':net,'padCount':len(ps),'connectedInThisPass':len(connected),'unconnected':[ps[j]['ref']+'-'+ps[j]['number']for j in sorted(unconnected)]})
segments=[{'net':t['net'],'layer':1,'width':width,'x1':a[0],'y1':a[1],'x2':b[0],'y2':b[1]}for t in traces for a,b in zip(t['points'],t['points'][1:])if a!=b]
(P/'LOCAL_ROUTE_PLAN.json').write_text(json.dumps({'widthMil':width,'clearanceMil':clearance,'status':'LOCAL_CRITICAL_PASS_ONLY_NOT_FULL_BOARD_ROUTING','paths':[{k:v for k,v in t.items()if k!='geometry'}for t in traces],'segments':segments,'results':results,'assumptions':'Conservative rectangular pad envelopes; excludes any wrong-net/NC pad and already planned wrong-net local track. Native DRC is authoritative.'},indent=2),'utf8')
code='const segs='+json.dumps(segments,separators=(',',':'))+';\n'
code+='''const pr=await eda.dmt_Project.getCurrentProjectInfo();if(pr.uuid!=="e58f223d256cd14d13a6fb04a0e150585301864f01c50827f9241f5945cf2801")throw Error('Wrong copy');await eda.dmt_EditorControl.openDocument('268e6597399ebcce');if((await eda.pcb_PrimitiveLine.getAll()).length!==0)throw Error('Unexpected existing routes; no duplicate');const ids=[];for(const s of segs){const l=await eda.pcb_PrimitiveLine.create(s.net,1,s.x1,s.y1,s.x2,s.y2,s.width,true);if(!l)throw Error('Local route');ids.push(l.getState_PrimitiveId());}const poly=eda.pcb_MathPolygon.createPolygon([20,20,'L',100/.0254-20,20,100/.0254-20,90/.0254-20,20,90/.0254-20,20,20]);if(!poly)throw Error('Ground polygon');const ground=await eda.pcb_PrimitivePour.create('GND',15,poly,undefined,false,'L2_CONTINUOUS_GND_REVIEW',0,6,true);if(!ground)throw Error('Ground pour');return {ids,ground:ground.getState_PrimitiveId(),saved:await eda.pcb_Document.save()};'''
(P/'route_local.js').write_text(code,'utf8')
print(json.dumps({'localPaths':len(traces),'segments':len(segments),'netsComplete':sum(not r['unconnected']for r in results),'netsTotal':len(results),'fullRouting':False}))
