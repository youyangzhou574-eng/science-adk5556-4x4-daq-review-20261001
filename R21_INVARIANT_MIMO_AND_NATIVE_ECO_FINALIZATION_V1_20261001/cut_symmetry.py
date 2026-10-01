import json,re,collections
from science import ROOT,OLD,start,dump
from network_cases import fullbase,seedlines,raw_nodes
from coupled_bench import emit
PAIRS=[('cmfb','XCM'),('exfb','XEX')]+[(f'fb{i}',f'XR{i}') for i in range(4)]+[(f'minus{i}',f'XT{i}') for i in range(4)]
def portperm(group,a,b):
    p=list(range(20));offset=2 if group=='row' else 6
    x,y=offset+a,offset+b;p[x],p[y]=p[y],p[x];p[x+10],p[y+10]=p[y+10],p[x+10];return p
def mapnode(node,group,a,b):
    # Circuit graph uses indexed physical nets; node aliases never alter values.
    prefixes=['sel','ns','cmd','fb','drv','row'] if group=='row' else ['col','minus','tdrv','tap','ain']
    for prefix in prefixes:
        node=re.sub(r'(?<![A-Za-z0-9_])'+prefix+r'('+str(a)+'|'+str(b)+r')(?![A-Za-z0-9_])',lambda m:prefix+str(b if int(m[1])==a else a),node)
    return node
def graph(lines,group=None,a=0,b=0):
    records=[]
    for line in lines[1:]:
        x=line.split()
        if not x or x[0].startswith('.'):continue
        # Element instance names are labels; preserve element type, ordered terminals and parameters.
        records.append(tuple([x[0][0].lower()]+[mapnode(v,group,a,b) if group else v for v in x[1:]]))
    return collections.Counter(records)
def plan(load,state):
    groups=[('row',list(range(4)) if state==-1 else [1,2,3]),('tia',list(range(4)) if load!='high_target' else [1,2,3])]
    representatives=list(range(10));mapping={i:{'representative':i,'permutation':list(range(20))} for i in range(20)}
    lines=fullbase(load,state);proof=[]
    for group,indices in groups:
        rep=indices[0];offset=2 if group=='row' else 6
        for target in indices[1:]:
            assert graph(lines)==graph(lines,group,rep,target),(load,state,group,rep,target,'not graph automorphism')
            representatives.remove(offset+target)
            for half in [0,10]:mapping[half+offset+target]={'representative':half+offset+rep,'permutation':portperm(group,rep,target)}
            proof.append({'group':group,'swap':[rep,target],'graphAutomorphism':True})
    reps=representatives+[i+10 for i in representatives]
    return reps,mapping,proof
