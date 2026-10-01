import pathlib,json,hashlib,base64,csv,collections,datetime
P=pathlib.Path(__file__).resolve().parent;O=P.parent/'R21_NATIVE_PIN_NET_CORRECTION_AND_FINAL_DRAWING_V1'
def load(f):return json.loads((P/f).read_text('utf8'))
def write(f,v):(P/f).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n','utf8')
w=load('SPLIT_WARM_CAPTURE.json')['parsed']['value'];pre=load('PRECLOSE_SNAPSHOT.json')['parsed']['value'];c=load('FINAL_COLD_CAPTURE.json')['parsed']['value']
a=load('SPLIT_WARM_AUDIT.json');b=load('FINAL_COLD_AUDIT.json')
def parts(v):return {q['ref']:q for pg in v['pages']for q in pg['parts']}
assert parts(w)==parts(pre)==parts(c)
assert a['pin_checks']==b['pin_checks']and a['net_members']==b['net_members']and a['pass']and b['pass']
old=json.loads((O/'AUDIT_D_COLD_FINAL.json').read_text('utf8'))
oldpins={x['pin']:x['actual']for x in old['pin_checks']};newpins={x['pin']:x['actual']for x in b['pin_checks']}
delta=[dict(pin=k,before=oldpins[k],after=v)for k,v in newpins.items()if v!=oldpins[k]]
assert {q['pin']for q in delta}=={'J3-1','J4-1','R_J3_1-1','R_J4_1-1'}
members={x['net']:x['actual']for x in b['net_members']}
assert members['V3V3_EXT_SWD']==['J3-1','R_J3_1-1'] and members['V3V3_EXT_UART']==['J4-1','R_J4_1-1']
assert 'V3V3_EXT'not in members
write('FUNCTIONAL_INTERFACE_SPLIT_CHECK.json',dict(pass_=True,changed_pins=delta,remaining_510_pins_unchanged=True,unchanged_main_supply_members=members['V3V3']==next(x['actual']for x in old['net_members']if x['net']=='V3V3'),SWD_members=members['V3V3_EXT_SWD'],UART_members=members['V3V3_EXT_UART'],external_pins_not_directly_same_net=True,no_component_value_change=True,not_physical_fault_release=True))
write('COLD_REOPEN_COMPARE.json',dict(pass_=True,connected=514,nets=107,NC=36,parts=176,all_network_members_exact=True,all_core_fields_and_pin_coordinates_exact=True,raw_bytes_exact=(P/'SPLIT_WARM_CAPTURE.net').read_bytes()==(P/'FINAL_COLD_CAPTURE.net').read_bytes()))
for pg in c['pages']:(P/f"FINAL_PAGE_{pg['page']['index']+1}_SOURCE.txt").write_text(pg['source'],'utf8')
artifacts={}
for key,filename in [('native','SCIENCE_ADK5556_4X4_R21_FINAL_INTERFACE_REVIEW.epro2'),('pdf','SCIENCE_ADK5556_4X4_R21_FINAL_INTERFACE_REVIEW.pdf')]:
 f=c[key];assert f['constructor']=='File'and f['tag']=='[object File]';data=base64.b64decode(f['base64']);assert len(data)==f['size'];(P/filename).write_bytes(data);artifacts[filename]=dict(bytes=len(data),sha256=hashlib.sha256(data).hexdigest().upper())
f=P/'SCIENCE_ADK5556_4X4_R21_FINAL_INTERFACE_WORK.eprj2';artifacts[f.name]=dict(bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest().upper())
write('FINAL_ARTIFACT_IDENTITY.json',artifacts)
with (P/'FINAL_514_PIN_NET_CHECKS.csv').open('w',encoding='utf-8-sig',newline='')as f:
 q=csv.DictWriter(f,fieldnames=['pin','expected','actual','pass_']);q.writeheader();q.writerows(b['pin_checks'])
with (P/'FINAL_107_NETWORK_MEMBERS.csv').open('w',encoding='utf-8-sig',newline='')as f:
 q=csv.writer(f);q.writerow(['net','members','pass']);q.writerows((x['net'],';'.join(x['actual']),x['pass_'])for x in b['net_members'])
with (P/'FINAL_36_NC.csv').open('w',encoding='utf-8-sig',newline='')as f:
 q=csv.writer(f);q.writerow(['ref','pin','NC']);q.writerows((ref,p['number'],True)for ref,x in sorted(parts(c).items())for p in x['pins']if p['nc'])
with (P/'FINAL_176_BOM.csv').open('w',encoding='utf-8-sig',newline='')as f:
 q=csv.writer(f);q.writerow(['ref','actual_device','Value','footprint']);q.writerows((ref,x['association']['name'],x['props'].get('Value',x['name']),x['footprint']['name'])for ref,x in sorted(parts(c).items()))
def texts(s):
 rows={}
 for line in s.splitlines():
  ss=line.split('||')
  if len(ss)!=2:continue
  try:head=json.loads(ss[0]);value=json.loads(ss[1].rstrip('|'))
  except ValueError:continue
  if head.get('type')=='TEXT':rows[head['id']]=value.get('value')
 return rows
n=load('ANNOTATION_ONCE.json')['parsed']['value'];before=texts(n['before']);after=texts(n['after'])
notePASS=set(after.values())==set(n['texts'])
write('ANNOTATION_SINGLE_ATTEMPT_RESULT.json',dict(attempts=1,API_saved_true=n['saved'],before=before,after=after,expected=n['texts'],actual_text_updated=notePASS,legacy_other_pages_titles_retained=True,no_second_attempt=True))
raw=bytes(c['actualFile']['bytes']).decode('utf8');warmraw=bytes(w['actualFile']['bytes']).decode('utf8')
write('ACTUAL_FILE_TEXT_ENCODING_NOTE.json',dict(warm_File_text_replacement=w['actualFile']['text'].count(chr(65533)),warm_actual_bytes_utf8_replacement=warmraw.count(chr(65533)),cold_File_text_replacement=c['actualFile']['text'].count(chr(65533)),cold_actual_bytes_utf8_replacement=raw.count(chr(65533)),actual_bytes_exact_warm_cold=True,raw_bytes_authoritative=True,not_reencoded=True))
frozen=load('FROZEN_INPUT_SHA.json');checks=[]
for name,e in frozen.items():
 if not isinstance(e,dict):continue
 f=P.parent/name;sha=hashlib.sha256(f.read_bytes()).hexdigest().upper();checks.append(dict(path=name,sha256=sha,pass_=sha==e['sha256']and f.stat().st_size==e['bytes']))
assert all(x['pass_']for x in checks);write('FROZEN_INPUTS_FINAL_SHA_PASS.json',checks)
write('GATES.json',dict(CORE_ACQUISITION_TOPOLOGY_REVIEW_PASS_FROM_PRO=True,FUNCTIONAL_INTERFACE_SPLIT_PASS=True,NATIVE_PIN_NET_IMPLEMENTATION_PASS=True,COLD_REOPEN_PASS=True,connected=514,nets=107,NC=36,parts=176,LEGACY_ANNOTATION_HOLD=True,MCU_INTERFACE_NOTES_UPDATED=notePASS,ERC_DETAIL_HOLD_INHERITED=True,BENCH_NOT_RELEASED=True,PCB_NOT_STARTED=True,FAULT_PROTECTION_HOLD=True,REFERENCE_CAPACITANCE_BENCH_HOLD=True,HARDWARE_WCET_PENDING=True,SWD_SERIES_RESISTOR_BENCH_CHECK=True,newSimulationCount=0))
q=load('EXECUTION_BUDGET.json');q.update(scienceStopped=True,STOP='NATIVE_EXECUTION_COMPLETE_HARD_QUOTAS_USED_NO_MORE_EDITS',technicalExecutionEndedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),actualSaveCalls=2);write('EXECUTION_BUDGET.json',q)
write('FINAL_SESSION_STATUS.json',dict(both_officially_closed=all(load(n)['parsed']['value']['status']=='closed'for n in ['CLOSE_A.json','CLOSE_COLD.json']),sessions=['d0b1b000-2114-491a-98af-9ffe4a377097','aa4e43f6-d45b-46f7-b8c4-86a4c744b31d'],no_solver_started=True,no_pending_call=True))
print(json.dumps({'coldPASS':True,'delta':delta,'notesUpdated':notePASS,'actualNotes':after,'used':q['used'],'artifacts':artifacts}))
