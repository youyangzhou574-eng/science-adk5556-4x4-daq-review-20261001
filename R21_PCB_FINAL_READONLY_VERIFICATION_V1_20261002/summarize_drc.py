import json,pathlib,collections,sys
P=pathlib.Path(__file__).resolve().parent;label=sys.argv[1]
v=json.loads((P/(label+'.json')).read_text('utf8'))['parsed'];assert v['ok']
leaves=[]
def walk(x):
 if isinstance(x,dict):
  if 'errorType'in x and 'globalIndex'in x:leaves.append(x)
  else:
   for y in x.values():walk(y)
 elif isinstance(x,list):
  for y in x:walk(y)
walk(v['value'])
out={'count':len(leaves),'categories':dict(collections.Counter(x['errorType']for x in leaves)),'unconnectedNetCounts':dict(collections.Counter(x.get('net')for x in leaves if x['errorType']=='Connection Error')),'otherViolations':[x for x in leaves if x['errorType']!='Connection Error']}
(P/(label+'_CLASSIFIED.json')).write_text(json.dumps(out,indent=2,ensure_ascii=False),'utf8')
print(json.dumps({k:v for k,v in out.items()if k!='otherViolations'}));print(json.dumps(out['otherViolations'][:5],ensure_ascii=True))
