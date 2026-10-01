import json,pathlib
p=pathlib.Path(__file__).resolve().parent
d=json.loads((p/'CORE_DEVICES_SELECTED.json').read_text(encoding='utf-8'))
passive=json.loads((p/'LIB_PASSIVE_CANDIDATES.json').read_text(encoding='utf-8'))['parsed']['value']['results']
for r in passive:
 exact=next((i for i in r['items'] if i['name']==r['key']),None)
 if exact:d[r['key']]=exact
extra=json.loads((p/'LIB_CONNECTOR_CAP_SEARCH.json').read_text(encoding='utf-8'))['parsed']['value']['results']
for r in extra:
 if r['key']=='CL31A226KAHNNNE':continue
 if r['key']=='GRM32ER71E226KE15L':d[r['key']]=next(i for i in r['items'] if i['name']==r['key']);continue
 wanted=r['key'].replace('HDR-M-2.54_','HDR-M_2.54_')+'P'
 exact=next((i for i in r['items'] if i['name']==wanted),None)
 assert exact is not None,wanted
 d[wanted]=exact
assert len(d)==22,len(d)
(p/'ALL_SELECTED_DEVICES.json').write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
(p/'EXPORT_ALL_ARGS.json').write_bytes(json.dumps({'uuids':[v['uuid']for v in d.values()]},ensure_ascii=False).encode('utf-8'))
print(json.dumps({'selected_count':len(d),'names':list(d)}))
