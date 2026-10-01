import pathlib,json,math
from shapely.geometry import LineString,box,Polygon
from shapely.affinity import rotate,translate
P=pathlib.Path(__file__).resolve().parent
src=(P/'PCB_DRC_01_SOURCE.txt').read_text('utf8');lines={}
for ln in src.splitlines():
 bits=ln.split('||')
 if len(bits)!=2:continue
 h=json.loads(bits[0]);b=json.loads(bits[1].rstrip('|'))
 if h['type']=='LINE':lines[h['id']]=b
cap=json.loads((P/'PCB_FLOORPLAN_CAPTURE.json').read_text('utf8'))['parsed']['value'];geoms=[]
for c in cap['parts']:
 for p in c['pads']:
  s=p['pad']
  if s[0]=='POLYGON':co=[n for n in s[1]if isinstance(n,(int,float))];g=Polygon(list(zip(co[::2],co[1::2])))
  else:g=translate(rotate(box(-s[1]/2,-s[2]/2,s[1]/2,s[2]/2),p['rotation'],origin=(0,0)),p['x'],p['y'])
  geoms.append((p['net'],g))
data=json.loads((P/'PCB_DRC_01.json').read_text('utf8'))['parsed']['value']['result'];fix=[]
for group in data:
 if group['name']!='Clearance Error':continue
 for sub in group['list']:
  for e in sub['list']:
   line=lines[e['objs'][0]];dx=line['endX']-line['startX'];dy=line['endY']-line['startY'];mag=math.hypot(dx,dy)
   assert mag>1
   candidates=[]
   for sx,sy in [(0,.8),(0,-.8),(.8,0),(-.8,0),(.6,.6),(.6,-.6),(-.6,.6),(-.6,-.6)]:
    prop={'startX':round(line['startX']+sx,1),'startY':round(line['startY']+sy,1),'endX':round(line['endX']+sx,1),'endY':round(line['endY']+sy,1)}
    g=LineString([(prop['startX'],prop['startY']),(prop['endX'],prop['endY'])]).buffer(3,cap_style=2)
    distance=min(g.distance(p)for net,p in geoms if net!=line['netName']);candidates.append((distance,prop))
   distance,prop=max(candidates,key=lambda a:a[0]);assert distance>=6.1
   fix.append({'id':e['objs'][0],'property':prop,'net':line['netName'],'staticMinMil':distance,'nativeOldMin':'5.9mil','required':'6mil','neighborOverlapPreservedBy6milWidth':True})
assert len(fix)==2
(P/'CLEARANCE_CORRECTION_PLAN.json').write_text(json.dumps(fix,indent=2),'utf8')
code='const fixes='+json.dumps(fix,separators=(',',':'))+';await eda.dmt_EditorControl.openDocument("268e6597399ebcce");for(const f of fixes){const r=await eda.pcb_PrimitiveLine.modify(f.id,f.property);if(!r)throw Error("Correction "+f.id);}return {fixes,saved:await eda.pcb_Document.save()};'
(P/'fix_two_clearances.js').write_text(code,'utf8');print(json.dumps(fix))
