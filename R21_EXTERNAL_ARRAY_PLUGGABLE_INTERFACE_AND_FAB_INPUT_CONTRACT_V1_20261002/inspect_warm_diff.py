exec(open(__file__.replace('inspect_warm_diff.py','warm_j2_audit.py'),encoding='utf-8-sig').read().split("r.pop('J2pins')")[0])
for x,y in zip(A['schematic']['pages'],B['schematic']['pages']):
 z={h.get('id'):(h,q) for h,q in rec(x['source'])};w={h.get('id'):(h,q) for h,q in rec(y['source'])};ds=[]
 for k in z.keys()|w.keys():
  if z.get(k)!=w.get(k):
   if k not in w or k not in z:ds.append({'id':k,'removed':z.get(k),'added':w.get(k)})
   else:
    u,v=z[k][1],w[k][1];d={f:[u.get(f),v.get(f)]for f in u.keys()|v.keys()if u.get(f)!=v.get(f)}
    if d:ds.append({'id':k,'type':z[k][0]['type'],'diff':d})
 print(x['page']['name'],json.dumps(ds,ensure_ascii=False)[:14000])
