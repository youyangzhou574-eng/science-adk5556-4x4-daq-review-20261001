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
def make(tag,load,state,vdd=5,opname=None):
    basename=opname or ('opwarm_'+load+('_blank' if state==-1 else ''));op=ROOT/'results'/basename/'op.raw'
    nodes=raw_nodes(op);assert abs(nodes['v(vcm)']-2.5)<.01 and abs(nodes['v(vexc)']-2.25)<.01
    reps,mapping,proof=plan(load,state)
    dump(ROOT/'cases'/(tag+'_PLAN.json'),{'load':load,'state':state,'vdd':vdd,'representatives':reps,'mapping':mapping,'automorphismProof':proof,'OPsource':str(op),'method':'loaded20port admittance; graph-exact symmetric columns; actual duplicate later checked'})
    for j in reps:
        name=tag+'_p'+str(j);lines=fullbase(load,state);lines=[re.sub(r'^V5 v5 0 .*$',f'V5 v5 0 {vdd}',l).replace('DC 2.5 AC 1','DC 2.5 AC 0') for l in lines];lines[0]=name
        for k,(fb,amp) in enumerate(PAIRS):
            for index,line in enumerate(lines):
                if line.split()[0]==amp:
                    words=line.split();assert words[2]==fb;words[2]='e'+str(k);lines[index]=' '.join(words)
            lines += [f'LDC{k} e{k} {fb} 1e9']
        def rename(n):return n
        lines+=seedlines(op)
        for k,(fb,amp) in enumerate(PAIRS):lines.append(f'.nodeset v(e{k})={nodes["v("+fb+")"]:.15g}')
        ports=['e'+str(k) for k in range(10)]+[fb for fb,amp in PAIRS]
        for k,node in enumerate(ports):lines += [f'VP{k} src{k} 0 DC 0 AC {int(j==k)}',f'CPORT{k} src{k} {node} 1u']
        lines+=['.save all','.control','set filetype=ascii','set wr_singlescale','set wr_vecnames','set numdgt=15','op','write op.raw all','ac dec 80 1 300meg']+[f'let ip{k}=-i(VP{k})' for k in range(20)]+['wrdata ac.txt '+' '.join([f'ip{k}' for k in range(20)]+[f'v({p})' for p in ports]),'quit','.endc','.end'];emit(name,lines);start(name,'P1','DC_AC_PZ',90)
if __name__=='__main__':
    import sys
    make(sys.argv[1],sys.argv[2],int(sys.argv[3]),float(sys.argv[4]) if len(sys.argv)>4 else 5,sys.argv[5] if len(sys.argv)>5 else None)
