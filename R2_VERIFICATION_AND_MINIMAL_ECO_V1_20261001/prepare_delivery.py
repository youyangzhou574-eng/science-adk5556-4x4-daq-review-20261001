"""Freeze completed evidence and create a credential-free public payload; no simulations."""
from pathlib import Path
import csv,datetime,hashlib,json,re,shutil
import numpy as np
root=Path(__file__).resolve().parent
delivery=root.parent/'GITHUB_R21_DELIVERY_20261001'
payload=delivery/'payload'
assert not payload.exists(), 'Do not silently replace a frozen delivery'
payload.mkdir(parents=True)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def save(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
b=json.loads((root/'EXECUTION_BUDGET.json').read_text())
b['stage_limits_minutes']=b.pop('stage_minutes');b['total_active_limit_minutes']=b.pop('total_active_minutes')
b['phase']='P4_PREPARE';b['time_notes']='Scientific wall42.91485min: P0~8.4, P1~26.1 including preliminary model runs; P2 formal entry to forced stop~2.5min, to scientific close~8.39min including evidence analysis. Subsequent review/software regression/delivery preparation tracked separately; no additional model/design/native work.'
b['review_and_preparation_checkpoint_utc']=now
b['elapsed_since_package_start_minutes_at_preparation']=(datetime.datetime.fromisoformat(now)-datetime.datetime.fromisoformat(b['started_utc'])).total_seconds()/60
save(root/'EXECUTION_BUDGET.json',b)
for name in ['README.md','COMPLETE_R21_RECEIPT.md']:
 p=root/name;s=p.read_text(encoding='utf-8').replace('八状态16测试通过','八状态及接收契约21测试通过').replace('16测试通过：','21测试通过：')
 if name=='COMPLETE_R21_RECEIPT.md':
  s=s.replace('差分计算。','差分计算。最终审查另发现失效清理丢失防重放水位；新增5项回归测试先实际失败，再将同epoch已收帧号/采集时间水位与连续资格分离，并加入跨失效/复位保留的有限单调接收时钟。过期旧帧重放、重复帧重播、倒退时钟、非有限时钟和新epoch时钟倒退均被拒绝，最终21/21通过。RED日志、修复后日志及FINAL_REVIEW.md保留。')
  s=s.replace('全部既有DYNAMIC_VALIDATION_HOLD','最终复查和软件修复不新增模型/设计修订/原生次数。预算字段已明确limit，上限不冒称实耗；正式P2进入至科学收尾约8.39min，停止进程后的分析归档包含其中。发布文件的来源/SHA和敏感下载头脱敏映射见MANIFEST.csv、PUBLIC_SOURCE_MAPPING.csv、PUBLIC_PREPARATION.json。\n\n全部既有DYNAMIC_VALIDATION_HOLD')
 p.write_text(s,encoding='utf-8')
p=root/'RESET_AND_TIMING_CONTRACT.md';s=p.read_text(encoding='utf-8');s+='\n最终软件审查修订：异常/超时仅清连续资格，不清同epoch的已接收帧号及采集时间水位；新帧必须在uint32半区间内向前且采集时间递增。接收器有限单调时钟跨clear及新epoch保留。旧帧不得作为恢复首帧，两帧恢复必须为两帧新的完整连续帧。21项实际回归通过，见FINAL_REVIEW.md。\n';p.write_text(s,encoding='utf-8')
p=root/'IMPLEMENTATION_PLAN.md';s=p.read_text(encoding='utf-8');s=s[:s.index('Progress:')]+'''Final: ruling8620chars received; frozen input verified; P0 qualified. Two design rounds consumed; coupled transient incomplete, stop gate reached. P3 NOT_ENTERED, every native counter0. Software21/21 after real RED-GREEN replay correction. Final review fixes documented. P4 one complete blocked-result upload/handoff, then a successor heartbeat monitor. No further simulations without new unified ruling.\n''';p.write_text(s,encoding='utf-8')
a=np.loadtxt(root/'results/p0_opax388_psa/trace.txt',skiprows=1)
save(root/'results/OPAX388_QUALIFICATION.json',{'status':'PASS_BASIC_FOLLOWER_ONLY','rows':len(a),'all_finite':bool(np.isfinite(a).all()),'steady_step_error_V':float(np.median(abs(a[a[:,0]>3e-6,2]-a[a[:,0]>3e-6,1]))),'model_sha256':digest(root/'models/OPAx388.LIB'),'model_edits':0,'raw_trace':'p0_opax388_psa/trace.txt','not_coupled_qualification':True})
review='''# 最终审查与修复回执

独立审查 r21_final_review：无Critical，1 Important（失效后可重放旧帧）、1 Minor（预算字段limit含义）。审查仅只读，无EDA/仿真/写入。

Important实际反例：合格帧1/2后tick1000，原时间戳旧帧1/2再次valid；另一反例重复帧2触发clear后重新接受帧2，只增加帧3便恢复。原16测试未覆盖。

修复前新增5回归，21项中5失败（results/PROTOCOL_REVIEW_RED.log）。修复后21项全部通过（results/PROTOCOL_TESTS.log）。同epoch seen_id/seen_capture防重放水位不随clear删除；连续资格独立清零；全局有限单调receiver clock跨clear及reset保留。uint32回绕仍通过。新epoch只清该epoch帧水位，接收时钟保持单调。

Minor：stage_limits_minutes/total_active_limit_minutes明确为上限，P2正式进入至科学收尾8.39min含停止后的分析。实耗计数不变。代码/协议证据通过不等于固件WCET、物理故障延迟或整板模型通过；所有电气HOLD保留。
'''
(root/'FINAL_REVIEW.md').write_text(review,encoding='utf-8')
readable=root/'readable';readable.mkdir(exist_ok=True);curves=[]
for p in sorted((root/'results').glob('*/*.txt')):
 if p.name not in ('trace.txt','loop.txt','op.txt'):continue
 try:
  data=np.loadtxt(p,skiprows=1);headers=p.read_text().splitlines()[0].split()
  if data.ndim!=2 or len(headers)!=data.shape[1]:continue
 except ValueError:continue
 out=readable/(p.parent.name+'_'+p.stem+'.csv')
 with out.open('w',encoding='utf-8',newline='')as f:
  w=csv.writer(f);w.writerow(headers);w.writerows(data)
 curves.append({'csv':out.relative_to(root).as_posix(),'source':p.relative_to(root).as_posix(),'source_sha256':digest(p),'rows':len(data),'scope':'exact text-column export, no new simulation'})
save(readable/'CURVE_SOURCE_INDEX.json',curves)
(root/'REPRODUCE.md').write_text('''# 复现材料说明

本版为停止门回执，不授权自动继续模型/EDA。公开原始cases、manufacturer LIB、execution.json及stdout/stderr/原始trace，附同一官方便携archive。原case包含本机绝对.include路径，复现到新位置时仅替换模型根路径，另存派生case并记录旧/新SHA，不覆盖原证据。ngspice命令及cwd见每个execution.json；兼容-n -D ngbehavior=psa。提取archive的bin/docs/share/lib，避免示例Unicode文件名问题；程序未安装到系统。

readable CSV逐列保留原始文本值及单位名称，CURVE_SOURCE_INDEX.json关联原始SHA；PNG提供视觉摘要。coupled三次均无完整波形，只有失败日志，禁止用单TIA CSV替代耦合结果。原始模型和两个原厂来源包完整保留。原版R2工程/PDF在README固定历史commit入口，没有新原生输出。

下载diagnosis中的HTTP cookie/临时签名查询仅在公开副本去除，原始本地证据保留，PUBLIC_SOURCE_MAPPING.csv记两端SHA。原厂便携包为复现附件，正文和波形均有独立可读文件，不依赖压缩包或LFS。
''',encoding='utf-8')
mapping=[]
for p in sorted(root.rglob('*')):
 if not p.is_file():continue
 rel=p.relative_to(root)
 if '__pycache__'in rel.parts:continue
 if rel.parts[0]=='runtime' and rel.as_posix()!='runtime/ngspice-47_64.7z':continue
 target=payload/rel;target.parent.mkdir(parents=True,exist_ok=True)
 if p.name in ('NGSPICE_DOWNLOAD_DIAGNOSIS.json','NGSPICE_MIRROR_DOWNLOAD.json'):
  data=json.loads(p.read_text())
  def clean(x):
   if isinstance(x,dict):return {k:('[REDACTED_EPHEMERAL_HEADER]' if any(v in k.lower()for v in ['cookie','authorization'])else clean(v))for k,v in x.items()}
   if isinstance(x,list):return [clean(v)for v in x]
   if isinstance(x,str):
    x=re.sub(r'https?://[^\s\"<>]+',lambda m:m.group(0).split('?')[0]+'?[EPHEMERAL_QUERY_REMOVED]'if '?'in m.group(0)else m.group(0),x)
    return x
   return x
  save(target,clean(data));action='SANITIZED_HTTP_EPHEMERAL_HEADERS_AND_QUERY'
 else:shutil.copyfile(p,target);action='EXACT_COPY'
 mapping.append({'path':rel.as_posix(),'local_sha256':digest(p),'public_sha256':digest(target),'action':action})
with(payload/'PUBLIC_SOURCE_MAPPING.csv').open('w',encoding='utf-8',newline='')as f:
 w=csv.DictWriter(f,fieldnames=list(mapping[0]));w.writeheader();w.writerows(mapping)
patterns={'github_token':r'gh[pousr]_[A-Za-z0-9]{20,}','github_pat':r'github_pat_[A-Za-z0-9_]{30,}','openai_key':r'sk-(?:proj-)?[A-Za-z0-9_-]{25,}','private_key':r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----','jwt':r'eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}','actual_cookie':r'(?i)(?:cf_clearance|__cf_bm)\s*[=:]\s*[A-Za-z0-9_+/.-]{20,}'}
hits=[]
for p in payload.rglob('*'):
 if not p.is_file()or p.suffix.lower()in ('.png','.pdf','.7z','.zip'):continue
 s=p.read_text(encoding='utf-8',errors='replace')
 for kind,pat in patterns.items():
  if re.search(pat,s):hits.append({'path':p.relative_to(payload).as_posix(),'kind':kind})
assert not hits, hits
baseline=json.loads((root/'P0_INPUT_VERIFIED.json').read_text());bp=Path(baseline['path']);assert digest(bp)==baseline['sha256']
save(delivery/'PREPARE_AND_SCAN.json',{'utc':now,'credential_pattern_hits':hits,'scope':'only R21 circuit project','raw_originals_preserved':True,'public_files':sum(p.is_file()for p in payload.rglob('*')),'csv_exports':len(curves),'baseline_native_unchanged':True,'baseline_sha256':digest(bp)})
save(payload/'PUBLIC_PREPARATION.json',{'scope':'only R21 circuit','credential_pattern_hits':0,'sanitized_files':[m for m in mapping if m['action']!='EXACT_COPY'],'source_mapping':'PUBLIC_SOURCE_MAPPING.csv','baseline_native_unchanged':True,'csv_exports':len(curves),'license_notes':'Original manufacturer and ngspice source/distribution notices retained inside supplied original packages; no modified manufacturer models.'})
files=[]
for p in sorted(payload.rglob('*')):
 if p.is_file():files.append({'path':p.relative_to(payload).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)})
with(payload/'MANIFEST.csv').open('w',encoding='utf-8',newline='')as f:
 w=csv.DictWriter(f,fieldnames=['path','bytes','sha256']);w.writeheader();w.writerows(files)
save(delivery/'PAYLOAD_FROZEN.json',{'utc':now,'files':len(files)+1,'bytes':sum(x['bytes']for x in files)+(payload/'MANIFEST.csv').stat().st_size,'report_sha256':digest(payload/'COMPLETE_R21_RECEIPT.md'),'manifest_sha256':digest(payload/'MANIFEST.csv'),'csv_exports':len(curves)})
source=root.parent/'GITHUB_R2_DELIVERY_20261001'
s=(source/'github_delivery.py').read_text().replace('FIRST_BUILD_ELECTRICAL_CLOSURE_AND_SCHEMATIC_R2_V1_20261001','R2_VERIFICATION_AND_MINIMAL_ECO_V1_20261001').replace('Deliver R2 electrical closure report, native schematic and complete audited evidence','Deliver R2.1 actual model verification and complete blocked-gate evidence')
(delivery/'github_delivery.py').write_text(s,encoding='utf-8');shutil.copyfile(source/'run_network.py',delivery/'run_network.py')
print(json.dumps(json.loads((delivery/'PAYLOAD_FROZEN.json').read_text())))
