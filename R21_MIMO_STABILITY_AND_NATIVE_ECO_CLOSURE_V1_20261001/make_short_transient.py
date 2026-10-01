from science import ROOT,start
from coupled_bench import make,emit
from network_cases import seedlines,raw_nodes
import json
def generate(rows,cols,load):
    label=f'r{rows}t{cols}_{load}';base='pre_'+label
    make(base,rows,cols,load,-1,5,'static','trap')
    # Correct generator high-target geometry must retain high target ROW0/COL0,
    # even though every row command is blank before switching.
    p=ROOT/'cases'/(base+'.cir');lines=p.read_text().split('.control')[0].splitlines();lines=[l for l in lines if not l.startswith('.save') and not l.startswith('.nodeset')]
    if load=='high_target':
        for index,line in enumerate(lines):
            if line.startswith('RA'):
                words=line.split();words[-1]='8000' if words[0]=='RA0_0' else '800';lines[index]=' '.join(words)
    nodes=raw_nodes(ROOT/'results'/'op5_800_blank'/'op.raw');prefixes=['v(xcm.','v(xex.']+[f'v(xr{i}.' for i in range(rows)]+[f'v(xt{i}.' for i in range(cols)]
    outer={w.lower() for line in lines for w in line.split()[1:]}
    lines += ['.nodeset '+n+'='+format(v,'.15g') for n,v in nodes.items() if n[2:-1] in outer or any(n.startswith(q) for q in prefixes)]
    lines += ['.save all','.control','set filetype=ascii','set numdgt=15','op','write op.raw all','quit','.endc','.end'];emit(base,lines);start(base,'P1','DC_AC_PZ',60)
def run(rows,cols,load):
    label=f'r{rows}t{cols}_{load}';base='pre_'+label;op=ROOT/'results'/base/'op.raw';nodes=raw_nodes(op)
    assert abs(nodes['v(vcm)']-2.5)<.01 and abs(nodes['v(vexc)']-2.25)<.01
    assert all(abs(nodes[f'v(row{i})']-2.5)<.01 for i in range(4))
    assert all(abs(nodes[f'v(ain{i})']-2.5)<.01 for i in range(cols))
    lines=(ROOT/'cases'/(base+'.cir')).read_text().split('.control')[0].splitlines();lines=[l for l in lines if not l.startswith('.nodeset') and not l.startswith('.save') and not l.startswith('.options')]
    lines=[l.replace('VSEL0 sel0 0 0','VSEL0 sel0 0 PULSE(0 1 3u 10n 10n 1m 10m)') for l in lines]
    saved=['v(vcm)','v(vexc)']+[f'v(row{i})' for i in range(4)]+[f'v(ain{i})' for i in range(cols)]+[f'v(drv{i})' for i in range(rows)]+[f'v(tdrv{i})' for i in range(cols)]
    name='short_'+label+'_gear';lines[0]=name;lines+=seedlines(op)+['.save all','.options method=gear','.control','set filetype=ascii','set wr_singlescale','set wr_vecnames','set numdgt=15','op','write pre_switch_op.raw all','tran 200n 353u 0 100n','wrdata trace.txt '+' '.join(saved),'quit','.endc','.end'];emit(name,lines)
    (ROOT/'cases'/(name+'.json')).write_text(json.dumps({'rowsMacro':rows,'colsMacro':cols,'load':load,'vdd':5,'switchTime_us':3,'endTime_us':353,'riseFall_ns':10,'saved':saved,'plannedValidEdgeOffsetsAfterSwitch_us':[325,350],'lateReference_us':[333,353],'scope':'two planned edge times in a short window, not32sample activity or fullframe; ideal reduced boundaries stated','noForcedIC':True,'noOptranWithSwitchPulse':True,'preSwitchOP':str(op)},indent=2))
    start(name,'P1','transient',180)
if __name__=='__main__':
    import sys
    (generate if sys.argv[1]=='pre' else run)(int(sys.argv[2]),int(sys.argv[3]),sys.argv[4])
