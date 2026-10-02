import json,pathlib,collections
P=pathlib.Path(__file__).resolve().parent;v=json.loads((P/'FILLED_CAPTURE.json').read_text('utf8'))['parsed']['value'];rs=[]
for s in v['source'].splitlines():
 if '||'not in s:continue
 h,b=s.split('||',1)
 try:h=json.loads(h);b=json.loads(b.rstrip('|'))
 except ValueError:continue
 rs.append((h,b))
print('parts/pads/assigned/nets/NC',len(v['parts']),sum(len(c['pads'])for c in v['parts']),sum(bool(p['net'])for c in v['parts']for p in c['pads']),len(set(p['net']for c in v['parts']for p in c['pads']if p['net'])),sum(not p['net']for c in v['parts']for p in c['pads']))
print('types',dict(collections.Counter(h['type']for h,b in rs)))
for kind in('VIA','POUR','POURED'):
 r=[(h,b)for h,b in rs if h['type']==kind];print(kind,'examples',str(r[:2])[:2000])
v=json.loads((P/'FILLED_DRC.json').read_text('utf8'))['parsed']['value'];leaf=[]
def walk(q):
 if isinstance(q,dict):
  if 'errorType'in q and 'globalIndex'in q:leaf.append(q)
  else:
   for x in q.values():walk(x)
 elif isinstance(q,list):
  for x in q:walk(x)
walk(v)
print('violations',[(q['errorObjType'],q['obj1'],q.get('obj2'),q['explanation']['param'].get('minDistance'))for q in leaf if q['errorType']!='Connection Error'])
print('remainingPads',[(q['net'],q['obj1']['suffix'])for q in leaf if q['errorType']=='Connection Error'and q['net']!='V3V3'])
