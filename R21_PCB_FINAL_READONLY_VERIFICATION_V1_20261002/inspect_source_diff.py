from pathlib import Path
import json,collections
P=Path(__file__).parent
d=json.loads((P/'FROZEN_NATIVE_VS_WARM_OBJECT_DIFF.json').read_text('utf8'))
print('REMOVED LINES',json.dumps(d['LINE']['removed']))
for q in d['POURED']['changed']:
 print('POURED',q['id'])
 for k in q['before'].keys()|q['after'].keys():
  if q['before'].get(k)!=q['after'].get(k):
   x=q['before'].get(k);y=q['after'].get(k)
   print(k,repr(x)[:500],repr(y)[:500], 'lengths',len(str(x)),len(str(y)))
