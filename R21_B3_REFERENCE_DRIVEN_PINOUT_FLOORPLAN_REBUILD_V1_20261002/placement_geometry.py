from pathlib import Path
import json, math
from shapely.geometry import Polygon,box,Point
from shapely.affinity import rotate,translate
from shapely.ops import unary_union
P=Path(__file__).parent
G=json.loads((P/'ACTUAL_GEOMETRY.json').read_text(encoding='utf8'))
C=json.loads((P/'CONSTRAINT_BLOCKS.json').read_text(encoding='utf8'))
membership=C['membership'];classes=C['classes'];regions=C['regions']
groups={}
for ref,n in membership.items():groups.setdefault(n,[]).append(ref)
def body(r,pos=None):
    g=G[r];x,y,a=pos or(g['xMm'],g['yMm'],g['rotation'])
    return translate(rotate(unary_union([Polygon(p)for p in g['bodyLocalPolygonsMm']]),a,origin=(0,0)),xoff=x,yoff=y)
def padshape(p):
    sh=p['shape'];x,y=p['xMm'],p['yMm']
    if sh[0]=='POLYGON':
        v=[v for v in sh[1]if isinstance(v,(int,float))]
        return Polygon([(v[i]*.0254,v[i+1]*.0254)for i in range(0,len(v),2)])
    w,h=sh[1]*.0254,sh[2]*.0254
    # Conservative rectangular bound for rounded pads, clearly a proxy.
    return translate(rotate(box(-w/2,-h/2,w/2,h/2),p['rotation'],origin=(0,0)),xoff=x,yoff=y)
original={r:unary_union([body(r)]+[padshape(p)for p in G[r]['pads']])for r in G}
def physical(r,pos):
    g=G[r];x,y,a=pos
    return translate(rotate(translate(original[r],xoff=-g['xMm'],yoff=-g['yMm']),a-g['rotation'],origin=(0,0)),xoff=x,yoff=y)
def newpad(r,p,pos):
    g=G[r];x,y,a=pos;t=math.radians(a-g['rotation']);u,v=p['xMm']-g['xMm'],p['yMm']-g['yMm']
    return x+u*math.cos(t)-v*math.sin(t),y+u*math.sin(t)+v*math.cos(t)
def reserve(kind,reason):
    import datetime
    p=P/'EXECUTION_BUDGET.json';b=json.loads(p.read_text());now=datetime.datetime.now(datetime.timezone.utc)
    assert b['status']=='ACTIVE' and now<datetime.datetime.fromisoformat(b['deadlineUTC'].replace('Z','+00:00'))
    count=b['actual'].get(kind,0)+1;assert count<=b['limits'][kind]
    b['actual'][kind]=count;b['reservations'].append({'UTC':now.isoformat(),'kind':kind,'count':1,'reason':reason});p.write_text(json.dumps(b,indent=2),encoding='utf8');return count
