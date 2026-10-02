from pathlib import Path
import json,math
from shapely.geometry import Point,Polygon,LineString,box
from shapely.affinity import rotate,translate
from shapely.ops import unary_union,nearest_points
P=Path(__file__).parent;v=json.loads((P/'PRE_CAPTURE.json').read_text('utf8'))['parsed']['value'];rs=[]
for ln in v['source'].splitlines():
 if '||'not in ln:continue
 h,b=ln.split('||',1)
 try:rs.append((json.loads(h),json.loads(b.rstrip('|'))))
 except ValueError:pass
def points(path):
 x,y=path[:2];out=[(x*10,y*10)];i=2;mode='L'
 while i<len(path):
  if isinstance(path[i],str):mode=path[i];i+=1;continue
  if mode=='ARC':
   ang,nx,ny=path[i:i+3];i+=3;theta=math.radians(ang);dx,dy=nx-x,ny-y
   if abs(math.sin(theta/2))>1e-10:
    cx=(x+nx)/2-dy/(2*math.tan(theta/2));cy=(y+ny)/2+dx/(2*math.tan(theta/2));sx,sy=x-cx,y-cy;n=max(4,math.ceil(abs(ang)/2))
    for k in range(1,n+1):
     t=theta*k/n;out.append(((cx+sx*math.cos(t)-sy*math.sin(t))*10,(cy+sx*math.sin(t)+sy*math.cos(t))*10))
   else:out.append((nx*10,ny*10))
   x,y=nx,ny;mode='L'
  else:x,y=path[i:i+2];i+=2;out.append((x*10,y*10))
 return out
items=[];fills=[]
for h,b in rs:
 if h['type']=='LINE'and b['netName']=='V3V3':items.append({'id':h['id'],'layer':b['layerId'],'kind':'LINE','g':LineString([(b['startX'],b['startY']),(b['endX'],b['endY'])]).buffer(b['width']/2)})
 if h['type']=='VIA'and b['netName']=='V3V3':items.append({'id':h['id'],'layer':12,'kind':'VIA','g':Point(b['centerX'],b['centerY']).buffer(b['viaDiameter']/2)})
 if h['type']=='POURED':
  pid=json.loads(h['id'])[1];bound=next(z for q,z in rs if q['type']=='POUR'and q['id']==pid)
  if bound['netName']!='V3V3':continue
  for chunk in b['pourFill']:
   if not chunk.get('fill'):continue
   ps=chunk['path'];ps=ps if isinstance(ps[0],list)else[ps];rings=[points(p)for p in ps];g=Polygon(rings[0],rings[1:]);g=g if g.is_valid else g.buffer(0)
   for n,sub in enumerate(g.geoms if g.geom_type=='MultiPolygon'else[g]):fills.append({'id':pid+'#'+str(len(fills)),'layer':bound['layerId'],'kind':'FILL','g':sub});items.append(fills[-1])
for c in v['parts']:
 for p in c['pads']:
  if p['net']!='V3V3':continue
  s=p['pad'];g=translate(rotate(box(-s[1]/2,-s[2]/2,s[1]/2,s[2]/2),p['rotation'],origin=(0,0)),p['x'],p['y'])
  items.append({'id':c['ref']+'-'+p['number'],'layer':p['layer'],'kind':'PAD','g':g})
parent=list(range(len(items)))
def find(i):
 while parent[i]!=i:i=parent[i]
 return i
for i,a in enumerate(items):
 for j,b in enumerate(items[:i]):
  if(a['layer']==b['layer']or a['layer']==12 or b['layer']==12)and a['g'].intersects(b['g']):parent[find(i)]=find(j)
groups={}
for i,q in enumerate(items):groups.setdefault(find(i),[]).append(q)
out={'scope':'offline geometry screen only; nativeDRC authoritative','fillArcMaxStepDegrees':2,'groups':[[{'id':q['id'],'kind':q['kind'],'layer':q['layer']}for q in g]for g in groups.values()]}
for label,xy in [('C_MCU1_1',(3200.8,1822.8)),('e255',(3317.55,1830.7))]:
 print(label,'fills',json.dumps([{'id':q['id'],'layer':q['layer'],'areaMil2':q['g'].area,'distanceMil':Point(xy).distance(q['g']),'nearestPoint':list(nearest_points(Point(xy),q['g'])[1].coords)[0]}for q in fills]))
print('groups',json.dumps([[q['id']for q in g if q['kind']!='LINE']for g in groups.values()]))
(P/'LOCAL_V3V3_GEOMETRY_SCREEN.json').write_text(json.dumps(out,indent=2),'utf8')
