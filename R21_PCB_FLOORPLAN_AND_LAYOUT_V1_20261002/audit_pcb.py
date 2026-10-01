import pathlib,json,csv,sys,collections
P=pathlib.Path(__file__).resolve().parent;label=sys.argv[1]
v=json.loads((P/(label+'.json')).read_text('utf8'))['parsed']['value'];plan=json.loads((P/'PCB_COMPONENT_PLAN.json').read_text('utf8'))
actual={c['ref']:c for c in v['parts']};checks=[];nc=[];errors=[]
for c in plan:
 a=actual.get(c['ref']);
 if not a:errors.append('missing '+c['ref']);continue
 pads={p['number']:p for p in a['pads']}
 for n,net in c['nets'].items():
  got=pads.get(n,{}).get('net');checks.append({'ref':c['ref'],'pin':n,'expected':net,'actual':got,'pass':got==net})
 for n in c['nc']:
  got=pads.get(n,{}).get('net');nc.append({'ref':c['ref'],'pin':n,'actual':got,'pass':n in pads and not got})
 if {p['number']for p in a['pads']}!=set(c['nets'])|set(c['nc']):errors.append('pad coverage '+c['ref'])
 # Native creation remaps global library UUIDs into the new project's local library.
 # Preserve both identities; compare the resolved native device/footprint names, not unrelated UUID namespaces.
 resolved=a['device']['uuid']
 if not isinstance(resolved,dict) or resolved.get('name')!=c['device']:errors.append('resolved device name '+c['ref'])
 if a['footprint']['name']!=c['deviceItem']['footprintName']:errors.append('resolved footprint name '+c['ref'])
if len(actual)!=176:errors.append('componentcount')
r={'parts':len(actual),'connectedChecked':len(checks),'connectedPass':sum(x['pass']for x in checks),'ncChecked':len(nc),'ncPass':sum(x['pass']for x in nc),'actualNonEmptyNets':len({p['net']for a in actual.values()for p in a['pads']if p['net']}),'physicalPads':sum(len(a['pads'])for a in actual.values()),'errors':errors,'pass':not errors and all(x['pass']for x in checks+nc)}
(P/(label+'_MAPPING_CHECK.json')).write_text(json.dumps(r,indent=2),'utf8');(P/(label+'_SOURCE.txt')).write_text(v['source'],'utf8')
for name,rows in [('PINS',checks),('NC',nc)]:
 with (P/(label+'_'+name+'.csv')).open('w',newline='',encoding='utf8')as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(json.dumps(r));
if not r['pass']:raise SystemExit('STOP actual mapping failure')
