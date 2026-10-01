import pathlib,json
p=pathlib.Path(__file__).resolve().parent;selected={}
names=['LM73100RPWR','SN74LVC08APWR','GRM1885C1H101JA01D','GRM31CR71H225KA88L','RC2010FK-07100RL','RC1206FR-07100RL','TPS389001DSET','BAT54S,215']
for file in ['NEW_LIBRARY_SEARCH.json','MORE_LIBRARY_SEARCH.json','LAST_LIBRARY_SEARCH.json']:
 for group in json.loads((p/file).read_text(encoding='utf-8'))['parsed']['value']['results']:
  for d in group['items']:
   if d['name'] in names and d['manufacturerId']==d['name']:selected[d['name']]=d
assert set(selected)==set(names)
(p/'NEW_SELECTED_DEVICES.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(p/'EXPORT_NEW_ARGS.json').write_text(json.dumps({'uuids':[d['uuid']for d in selected.values()]})+'\n',encoding='utf-8')
v=p.parent/'FIRST_BUILD_DETAILED_DESIGN_AND_NATIVE_SCHEMATIC_V1'
old=json.loads((v/'CORE_LIBRARY_FILE.json').read_text(encoding='utf-8'))['command']
code=old[old.index('--code')+1]
(p/'export_new_library.js').write_text(code,encoding='utf-8')
b=json.loads((p/'EXECUTION_BUDGET.json').read_text());b['counts'].update(new_primary_sources=7,new_library_identities=8,library_search_and_readbacks=14,new_function_classes=5,design_revisions=1)
(p/'EXECUTION_BUDGET.json').write_text(json.dumps(b,indent=2)+'\n')
print(json.dumps({'selected':names,'export_args_ready':True}))
