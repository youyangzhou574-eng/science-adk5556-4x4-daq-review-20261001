"""Full-network nodeset continuation and loaded multiport benches."""
import re,json
from pathlib import Path
from science import ROOT
OLD=ROOT.parent/'R21_COUPLED_ROOTCAUSE_AND_R21_NATIVE_ECO_V1'
from coupled_bench import emit
def raw_nodes(p):
    text=Path(p).read_text();assert 'Plotname: Operating Point' in text and 'Flags: real' in text
    defs=[line.split()[1:] for line in text.split('Variables:\n')[1].split('Values:\n')[0].splitlines() if line.strip()];vs=text.split('Values:\n')[1].splitlines();values=[float(vs[0].split()[1])]+[float(l) for l in vs[1:] if l.strip()]
    assert len(defs)==len(values)
    return {n[0]:v for n,v in zip(defs,values) if n[1]=='voltage'}
def seedlines(p,rename=None):
    a=raw_nodes(p)
    return ['.nodeset '+(rename(n) if rename else n)+'='+format(v,'.15g') for n,v in a.items()]
def fullbase(load='800',state=0):
    name='full_static_800_s0_permuted' if load=='800' and state==0 else 'full_static_800_s-1_fullseed' if load=='800' and state==-1 else 'full_static_'+load+'_s0'
    text=(OLD/'cases'/(name+'.cir')).read_text();lines=text.split('.control')[0].splitlines();lines[0]='Corrected frozen full-network '+load+' state '+str(state)
    return [line for line in lines if not line.startswith('.save') and not line.startswith('.nodeset')]
def op(name,load='800',state=0,vdd=5,prior=None):
    lines=fullbase(load,state);lines=[re.sub(r'^V5 v5 0 .*$',f'V5 v5 0 {vdd}',l) for l in lines]
    path=prior if prior else OLD/'results'/'full_static_800_s0_permuted'/'op.raw'
    lines+=seedlines(path)+['.save all','.control','set filetype=ascii','set numdgt=15','op','write op.raw all','wrdata op.txt v(vcm) v(vexc) v(vexcmd) v(row0) v(row1) v(row2) v(row3) v(ain0) v(ain1) v(ain2) v(ain3)','quit','.endc','.end'];emit(name,lines)
    (ROOT/'cases'/(name+'.json')).write_text(json.dumps({'analysis':'DC','load':load,'state':state,'vdd':vdd,'nodesetSource':str(path),'noForcedIC':True},indent=2))
if __name__=='__main__':
    for load,state in [('800',-1),('800',0),('8000',0),('high_target',0)]:op('op5_'+load+('_blank' if state==-1 else ''),load,state)
