from pathlib import Path
import json,collections
P=Path(__file__).parent
exec((P/'cold_j2_audit.py').read_text('utf-8-sig').split("pa={x['ref']")[0])
def diff(x,y):
 a={(h['type'],h.get('id')):(h,q)for h,q in rec(x)};b={(h['type'],h.get('id')):(h,q)for h,q in rec(y)};d=[]
 for k in a.keys()|b.keys():
  if k not in a or k not in b:d.append({'key':k,'before':a.get(k),'after':b.get(k)})
  else:
   u,v=a[k][1],b[k][1];ds={f:[u.get(f),v.get(f)]for f in u.keys()|v.keys()if u.get(f)!=v.get(f)}
   if ds:d.append({'key':k,'diff':ds})
 return d
r={'pcb':diff(W['pcb']['source'],C['pcb']['source']),'sch':{x['page']['name']:diff(x['source'],y['source'])for x,y in zip(W['schematic']['pages'],C['schematic']['pages'])}}
(P/'WARM_COLD_SOURCE_DIFF_RAW.json').write_text(json.dumps(r,indent=2),'utf8');print(json.dumps(r)[:18000]);print('NETLISTTYPES',type(W['pcb']['netlist']).__name__,type(C['pcb']['netlist']).__name__);print(str(W['pcb']['netlist'])[:1300]);print(str(C['pcb']['netlist'])[:1300])
