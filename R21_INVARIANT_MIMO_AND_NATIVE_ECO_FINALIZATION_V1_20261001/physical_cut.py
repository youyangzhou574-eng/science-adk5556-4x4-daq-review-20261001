from pathlib import Path
import json
from science import ROOT,dump,start
from network_cases import fullbase,seedlines,raw_nodes
from cut_symmetry import PAIRS,plan
from coupled_bench import emit
OLD=ROOT.parent/'R21_MIMO_STABILITY_AND_NATIVE_ECO_CLOSURE_V1';OP=OLD/'results/opwarm_800_blank/op.raw'

def build():
 nodes=raw_nodes(OP);reps,mapping,proof=plan('800',-1);cases=[]
 for topology in ['open','closed','tian']:
  indices=(reps+[3,7,13,17]) if topology=='closed' else reps if topology=='open' else [0,10,1,11,2,12,6,16]
  for j in indices:
   name=f'{topology}_blank_p{j}';lines=[l.replace('DC 2.5 AC 1','DC 2.5 AC 0') for l in fullbase('800',-1)];lines[0]=name
   active=list(range(10)) if topology!='tian' else [j%10]
   for k in active:
    fb,amp=PAIRS[k]
    for idx,line in enumerate(lines):
     if line.split()[0]==amp:
      x=line.split();assert x[2]==fb;x[2]='e'+str(k);lines[idx]=' '.join(x)
    if topology=='open':lines.append(f'LDC{k} e{k} {fb} 1e9')
    else:lines.extend([f'VT{k} e{k} {fb} DC 0 AC {int(j==k)}',f'IT{k} 0 e{k} DC 0 AC {int(j==10+k)}'])
   lines+=seedlines(OP)+[f'.nodeset v(e{k})={nodes["v("+PAIRS[k][0]+")"]:.17g}' for k in active]
   if topology=='open':
    ports=['e'+str(k) for k in range(10)]+[fb for fb,amp in PAIRS]
    for k,node in enumerate(ports):lines.extend([f'VP{k} src{k} 0 DC 0 AC {int(j==k)}',f'CPORT{k} src{k} {node} 1u'])
    outputs=[f'ip{k}'for k in range(20)]+[f'v({n})'for n in ports];lets=[f'let ip{k}=-i(VP{k})'for k in range(20)]
   else:outputs=[f'ip{k}'for k in active]+[f'v(e{k})'for k in active];lets=[f'let ip{k}=-i(VT{k})'for k in active]
   lines+=['.save all','.control','set filetype=ascii','set wr_singlescale','set wr_vecnames','set numdgt=17','op','write op.raw all','ac dec 80 .01 300meg']+lets+['wrdata data.txt '+' '.join(outputs),'quit','.endc','.end']
   emit(name,lines);cases.append({'name':name,'topology':topology,'stimulus':j,'activeCuts':active,'purpose':'PRIMARY_PORT_CUT_AND_LOW_FREQUENCY_QUALIFICATION','diagnosticAttribute':False,'fixedScale':'Sv=I/Si=I'})
 dump(ROOT/'PHYSICAL_MEASUREMENT_PLAN.json',{'cases':cases,'representatives':reps,'mapping':mapping,'symmetryProof':proof,'OPsource':str(OP),'fixedPhysicalCut':'all external feedback stays f; only macro minus input terminal moved to e; 1k outputISO not cut','analysisChargesPerCase':2,'actualWaveform':False,'diagnosticClassification':'Primary mandatory AC qualification, not numerical solver diagnostic variation; all 56 analysis directives charged; offline numerical replay separately diagnostic2/24'})
 print(json.dumps({'plannedCases':len(cases),'plannedAnalyses':2*len(cases)}))

def dispatch(count=2):
 planfile=ROOT/'EXTENDED_MEASUREMENT_PLAN.json';p=json.loads((planfile if planfile.exists() else ROOT/'PHYSICAL_MEASUREMENT_PLAN.json').read_text());b=json.loads((ROOT/'EXECUTION_BUDGET.json').read_text());done={c['name']for c in b['cases']}
 running=[]
 for c in b['cases']:
  status=ROOT/'results'/c['name']/'STATUS.json'
  if not status.exists() or json.loads(status.read_text()).get('status')=='RUNNING':running.append(c['name'])
 assert not running,('Wait for own current cases before dispatch',running)
 todo=[c for c in p['cases']if c['name']not in done][:count]
 for c in todo:start(c['name'],'P0','DC_AC_PZ',90)
 print(json.dumps({'remaining':len(p['cases'])-len(done)-len(todo)}))
if __name__=='__main__':
 import sys
 if sys.argv[1]=='build':build()
 elif sys.argv[1]=='dispatch':dispatch(int(sys.argv[2])if len(sys.argv)>2 else 2)
