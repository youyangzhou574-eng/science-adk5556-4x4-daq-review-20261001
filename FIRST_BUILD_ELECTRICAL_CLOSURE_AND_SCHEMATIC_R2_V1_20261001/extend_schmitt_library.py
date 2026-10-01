import pathlib,json
p=pathlib.Path(__file__).resolve().parent
selected=json.loads((p/'NEW_SELECTED_DEVICES.json').read_text(encoding='utf-8'))
d=json.loads((p/'SCHMITT_LIBRARY_SEARCH.json').read_text(encoding='utf-8'))['parsed']['value']['items']
selected['SN74LVC1G17DBVR']=next(x for x in d if x['name']=='SN74LVC1G17DBVR'and x['manufacturerId']=='SN74LVC1G17DBVR')
(p/'NEW_SELECTED_DEVICES.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(p/'EXPORT_NEW_ARGS.json').write_text(json.dumps({'uuids':[x['uuid']for x in selected.values()]})+'\n')
# Preserve earlier eight-identity export rather than overwrite.
for src,dst in [('NEW_LIBRARY_FILE.json','NEW_LIBRARY_FILE_REV1.json'),('NEW_LIBRARY_PARSED.json','NEW_LIBRARY_PARSED_REV1.json')]:
 if not(p/dst).exists():(p/dst).write_bytes((p/src).read_bytes())
