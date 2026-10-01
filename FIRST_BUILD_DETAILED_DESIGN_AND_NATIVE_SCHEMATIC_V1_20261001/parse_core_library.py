import json,pathlib,collections
p=pathlib.Path(__file__).resolve().parent
source=next((p/'core_library').glob('*.elibu')).read_text(encoding='utf-8')
docs={};current=None
lines=source.splitlines()
for lineno,line in enumerate(lines):
 if not line.strip():continue
 assert '||' in line
 if line.endswith('|'):line=line[:-1]
 else:assert lineno==len(lines)-1,'missing terminator before EOF'
 h,b=line.split('||',1);h=json.loads(h);b=json.loads(b)
 if h['type']=='DOCHEAD':
  current=b['uuid'];docs.setdefault(current,{'head':b,'records':[]});continue
 assert current is not None
 docs[current]['records'].append({'head':h,'body':b})
core=json.loads((p/'CORE_DEVICES_SELECTED.json').read_text(encoding='utf-8'))
result={}
for name,dev in core.items():
 assert dev is not None,'missing exact core '+name
 sym=docs[dev['symbolUuid']];foot=docs[dev['footprintUuid']]
 pins=[];attrs=collections.defaultdict(dict)
 for r in sym['records']:
  if r['head']['type']=='ATTR':attrs[r['body'].get('parentId')][r['body']['key']]=r['body']['value']
 for r in sym['records']:
  if r['head']['type']=='PIN':
   a=attrs[r['head']['id']];pins.append({'local_id':r['head']['id'],'number':str(a['Pin Number']),'name':a.get('Pin Name'),'part':r['body']['partId'],'x':r['body']['x'],'y':r['body']['y'],'rotation':r['body']['rotation']})
 pads=[r for r in foot['records'] if r['head']['type']=='PAD']
 result[name]={'device':{k:dev.get(k) for k in ['uuid','name','manufacturerId','supplierId','symbolUuid','footprintUuid','footprintName']},'pins':pins,'pad_records':pads,'footprint_doc_head':foot['head']}
(p/'CORE_LIBRARY_PIN_PAD_RAW.json').write_bytes((json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps({name:{'pins':[(i['number'],i['name'],i['part']) for i in d['pins']],'first_pad':d['pad_records'][:1],'pad_count':len(d['pad_records'])}for name,d in result.items()},ensure_ascii=True))
