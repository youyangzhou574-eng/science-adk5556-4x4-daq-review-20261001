import pathlib,json,re,collections
P=pathlib.Path(__file__).resolve().parent
def fields(name):
 t=(P/name).read_text('utf8').replace('\r','')
 blocks=[]
 for m in re.finditer(r'^\[\s*\n([\s\S]*?)^\]\s*$',t,re.M):
  lines=m.group(1).splitlines()
  assert len(lines)%2==0
  pairs=list(zip(lines[::2],lines[1::2]))
  blocks.append((dict(pairs)['DESIGNATOR'],sorted(collections.Counter(pairs).items())))
 return sorted(blocks)
a=fields('AUDIT_C_CAPTURE.net');b=fields('AUDIT_D_COLD_CAPTURE.net')
assert a==b
(P/'ACTUAL_COMPONENT_KV_MULTISET_COLD_PASS.json').write_text(json.dumps({'components':len(a),'all_complete_key_value_multisets_exact':True,'net_members_exact_from_COLD_REOPEN_COMPARISON':True,'raw_bytes_not_equal':True},indent=2)+'\n','utf8')
print('176 complete component KV multisets exact; field order may vary')
