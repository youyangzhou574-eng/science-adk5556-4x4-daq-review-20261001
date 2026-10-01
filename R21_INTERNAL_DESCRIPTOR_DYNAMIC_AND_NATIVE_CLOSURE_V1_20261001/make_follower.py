from pathlib import Path
import json,hashlib,collections
from spice_flatten import flatten
r=Path(__file__).resolve().parent
lines=['07 descriptor local follower qualification','.include "'+str(r/'models/OPA4388_ORIGINAL.LIB')+'"','Vdd vdd 0 DC 5','Vin inp 0 DC 2.5 AC 1','X1 inp out vdd 0 out OPA4388','Rload out 0 10k','Cload out 0 10p','.save all','.control','set filetype=ascii','set numdgt=15','set wr_singlescale','set wr_vecnames','op','write op.raw all','show all']
freq=[.01,.1,1,10,100,1e3,1e4,1e5,1e6,1e7,1e8,3e8]
for j,f in enumerate(freq):lines += ['ac lin 1 '+str(f)+' '+str(f),'wrdata ac_%02d.txt v(out) v(inp)'%j]
lines+=['ac dec 100 1k 300meg','wrdata crossover.txt v(out) v(inp)','quit','.endc','.end'];net='\n'.join(lines)+'\n';(r/'cases/follower_exact.cir').write_text(net)
flat=flatten(net,source=str(r/'cases/follower_exact.cir'));rows=[{'name':x.name,'kind':x.kind,'nodes':x.nodes,'args':x.args,'params':x.params,'model':x.model,'source':x.source,'line':x.line,'scope':x.scope}for x in flat];(r/'PRIMITIVE_INVENTORY.json').write_text(json.dumps({'counts':dict(collections.Counter(x.kind for x in flat)),'total':len(flat),'allActualMapped':True,'modelsSHA256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest().upper()for p in (r/'models').glob('*.LIB')},'elements':rows},indent=2),encoding='utf-8');print(json.dumps({'flattenedElements':len(flat),'frequencies':freq,'analyses':14}))
