"""Independent loaded closed-loop double-injection matrix measurement."""
from science import ROOT,start,dump
from network_cases import fullbase,raw_nodes,seedlines
from make_mimo import PAIRS,plan
from coupled_bench import emit
reps,mapping,proof=plan('800',-1);tag='hybrid_blank_800';op=ROOT/'results'/'opwarm_800_blank'/'op.raw';nodes=raw_nodes(op)
dump(ROOT/'cases'/(tag+'_PLAN.json'),{'load':'800','state':-1,'representatives':reps,'mapping':mapping,'automorphismProof':proof,'OPsource':str(op),'stimuli':'first10 seriesvoltage W, next10 shuntcurrent J','DCtests':'allDCzero;originalfeedbackwires retained via0Vtest; originalmodels unchanged'})
for j in reps:
    lines=fullbase('800',-1);name=tag+'_p'+str(j);lines[0]=name;lines=[l.replace('DC 2.5 AC 1','DC 2.5 AC 0') for l in lines]
    for k,(fb,amp) in enumerate(PAIRS):
        for index,line in enumerate(lines):
            if line.split()[0]==amp:
                words=line.split();assert words[2]==fb;words[2]='e'+str(k);lines[index]=' '.join(words)
        lines += [f'VT{k} e{k} {fb} DC 0 AC {int(j==k)}',f'IT{k} 0 e{k} DC 0 AC {int(j==10+k)}']
    lines+=seedlines(op)+[f'.nodeset v(e{k})={nodes["v("+fb+")"]:.15g}' for k,(fb,amp) in enumerate(PAIRS)]
    lines+=['.save all','.control','set filetype=ascii','set wr_singlescale','set wr_vecnames','set numdgt=17','op','write op.raw all','ac dec 80 1 300meg']+[f'let ip{k}=-i(VT{k})' for k in range(10)]+['wrdata hybrid.txt '+' '.join([f'ip{k}' for k in range(10)]+[f'v(e{k})' for k in range(10)]),'quit','.endc','.end'];emit(name,lines);start(name,'P1','diagnostics',90)
