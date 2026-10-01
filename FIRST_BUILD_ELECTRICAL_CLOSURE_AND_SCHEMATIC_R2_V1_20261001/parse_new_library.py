import json,pathlib,base64,zipfile,io,collections
p=pathlib.Path(__file__).resolve().parent
blob=json.loads((p/'NEW_LIBRARY_FILE_REV2.json').read_text(encoding='utf-8'))['parsed']['value'];b=base64.b64decode(blob['base64']);assert len(b)==blob['size']
(p/'NEW_LIBRARY.elibz2').write_bytes(b)
z=zipfile.ZipFile(io.BytesIO(b));out=p/'new_library';out.mkdir(exist_ok=True)
assert all((out/n).resolve().is_relative_to(out.resolve())for n in z.namelist());z.extractall(out)
source=z.read(next(n for n in z.namelist() if n.endswith('.elibu'))).decode('utf-8');lines=source.splitlines();docs={};current=None
for i,l in enumerate(lines):
 if not l.strip():continue
 assert '||' in l
 if l.endswith('|'):l=l[:-1]
 else:assert i==len(lines)-1
 h,t=l.split('||',1);h=json.loads(h);t=json.loads(t)
 if h['type']=='DOCHEAD':current=t['uuid'];docs.setdefault(current,{'head':t,'records':[]})
 else:docs[current]['records'].append({'head':h,'body':t})
devices=json.loads((p/'NEW_SELECTED_DEVICES.json').read_text(encoding='utf-8'));parsed={}
for name,d in devices.items():
 sym=docs[d['symbolUuid']];foot=docs[d['footprintUuid']];attrs=collections.defaultdict(dict)
 for r in sym['records']:
  if r['head']['type']=='ATTR':attrs[r['body'].get('parentId')][r['body']['key']]=r['body']['value']
 pins=[dict(local_id=r['head']['id'],number=str(attrs[r['head']['id']]['Pin Number']),name=attrs[r['head']['id']].get('Pin Name'),part=r['body']['partId'],x=r['body']['x'],y=r['body']['y'],rotation=r['body']['rotation'])for r in sym['records']if r['head']['type']=='PIN']
 pads=[r for r in foot['records']if r['head']['type']=='PAD']
 assert len(pins)==len(set(x['number']for x in pins)),name
 assert len(pads)==len(set(str(x['body']['num'])for x in pads)),name
 assert set(x['number']for x in pins)==set(str(x['body']['num'])for x in pads),name
 parsed[name]={'device':d,'pins':pins,'pads':pads}
(p/'NEW_LIBRARY_PARSED.json').write_bytes((json.dumps(parsed,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps({'identities':len(parsed),'pin_pad_correspondence':{n:len(d['pins'])for n,d in parsed.items()}}))
