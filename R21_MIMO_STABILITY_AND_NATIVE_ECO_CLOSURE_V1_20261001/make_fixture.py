from science import ROOT
from coupled_bench import emit
import sys
prefix=sys.argv[1] if len(sys.argv)>1 else 'fixture_y_'
for j in range(4):
    s=['Coupled analytic two-loop multiport fixture']
    for i in range(2):s += [f'RIN{i} e{i} 0 100k',f'ROUT{i} f{i} 0 1k',f'EG{i} z{i} 0 e{i} 0 100',f'RP{i} z{i} pole{i} 1k',f'CP{i} pole{i} 0 159.1549431n',f'GO{i} f{i} 0 pole{i} 0 1m']
    s+=['GX01 f0 0 pole1 0 .15m','GX10 f1 0 pole0 0 .05m','L0 e0 f0 1e9','L1 e1 f1 1e9']
    ports=['e0','e1','f0','f1']
    for k,node in enumerate(ports):s += [f'VP{k} src{k} 0 DC 0 AC {int(j==k)}',f'CPORT{k} src{k} {node} 1u']
    s+=['.control','set wr_singlescale','set wr_vecnames','set numdgt=15','op','ac dec 80 1 300meg']+[f'let ip{k}=-i(VP{k})' for k in range(4)]+['wrdata ac.txt '+' '.join([f'ip{k}' for k in range(4)]+[f'v({p})' for p in ports]),'quit','.endc','.end']
    emit(prefix+str(j),s)
if not (ROOT/'cases'/'pz_fixture_rc.cir').exists():emit('pz_fixture_rc',['Known passive transimpedance RC pole=-500 rad/s','RIN in 0 1k','R in out 1k','C out 0 1u','.control','set filetype=ascii','op','pz in 0 out 0 cur pz','print all > pz.txt','write pz.raw all','quit','.endc','.end'])
