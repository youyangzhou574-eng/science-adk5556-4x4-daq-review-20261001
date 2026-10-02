from pathlib import Path
P=Path(__file__).parent
v=(P/'warm_j2_audit.py').read_text('utf-8-sig')
v=v.replace("def filtered(s):return collections.Counter(json.dumps([h['type'],h.get('id'),q],sort_keys=True) for h,q in rec(s) if h.get('id') not in ids and q.get('parentId')not in ids)","""def filtered(s):
  out=[]
  for h,q in rec(s):
   if h.get('id') in ids or q.get('parentId') in ids:continue
   q=dict(q)
   if h['type']=='DOCHEAD':
    for key in ('client','updateTime','version'):q.pop(key,None)
   out.append(json.dumps([h['type'],h.get('id'),q],sort_keys=True))
  return collections.Counter(out)""")
v=v.replace("'otherSchematicSourceSame':sc", "'otherSchematicSourceSameExcluding3TransportHeaderFields':sc,'headerExclusions':['DOCHEAD.client','DOCHEAD.updateTime','DOCHEAD.version']")
(P/'warm_j2_audit_qualified.py').write_text(v,'utf8')
