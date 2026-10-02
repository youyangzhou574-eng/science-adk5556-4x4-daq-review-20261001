from pathlib import Path
import json,math
from shapely.geometry import Polygon,box,Point
from shapely.affinity import rotate,translate
from shapely.ops import unary_union
P=Path(__file__).parent
G=json.loads((P/'ACTUAL_GEOMETRY.json').read_text(encoding='utf8'))
legacy=json.loads((P.parent/'R21_PCB_FUNCTIONAL_COMPACTION_AND_LAYOUT_REORGANIZATION_V1/PRE_USER_SCIENCE_ALIGNMENT_DRAFT/CANDIDATE_B_PLAN.json').read_text(encoding='utf8'))
legacy_membership=legacy['membership']
def body(ref,position=None):
    g=G[ref];x,y,angle=position or(g['xMm'],g['yMm'],g['rotation'])
    return translate(rotate(unary_union([Polygon(p)for p in g['bodyLocalPolygonsMm']]),angle,origin=(0,0)),xoff=x,yoff=y)
def pad_shape(p):
    sh=p['shape'];x,y=p['xMm'],p['yMm']
    if sh[0]=='POLYGON':
        v=[v for v in sh[1] if isinstance(v,(int,float))]
        return Polygon([(v[i]*.0254,v[i+1]*.0254)for i in range(0,len(v),2)])
    w,h=sh[1]*.0254,sh[2]*.0254
    q=box(-w/2,-h/2,w/2,h/2)
    # Conservative rectangular pad bound for OVAL/ELLIPSE; body collision
    # separately uses native exact body polygons, not this pad proxy.
    return translate(rotate(q,p['rotation'],origin=(0,0)),xoff=x,yoff=y)
def geometry(ref):return unary_union([body(ref)]+[pad_shape(p)for p in G[ref]['pads']])
def physical(ref,position):
    g=G[ref];x,y,a=position
    return translate(rotate(translate(geometry(ref),xoff=-g['xMm'],yoff=-g['yMm']),a-g['rotation'],origin=(0,0)),xoff=x,yoff=y)

groups={};classes={};membership={}
def group(name,refs,classification):
    assert all(r not in membership for r in refs)
    groups[name]=refs
    for r in refs:membership[r]=name;classes[r]=classification
for name,old in [('TIA','TIA'),('ROW','ROW'),('REFERENCE','REFERENCE'),('ADC','ADC')]:
    group(name,[r for r in G if legacy_membership[r]==old],'A')
group('MCU',['U7','C_MCU1'],'A')
group('POWER5',['U9','U9_IN_CAP','U9_OUT_CAP'],'A')
group('POWER3',['U10','U10_IN_CAP','U10_OUT_CAP'],'A')
group('LDO',['U8','C_LDO_IN','C_LDO_OUT'],'A')
group('MUX',['U4','C_MUX'],'B')
for u in ('U13','U14','U15'):group(u,[u,'C_'+u],'B')
for u in ('U11','U12'):group(u,[u,u+'_VDD_C',u+'_SENSE_C',u+'_CT_C'],'B')
for j in ('J1','J2','J3','J4'):group(j,[j],'A'if j=='J2'else'C')
free=[r for r in G if r not in membership]
for r in free:group(r,[r],'C')
assert len(membership)==176
def region(ref):
    old=legacy_membership[ref]
    if old in('FFC','TIA','ROW'):return'AFE'
    if old in('REFERENCE','MUX'):return'BIAS'
    if old in('ADC','ADC_RESET_PULLDOWN'):return'ADC'
    if old in('MCU','DIGITAL','RESET','ENABLE_GATES'):return'DIGITAL'
    if old in('POWER_5V','POWER_3V3','LDO','POWER_ENTRY','POWER_BULK'):return'POWER'
    if old in('DEBUG','UART','SUPERVISOR_A','SUPERVISOR_B'):return'EXTERNAL'
    raise ValueError(ref)
def groupbounds(name):return unary_union([geometry(r)for r in groups[name]]).bounds
if __name__=='__main__':
    out={n:{'count':len(rs),'region':region(rs[0]),'class':classes[rs[0]],'bbox':groupbounds(n),'width':groupbounds(n)[2]-groupbounds(n)[0],'height':groupbounds(n)[3]-groupbounds(n)[1]}for n,rs in groups.items()if len(rs)>1 or n.startswith('J')}
    (P/'CONSTRAINT_BLOCKS.json').write_text(json.dumps({'blocks':out,'free':free,'membership':membership,'classes':classes,'regions':{r:region(r)for r in G}},indent=2),encoding='utf8')
    print(json.dumps({'blocks':out,'free':free},ensure_ascii=True))
