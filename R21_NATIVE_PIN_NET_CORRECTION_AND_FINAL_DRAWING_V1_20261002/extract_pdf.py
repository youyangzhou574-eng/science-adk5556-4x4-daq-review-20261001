import pathlib,json,base64,hashlib,sys
P=pathlib.Path(__file__).resolve().parent
r=json.loads((P/(sys.argv[1]+'.json')).read_text('utf8'))
assert r['parsed']['ok']
f=r['parsed']['value']['pdf'];assert f['constructor']=='File'
b=base64.b64decode(f['base64']);assert len(b)==f['size']
(P/sys.argv[2]).write_bytes(b)
print(json.dumps({'file':sys.argv[2],'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest().upper()}))
