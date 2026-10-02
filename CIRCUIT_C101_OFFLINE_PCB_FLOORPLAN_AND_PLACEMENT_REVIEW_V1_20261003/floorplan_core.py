from pathlib import Path
import json,math,datetime,itertools
from shapely.geometry import Polygon,box
from shapely.affinity import rotate,translate
from shapely.ops import unary_union
from shapely.strtree import STRtree
P=Path(__file__).parent
G=json.loads((P/'C101_PHYSICAL_GEOMETRY.json').read_text(encoding='utf-8'))
ID=json.loads((P/'C101_IDENTITY_AND_NETS.json').read_text(encoding='utf-8'))
def reserve(kind,count,why):
 f=P/'EXECUTION_BUDGET.json';b=json.loads(f.read_text(encoding='utf-8'));now=datetime.datetime.now(datetime.timezone.utc)
 assert not b['STOP'] and now<datetime.datetime.fromisoformat(b['deadlineUTC'])
 if b.get('coordinateSTOP'):assert kind=='image','Coordinates stopped; only already-approved closing images remain'
 assert b['spent'][kind]+count<=b['limits'][kind]
 b['spent'][kind]+=count;b['events'].append({'utc':now.isoformat(),'kind':kind,'count':count,'why':why});f.write_text(json.dumps(b,indent=2),encoding='utf-8')
def moved(shape,pos):
 x,y,a=pos;return translate(rotate(shape,a,origin=(0,0)),xoff=x,yoff=y)
LOCAL_BODY={r:unary_union([Polygon(poly)for poly in g['body']])for r,g in G.items()}
LOCAL_PHYS={}
for r,g in G.items():
 pads=[]
 for q in g['pads']:
  if q.get('polygon'):sh=Polygon(q['polygon'])
  else:sh=translate(rotate(box(-q['w']/2,-q['h']/2,q['w']/2,q['h']/2),q['angle'],origin=(0,0)),xoff=q['x'],yoff=q['y'])
  pads.append(sh)
 LOCAL_PHYS[r]=unary_union([LOCAL_BODY[r]]+pads)
def shape(r,pos):return moved(LOCAL_PHYS[r],pos)
def body(r,pos):return moved(LOCAL_BODY[r],pos)
def pad(r,n,pos):
 q=next(p for p in G[r]['pads']if p['number']==str(n));x,y,a=pos;c=math.cos(math.radians(a));s=math.sin(math.radians(a));return(x+q['x']*c-q['y']*s,y+q['x']*s+q['y']*c)
def net(r,n):return next(p['net']for p in G[r]['pads']if p['number']==str(n))
def dist(a,b):return math.hypot(a[0]-b[0],a[1]-b[1])
def actualpin(r,n):return next(p for p in G[r]['pads']if p['number']==str(n))
def legal(r,pos,placed,outline,exclusions,gap=.20,tree=None,existing=None):
 s=shape(r,pos)
 if not outline.buffer(-.35).covers(s) and r not in ['J1','J2','J3','J4']:return False
 if not outline.covers(s):return False
 for owner,keep in exclusions:
  if owner!=r and s.intersects(keep):return False
 if tree is not None:
  return all(s.distance(existing[i])>=gap-1e-9 for i in tree.query(s.buffer(gap)))
 return all(s.distance(shape(q,v))>=gap-1e-9 for q,v in placed.items())
def allpairs(placement):
 collisions=[];bodys=[];minimum=(float('inf'),None)
 ss={r:shape(r,v)for r,v in placement.items()};bb={r:body(r,v)for r,v in placement.items()}
 for a,b in itertools.combinations(sorted(placement),2):
  d=ss[a].distance(ss[b]);minimum=min(minimum,(d,[a,b]),key=lambda x:x[0])
  if ss[a].intersection(ss[b]).area>1e-9:collisions.append([a,b])
  if bb[a].intersection(bb[b]).area>1e-9:bodys.append([a,b])
 return {'pairs':len(placement)*(len(placement)-1)//2,'physicalProxyCollisions':collisions,'bodyCollisions':bodys,'minimumProxyGapMm':minimum[0],'minimumPair':minimum[1]}
