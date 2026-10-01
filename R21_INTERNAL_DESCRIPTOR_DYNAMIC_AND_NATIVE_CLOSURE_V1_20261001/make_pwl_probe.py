from pathlib import Path
from processed import parse
from rawio import op_values
import json
r=Path(__file__).resolve().parent;op=op_values(r/'results/follower_exact/op.raw');es=parse((r/'results/follower_listing/stdout.log').read_text(errors='replace'))
rows=[]
for k,e in enumerate(e for e in es if e.kind=='a'and e.model['type']=='pwl'):
 name='pwl_actual_op_'+str(k);value=op.get(e.nodes[2],0)-op.get(e.nodes[3],0);model=e.original.split()[-1]
 card=next(x.strip().split(': ',1)[1]for x in (r/'results/follower_listing/stdout.log').read_text(errors='replace').splitlines()if '.model '+model+' 'in x).replace(model,'probe')
 lines=['actual PSA PWL at frozen follower OP','Vin in 0 DC %.17g AC 1'%value,'a1 %v in %v out probe','Rload out 0 1meg',card,'.control','set filetype=ascii','set numdgt=15','set wr_vecnames','set wr_singlescale','op','write op.raw all']
 for j,hz in enumerate([1,1e8,3e8]):lines+=['ac lin 1 %.17g %.17g'%(hz,hz),'wrdata ac_%d.txt v(out) i(Vin)'%j]
 lines+=['quit','.endc','.end'];(r/'cases'/ (name+'.cir')).write_text('\n'.join(lines)+'\n');rows.append({'name':name,'sourceElement':e.name,'sourceLine':e.line,'actualControlOP':value,'model':e.model})
(r/'PWL_PROBE_SOURCE_MAP.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows))
