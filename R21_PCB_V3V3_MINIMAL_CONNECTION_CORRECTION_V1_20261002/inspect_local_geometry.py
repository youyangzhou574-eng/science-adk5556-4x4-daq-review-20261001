from pathlib import Path
import json,math
P=Path(__file__).parent
f=P/'PRE_CAPTURE.json';v=json.loads(f.read_text('utf8')if f.exists()else(P.parent/'R21_PCB_FINAL_READONLY_VERIFICATION_V1'/'WARM_CAPTURE.json').read_text('utf8'))['parsed']['value']
rs=[]
for ln in v['source'].splitlines():
 if '||'not in ln:continue
 h,b=ln.split('||',1)
 try:rs.append((json.loads(h),json.loads(b.rstrip('|'))))
 except ValueError:pass
pad=next(p for c in v['parts']if c['ref']=='C_MCU1'for p in c['pads']if p['number']=='1')
via=next({'id':h['id'],**b}for h,b in rs if h['type']=='VIA'and h['id']=='d9d6381bb71f0d80')
from shapely.geometry import LineString,Point
for label,obj in [('C_MCU1_1',pad),('e255',via)]:
 x=obj.get('x',obj.get('centerX'));y=obj.get('y',obj.get('centerY'));near=[]
 for h,b in rs:
  if h['type']=='LINE'and b.get('netName')=='V3V3':
   line=LineString([(b['startX'],b['startY']),(b['endX'],b['endY'])]);pt=line.interpolate(line.project(Point(x,y)));near.append({'id':h['id'],'layer':b['layerId'],'width':b['width'],'start':[b['startX'],b['startY']],'end':[b['endX'],b['endY']],'distanceMil':pt.distance(Point(x,y)),'nearest':[pt.x,pt.y]})
 print(label,json.dumps(obj));print(json.dumps(sorted(near,key=lambda q:q['distanceMil'])[:8]))
print('localvias',json.dumps([{'id':h['id'],**b}for h,b in rs if h['type']=='VIA'and 2800<b['centerX']<3450 and 1700<b['centerY']<2000]))
print('localV3pads',json.dumps([{'ref':c['ref'],**p}for c in v['parts']for p in c['pads']if p['net']=='V3V3'and 2800<p['x']<3450 and 1700<p['y']<2200]))
