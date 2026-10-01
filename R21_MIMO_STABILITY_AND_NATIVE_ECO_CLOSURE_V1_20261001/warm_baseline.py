from science import ROOT,OLD,start
from coupled_bench import emit
from network_cases import fullbase
for load,state in [('800',-1),('800',0),('8000',0),('high_target',0)]:
    old='full_static_800_s0_permuted' if load=='800' and state==0 else 'full_static_800_s-1_fullseed' if state==-1 else 'full_static_'+load+'_s0'
    lines=(OLD/'cases'/(old+'.cir')).read_text().split('.control')[0].splitlines();lines=[l for l in lines if not l.startswith('.save')];name='opwarm_'+load+('_blank' if state==-1 else '')
    lines[0]=name;lines+=['.save all','.control','set filetype=ascii','set numdgt=15','optran 1 1 1 200n 100u 0','op','write op.raw all','wrdata op.txt v(vcm) v(vexc) v(vexcmd) v(row0) v(row1) v(row2) v(row3) v(ain0) v(ain1) v(ain2) v(ain3)','quit','.endc','.end'];emit(name,lines);start(name,'P0','diagnostics',60)
