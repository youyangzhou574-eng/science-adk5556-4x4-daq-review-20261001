import pathlib,json,re,hashlib,sys,collections
p=pathlib.Path(__file__).resolve().parent
label=sys.argv[1];outname=sys.argv[2]
raw=json.loads((p/(label+'.json')).read_text(encoding='utf-8'));assert raw['parsed']['ok'] is True
cap=raw['parsed']['value'];plan=json.loads((p/'ENGINEERING_PLAN.json').read_text(encoding='utf-8'));libs=json.loads((p/'ENGINEERING_LIBRARY_PARSED.json').read_text(encoding='utf-8'))
f=cap['actualFile'];assert f and f['constructor']=='File' and f['tag']=='[object File]'
b=bytes(f['bytes']);assert len(b)==f['size'];(p/(label+'.net')).write_bytes(b)
try:text=b.decode('utf-8-sig');encoding='UTF-8'
except UnicodeDecodeError:text=b.decode('gb18030');encoding='GB18030 strict'
# Original actual bytes remain untouched. Normalize vendor CRCRLF only for parsing.
txt=text.replace('\r\r\n','\n').replace('\r\n','\n').replace('\r','\n')
assert txt.startswith('PROTEL NETLIST 2.0')
pins={};nets={};blocks=[]
for m in re.finditer(r'^\(\s*\n([^\n]+)\n([\s\S]*?)^\)\s*$',txt,re.M):
 net=m.group(1).strip();assert net and net not in nets,'Duplicate/empty net'
 members=[]
 for line in m.group(2).splitlines():
  if not line.strip():continue
  key=line.split()[0];assert re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*-[0-9]+',key),key
  assert key not in pins,'Duplicate physical pin '+key
  pins[key]=net;members.append(key)
 assert members,'Empty net';nets[net]=sorted(members)
for m in re.finditer(r'^\[\s*\n([\s\S]*?)^\]\s*$',txt,re.M):
 lines=m.group(1).splitlines();assert lines[0]=='DESIGNATOR';ref=lines[1].strip();fi=lines.index('FOOTPRINT');fp=lines[fi+1].strip();assert fp and fp.lower()!='undefined' and not fp.startswith('AUDIT_ONLY')
 blocks.append(dict(ref=ref,footprint=fp))
expect={q['ref']+'-'+n:net for q in plan['parts']for n,net in q['nets'].items()if net is not None}
nc={q['ref']+'-'+n for q in plan['parts']for n,net in q['nets'].items()if net is None}
checks=[dict(pin=k,expected=v,actual=pins.get(k),pass_=pins.get(k)==v)for k,v in expect.items()]
placed=[c for pg in cap['pages']for c in pg['parts']if c['type']=='part'];actualNC={c['ref']+'-'+v['number']for c in placed for v in c['pins']if v['nc']}
refcount=collections.Counter(c['ref']for c in placed);blockcount=collections.Counter(c['ref']for c in blocks)
identity=[]
for q in plan['parts']:
 cs=[c for c in placed if c['ref']==q['ref']]
 good=len(cs)==1
 if good:
  c=cs[0];d=libs[q['device']]['device'];actualNumbers=[v['number']for v in c['pins']]
  good=set(actualNumbers)==set(q['nets'])and len(actualNumbers)==len(set(actualNumbers))and c['sub']==q['subpart']and c['footprint'].get('name')==d['footprintName']
 identity.append(dict(ref=q['ref'],actual_footprint=cs[0]['footprint']if cs else None,expected_footprint_name=libs[q['device']]['device']['footprintName'],pass_=good))
netchecks=[dict(net=k,expected=sorted(n for n,v in expect.items()if v==k),actual=nets.get(k,[]),pass_=sorted(n for n,v in expect.items()if v==k)==nets.get(k,[]))for k in sorted(set(expect.values())|set(nets))]
report=dict(actual_source=label,raw_sha256=hashlib.sha256(b).hexdigest().upper(),raw_bytes=len(b),parser_encoding=encoding,File_text_has_replacement_character='\ufffd'in f['text'],no_reencoding_of_actual_netlist=True,pin_checks=checks,net_members=netchecks,part_identity=identity,expected_connected_pins=len(expect),passed_connected_pins=sum(q['pass_']for q in checks),expected_NC_count=len(nc),actual_NC_count=len(actualNC),NC_exact_match=actualNC==nc,NC_in_actual_nets=sorted(nc&set(pins)),missing_pins=sorted(set(expect)-set(pins)),unexpected_pins=sorted(set(pins)-set(expect)),expected_net_count=len(set(expect.values())),actual_net_count=len(nets),expected_parts=len(plan['parts']),actual_parts=len(placed),actual_component_blocks=len(blocks),duplicates={k:v for k,v in refcount.items()if v!=1},block_duplicates={k:v for k,v in blockcount.items()if v!=1},pages=len(cap['pages']),manufacturing_release=False)
report['pass']=all(q['pass_']for q in checks+netchecks+identity)and actualNC==nc and not report['missing_pins']and not report['unexpected_pins']and not report['NC_in_actual_nets']and set(refcount)==set(blockcount)=={q['ref']for q in plan['parts']}and not report['duplicates']and not report['block_duplicates']and len(placed)==len(plan['parts'])
(p/outname).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items()if k not in ['pin_checks','net_members','part_identity']},ensure_ascii=True))
if not report['pass']:raise SystemExit(2)
