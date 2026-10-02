exec((__import__('pathlib').Path(__file__).parent/'local_plane_geometry.py').read_text('utf8').split('items=[]',1)[0])
from shapely.affinity import translate,rotate
def othernet_obstacles(layer):
 out=[]
 for h,b in rs:
  if h['type']=='LINE'and b['netName']!='V3V3'and b['layerId']==layer:out.append((h['id'],b['netName'],LineString([(b['startX'],b['startY']),(b['endX'],b['endY'])]).buffer(b['width']/2)))
  if h['type']=='VIA'and b['netName']!='V3V3':out.append((h['id'],b['netName'],Point(b['centerX'],b['centerY']).buffer(b['viaDiameter']/2)))
  if h['type']=='POURED':
   pid=json.loads(h['id'])[1];bound=next(z for a,z in rs if a['type']=='POUR'and a['id']==pid)
   if bound['netName']=='V3V3'or bound['layerId']!=layer:continue
   for chunk in b['pourFill']:
    if not chunk.get('fill'):continue
    ps=chunk['path'];ps=ps if isinstance(ps[0],list)else[ps];rings=[points(p)for p in ps];g=Polygon(rings[0],rings[1:]);g=g if g.is_valid else g.buffer(0);out.append((pid+'#fill',bound['netName'],g))
 for c in v['parts']:
  for p in c['pads']:
   if p['net']=='V3V3'or p['layer']not in(layer,12):continue
   s=p['pad']
   if s[0]=='POLYGON':continue
   g=translate(rotate(box(-s[1]/2,-s[2]/2,s[1]/2,s[2]/2),p['rotation'],origin=(0,0)),p['x'],p['y']);out.append((c['ref']+'-'+p['number'],p['net'],g))
 return out
old=P/'TWO_LOCAL_BRIDGES_PLAN.json'
if old.exists()and not(P/'INITIAL_REJECTED_GEOMETRY_PLAN.json').exists():(P/'INITIAL_REJECTED_GEOMETRY_PLAN.json').write_bytes(old.read_bytes())
if old.exists():(P/'TOP_BRIDGE_REJECTED_FILLED_GND_PLAN.json').write_bytes(old.read_bytes())
choices=[{'label':'C_MCU1 exact native DRC pad landing to existing main-plane via26','layer':1,'width':12,'points':[[3200.7865,1822.8346],[3160.05,1822.8]],'replaceLocalLine':'c131c12ef419b393'}, {'label':'e255 short bottom bridge to one V3V3 via on main plane right of MCU_ROW0 barrier','layer':2,'width':12,'points':[[3317.55,1830.7],[3340,1830.7],[3380,1790.7]],'replaceLocalLine':None}]
for q in choices:
 g=LineString(q['points']).buffer(6);near=[{'object':i,'net':n,'gapMil':g.distance(o)}for i,n,o in othernet_obstacles(q['layer'])if g.distance(o)<6-1e-7];q['geometricScreenOtherNetClearanceBelow6Mil']=near
via={'net':'V3V3','x':3380,'y':1790.7,'hole':12,'diameter':24};vg=Point(via['x'],via['y']).buffer(12)
check=[]
for layer in(1,2,16):
 for i,n,g in othernet_obstacles(layer):
  if '#fill'in i:continue
  if vg.distance(g)<6-1e-7:check.append({'layer':layer,'object':i,'net':n,'gapMil':vg.distance(g)})
via['geometricOtherNetClearanceBelow6Mil']=check
(P/'TWO_LOCAL_BRIDGES_PLAN.json').write_text(json.dumps({'scope':'two GUI-observed native DRC objects only; static screen not nativeDRC PASS','bridges':choices,'newVias':[via],'componentMoves':0,'unchangedRule':True,'note':'new via requires normal same-layer plane antipad behavior; nativeDRC must confirm; no explicit pour rebuild permitted by strict object scope'},indent=2),'utf8');print(json.dumps({'bridges':choices,'via':via}))
