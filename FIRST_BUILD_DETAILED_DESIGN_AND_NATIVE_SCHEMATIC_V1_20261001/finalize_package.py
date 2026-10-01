import pathlib,json,hashlib,datetime,collections,re
from pypdf import PdfReader
p=pathlib.Path(__file__).resolve().parent
def j(n):return json.loads((p/n).read_text(encoding='utf-8-sig'))
def sha(q):return hashlib.sha256(q.read_bytes()).hexdigest().upper()
pre=j('REPAIRED_PRE_CLOSE_CONNECTIVITY_AUDIT.json');post=j('POST_REOPEN_CONNECTIVITY_AUDIT.json')
assert pre['pass']and post['pass']
canonical=dict(pin_checks_exact=pre['pin_checks']==post['pin_checks'],net_members_exact=pre['net_members']==post['net_members'],footprint_names_exact={x['ref']:x['actual_footprint']['name']for x in pre['part_identity']}=={x['ref']:x['actual_footprint']['name']for x in post['part_identity']})
assert all(canonical.values())
def metadata(n):
 t=(p/n).read_bytes().decode('utf-8').replace('\r\r\n','\n').replace('\r\n','\n').replace('\r','\n')
 records={}
 for m in re.finditer(r'^\[\s*\n([\s\S]*?)^\]\s*$',t,re.M):
  lines=m.group(1).splitlines();ref=lines[1].strip();ix=lines.index('*');pairs=lines[:ix]
  if pairs and pairs[-1]=='':pairs=pairs[:-1]
  assert len(pairs)%2==0,(ref,len(pairs))
  records[ref]=collections.Counter(zip(pairs[::2],pairs[1::2]))
 return records
canonical['full_component_key_value_multisets_exact']=metadata('REPAIRED_PRE_CLOSE_CAPTURE.net')==metadata('POST_REOPEN_CAPTURE_EXPORT_ACTUAL.net')
assert canonical['full_component_key_value_multisets_exact']
canonical.update(raw_bytes_identical=(p/'REPAIRED_PRE_CLOSE_CAPTURE.net').read_bytes()==(p/'POST_REOPEN_CAPTURE_EXPORT_ACTUAL.net').read_bytes(),difference='component metadata field ordering changed after reopen; exact unordered key-value multisets and all physical pin/nets/footprint names equal')
(p/'PERSISTENCE_COMPARISON.json').write_text(json.dumps(canonical,indent=2)+'\n',encoding='utf-8')
native=pathlib.Path(r'C:\Users\yang\Documents\LCEDA-Pro\projects\SCIENCE_ADK5556_4X4_FIRST_BUILD_V1.eprj2')
copy=p/native.name;save=j('NATIVE_SAVE_COPY.json');assert sha(native)==sha(copy)==save['sha256']
assert j('CLOSE_FIRST_BUILD_SESSION_ACTUAL.json')['parsed']['value']['status']=='closed'
assert j('CLOSE_REOPEN_SESSION.json')['parsed']['value']['status']=='closed'
pdf=p/'FIRST_BUILD_REVIEW_ONLY.pdf';reader=PdfReader(str(pdf));assert len(reader.pages)==4
visual={'pages':4,'actual_native_export':True,'rendered_all_four_pages_and_visually_inspected':True,'readable_values_and_warning_notes':True,'issues':['some port net text collides with IC pin numbering/names and some designators','some leftmost BI port polygons meet or extend across the drawing border; no pin/net data lost in actual netlist'],'status':'DRAWING_LAYOUT_HOLD','drawing_export_budget_used':2,'drawing_export_budget_limit':2,'next_action':'separate approved layout correction with real attribute visibility/position handling and new export budget; do not exceed current budget'}
(p/'DRAWING_VISUAL_QA.json').write_text(json.dumps(visual,indent=2)+'\n',encoding='utf-8')
(p/'NATIVE_GENERATION_CORRECTION.md').write_text((p/'NATIVE_GENERATION_CORRECTION.md').read_text(encoding='utf-8')+'\n追加：部分10nF原生符号为垂直引脚，首个修复拒绝270°并停下，明确保留错误API证据，后按实际位置支持垂直引脚并将4个ADC滤波电容旋转90°，不改针号或网络。冷重开工程runtime UUID改变为07975f0d...33402；首次静态旧UUID守卫拒绝、零capture/修改。根据官方open绝对路径/字节hash、完整原project对象及同一schematic/4page UUID和parent链接受新运行态UUID。不是错误工程，也不是工具不兼容。\n',encoding='utf-8')
timing=[]
commands=[0xC000,0xC400,0xC800,0xCC00]
for row in range(4):
 start=row*2500
 for state,base in [('blank',start),('active',start+1100)]:
  timing.append({'row':row,'state':state,'CS_us':base+250,'result_channel':'previous;discard','command_hex':'C000','purpose':'select CH0 for next frame; output is discarded during settling'})
  selected=0
  for k in range(16):
   nxt=(k+1)%4;timing.append({'row':row,'state':state,'CS_us':base+300+50*k,'result_channel':selected,'command_hex':f'{commands[nxt]:04X}','SPI_finish_us':base+308+50*k,'purpose':'valid planned acquisition; no actual firmware/SPI test'})
   selected=nxt
assert max(e['CS_us']for e in timing)<10000
(p/'SPI_EVENT_PLAN.json').write_text(json.dumps({'source':'ADS8684 RevC8.4.1.1.1/Table6; next frame channel; full32clocks4MHz','events':timing,'hardware_verified':False,'configuration_readback_and_range_setup':'firmware pending'},indent=2)+'\n',encoding='utf-8')
validation=j('VALIDATION_SUMMARY.json')
summary={'project':'SCIENCE_ADK5556_4X4_DAQ_REPLICA','package':'SCIENCE_ADK5556_4X4_FIRST_BUILD_DETAILED_DESIGN_AND_NATIVE_SCHEMATIC_V1','decision':'CIRCUIT-PRO-FIRST-BUILD-INTEGRATED-DESIGN-GATES-20261001-01','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'state':'NATIVE_SCHEMATIC_DELIVERED / DYNAMIC_VALIDATION_HOLD / FAULT_PROTECTION_HOLD / REFERENCE_CAPACITANCE_HOLD / ERC_DETAIL_HOLD / DRAWING_LAYOUT_HOLD','bench_released':False,'user_facts':['fixed4rows+4columns8electrode leads','approx1-7kohm / approx10%change; not metrologically frozen'],'native_file':save,'pdf':{'path':str(pdf),'bytes':pdf.stat().st_size,'sha256':sha(pdf),'pages':4,'status':visual['status']},'connectivity':{k:post[k]for k in ['expected_connected_pins','passed_connected_pins','expected_NC_count','actual_NC_count','actual_net_count','actual_parts','actual_component_blocks','pass']},'persisted_native_hash_unchanged_after_reopen_and_close':True,'persistence':canonical,'budgets_used':{'core_types':7,'library_identities':22,'P1_lookup_and_library_reads_conservative':54,'sources':'primary datasheets/EVM/Yageo plus2 model download locators; within20; failures/redirects retained in ledgers','model_downloads':2,'passive_protection_revision_rounds':1,'DC_groups':validation['dc_groups'],'AC_cases':0,'normal_transient_cases':0,'fault_transient_cases':0,'fault_static_qualitative_cases':24,'native_new_projects':1,'native_sessions':2,'save_invocations_returning_true':5,'complete_connection_audits':3,'native_connection_and_File_netlist_capture_versions':3,'native_DRC':1,'drawing_export_versions':2},'stage_evidence_timestamps_utc':{n:datetime.datetime.fromtimestamp((p/n).stat().st_mtime,datetime.timezone.utc).isoformat()for n in ['P1_COMPLETION.md','detailed_design.py','VALIDATION_SUMMARY.json','CREATE_FOUR_PAGES.json']},'native_sessions_closed':['14431564-62fb-4c45-9e30-adc4717bdb9b','1c6c22f6-f5bf-45b0-8cc4-1e696b6b45a7'],'actual_pending_or_timeout':False,'zero_operations':['oldmaster open/copy/write','customlibrary device/symbol/footprint create','PCB','manufacturing','procurement','Git writes','directDB/cache/profile/activation/system writes','third-party install'],'remaining':['manufacturer macro AC/normal transient and output recovery/loop PMGM','hardware single-fault/power sequence/backfeed/60sthermal and fault detection','REFIO effective capacitance >=10uF at4.096V and assembly traceability for generic headers','native10warn full descriptions/classification','IC port-label layout correction; export budget exhausted','full accuracy/noise/temperature/lead-resistance and standard bench validation; planned firmware not executed'],'pro_request':'Accept exact saved/reopened native connectivity and bounded DC findings, retain all HOLDs; give unique next package and budget for electrical protection/dynamic closure and explicit layout/DRC detail allowance. No PCB/manufacturing release.'}
(p/'EXECUTION_SUMMARY.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(p/'VALIDATION_REPORT.md').write_text((p/'VALIDATION_REPORT.md').read_text(encoding='utf-8')+'\n静态故障电阻界的前提是两端在0–5.25V、无电容尖峰；不是内部钳位/输出或供电时序的保证。时序规划136条（每状态1dummy+16有效，共8窗口），未运行固件。首次进入模式和寄存器配置属于startup，另需验证。\n',encoding='utf-8')
files=[]
for q in sorted(p.rglob('*')):
 if q.is_file()and q.name not in ['PACKAGE_HASHES.json','PRO_FIRST_BUILD_RECEIPT.txt','PRO_DELIVERY.json']:
  files.append({'relative_path':str(q.relative_to(p)),'bytes':q.stat().st_size,'sha256':sha(q)})
(p/'PACKAGE_HASHES.json').write_text(json.dumps({'root':str(p),'files':files},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'summary':summary,'file_count':len(files)},ensure_ascii=True))
