import pathlib,json,math,collections
from shapely.geometry import Polygon,LineString,Point,box
from shapely.affinity import rotate,translate
P=pathlib.Path(__file__).resolve().parent
v=json.loads((P/'FILLED_CAPTURE.json').read_text('utf8'))['parsed']['value'];pads=[];traces=[];vias=[];records=[]
for c in v['parts']:
 for p in c['pads']:
  s=p['pad'];x,y=p['x'],p['y']
  if s[0]=='POLYGON':
   co=[q for q in s[1]if isinstance(q,(int,float))];g=Polygon(list(zip(co[::2],co[1::2])))
  else:g=translate(rotate(box(-s[1]/2,-s[2]/2,s[1]/2,s[2]/2),p['rotation'],origin=(0,0)),x,y)
  pads.append(dict(p,ref=c['ref'],key=c['ref']+'-'+p['number'],geometry=g))
for ln in v['source'].splitlines():
 if '||'not in ln:continue
 h,b=ln.split('||',1)
 try:h=json.loads(h);b=json.loads(b.rstrip('|'))
 except ValueError:continue
 records.append((h,b))
 if h['type']=='LINE':
  pts=[(b['startX'],b['startY']),(b['endX'],b['endY'])];traces.append({'id':h['id'],'net':b['netName'],'layer':b['layerId'],'width':b['width'],'points':pts,'geometry':LineString(pts).buffer(b['width']/2,cap_style=1)})
 if h['type']=='VIA':vias.append({'id':h['id'],'net':b['netName'],'x':b['centerX'],'y':b['centerY'],'hole':b['holeDiameter'],'diameter':b['viaDiameter'],'geometry':Point(b['centerX'],b['centerY']).buffer(b['viaDiameter']/2)})
byNet=collections.defaultdict(list)
viaDiameter=24
for p in pads:
 if p['net']:byNet[p['net']].append(p)
exec((P/'prepare_p0.py').read_text('utf8').split('def candidates(a,b):',1)[1].split("# Explicit sensitive local work",1)[0].join(['def candidates(a,b):','']))
exec((P/'prepare_p1.py').read_text('utf8').split('def allgroups(net):',1)[1].split('# Engineer-defined signal',1)[0].join(['def allgroups(net):','']))
exec((P/'prepare_p0_transitions.py').read_text('utf8').split('def clear(pts,net,layer,w=6):',1)[1].split('def recordPath',1)[0].join(['def clear(pts,net,layer,w=6):','']))
exec((P/'prepare_dogleg_escapes.py').read_text('utf8').split('def dogEsc(p):',1)[1].split("selected=['DIV_SEG8'",1)[0].join(['def dogEsc(p):','']))
p1paths=[];p1vias=[]
