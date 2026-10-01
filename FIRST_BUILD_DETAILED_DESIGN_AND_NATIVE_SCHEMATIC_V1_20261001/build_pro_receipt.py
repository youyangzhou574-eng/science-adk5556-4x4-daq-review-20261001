import pathlib,json,hashlib,datetime,csv
p=pathlib.Path(__file__).resolve().parent
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest().upper()
with(p/'EXACT_BOM_AND_PINMAP.csv').open(encoding='utf-8-sig',newline='')as f:pinrows=list(csv.DictReader(f))
for row in pinrows:row['remaining']='post-reopen pin/net PASS; dynamic/fault/effective-reference-cap/assembly/bench HOLD'
with(p/'EXACT_BOM_AND_PINMAP.csv').open('w',encoding='utf-8-sig',newline='')as f:w=csv.DictWriter(f,fieldnames=list(pinrows[0]));w.writeheader();w.writerows(pinrows)
report=(p/'VALIDATION_REPORT.md').read_text(encoding='utf-8').replace('完整137个时序事件中136条实际生成规划（每状态1dummy+16有效，共8窗口=136），未运行固件。','时序规划136条（每状态1dummy+16有效，共8窗口），未运行固件。')
(p/'VALIDATION_REPORT.md').write_text(report,encoding='utf-8')
raw=json.loads((p/'POST_REOPEN_CAPTURE_EXPORT_ACTUAL.json').read_text(encoding='utf-8'))['parsed']['value']
snapshot={'project':{k:raw['project'].get(k)for k in ['uuid','name','friendlyName','teamUuid']},'pages':[{'page':q['page'],'parts':[{k:c.get(k)for k in ['id','ref','name','sub','association','footprint','pins']}for c in q['parts']if c['type']=='part']}for q in raw['pages']]}
(p/'PLACED_POST_REOPEN_INSTANCE_SNAPSHOT.json').write_text(json.dumps(snapshot,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
summary=json.loads((p/'EXECUTION_SUMMARY.json').read_text(encoding='utf-8'))
summary['timing_events']=136
summary['P4_elapsed_minutes_through_final_native_close']=round((datetime.datetime.fromisoformat(summary['completed_utc'])-datetime.datetime.fromisoformat(summary['stage_evidence_timestamps_utc']['CREATE_FOUR_PAGES.json'])).total_seconds()/60,2)
summary['limits_preserved']='No further native edits/export after two drawing versions; graphic flaws disclosed. Native connection is accepted only as logical verification; bench/manufacturing remain blocked.'
(p/'EXECUTION_SUMMARY.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
files=[]
for q in sorted(p.rglob('*')):
 if q.is_file()and q.name not in ['PACKAGE_HASHES.json','PRO_FIRST_BUILD_RECEIPT.txt','PRO_DELIVERY.json','PRO_RECEIPT_PARTS.json']and not q.name.startswith('PRO_PART_'):
  files.append({'relative_path':str(q.relative_to(p)),'bytes':q.stat().st_size,'sha256':sha(q)})
(p/'PACKAGE_HASHES.json').write_text(json.dumps({'root':str(p),'files':files},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
intro='''CIRCUIT-FIRST-BUILD-INTEGRATED-SCHEMATIC-HOLD-RECEIPT-20261001-01
仅项目 SCIENCE_ADK5556_4X4_DAQ_REPLICA；对应你已授权并完成的 CIRCUIT-PRO-FIRST-BUILD-INTEGRATED-DESIGN-GATES-20261001-01，执行端用户全部普通技术连续授权及直接报告有效。不是旧Decision29/SGM调试。
现正式提交唯一包 SCIENCE_ADK5556_4X4_FIRST_BUILD_DETAILED_DESIGN_AND_NATIVE_SCHEMATIC_V1 的完整必要审查材料。Pro不能读取本地，下面直接正文。仅等完整多段END后统一裁定；中途仅ACK，不发布新任务。无需用户重新确认模型或重复供应电路参数。
事实与结果：现成原生库7核心类型/22独立器件身份，120核心物理针号与厂家/封装焊盘对应；78实际器件，4页新工程，258连接针/28NC/63网。初次自动连接脚本方向错误被真实网表发现，未冒称PASS；修复后preclose和coldreopen两个实际File网表均258/258及完整网络成员/器件集合/真实封装名称PASS，5次save=true，独立close/reopen，磁盘字节hash不变。前后两份真实网表字节不同，完整组件key/value多重集合完全相同，仅字段顺序变化；不冒称字节相等。
81实际线性DC组(324选行状态/1296读数)，8物理自检；固定校准后9阵列模式下每线0.1Ω最大误差0.0797833%，每线1Ω0.791526%超0.20%线阻分配。不是严格最坏或实物性能保证。24项静态/定性故障审查，不是24暂态运行。官方PSpice/TINA模型2包已保全但未运行；本机未确认可用模拟器，不安装第三方，不转回长API排错。AC/正常暂态/故障暂态均0，PM/GM/300µs/噪声/温度/60s热/供电时序未通过。
保持 DYNAMIC_VALIDATION_HOLD / FAULT_PROTECTION_HOLD / REFERENCE_CAPACITANCE_HOLD / ERC_DETAIL_HOLD / DRAWING_LAYOUT_HOLD / BENCH_NOT_RELEASED。native DRC实际只返回warn10 count，无正文，不称DRC clean。最终4页真实PDF已全部render看过，仍有IC网名与针号/位号重叠、左缘端口碰图框；export2/2耗尽而停止，不隐藏排版缺陷或擅增预算。图纸只供审查，不称出版/制造完成。
本轮没有旧master打开/复制/写入、自定义库建器件、PCB、制造、采购、Git或直接系统/数据库/cache/profile/activation变更。两自有sessions均official closed，无pending/timeout。官方create在配置项目目录生成新工程，再字节原样拷贝交付目录；不改APP_PROJECT_DIR。
希望裁定：接受已证明的原生逻辑连通性/保存持久化/有边界DC结果并维持以上HOLD；集中给唯一下一任务、输入、交付物、通过/停止门、预算。优先闭合故障/动态工程门，同时明确完整DRC正文和端口文字排版后续额度。不得把新预算伪装成PCB或制造许可；切核心系列/E/Rf等需明确裁定。
''' 
names=['PRO_INTEGRATED_DESIGN_GATES_FULL.txt','PLAN.md','P1_COMPLETION.md','BASELINE_AND_CHANGELOG.md','EXACT_BOM_AND_PINMAP.csv','DETAILED_CIRCUIT_AND_PROTECTION.md','ERROR_CALIBRATION_AND_TIMING.md','VALIDATION_REPORT.md','VALIDATION_SUMMARY.json','DC_CASES.csv','FAULT_CASES.json','SPI_EVENT_PLAN.json','P1_CORE_PINMAP_CHECKS.json','PLACED_POST_REOPEN_INSTANCE_SNAPSHOT.json','PLANNED_NATIVE_DESIGN.json','POST_REOPEN_CONNECTIVITY_AUDIT.json','PERSISTENCE_COMPARISON.json','REPAIRED_PRE_CLOSE_CAPTURE.net','POST_REOPEN_CAPTURE_EXPORT_ACTUAL.net','ERC_REPORT.md','DRAWING_VISUAL_QA.json','NATIVE_GENERATION_CORRECTION.md','EXECUTION_SUMMARY.json','SOURCE_ACQUISITION.json','SOURCE_RETRY.json','SUPPORT_SOURCE_ACQUISITION.json','verify_core_pinmap.py','validate_electrical.py','audit_actual_netlist.py','prepare_native_scripts.py','prepare_repair.py','capture_and_export.js','finalize_package.py','build_pro_receipt.py','PACKAGE_HASHES.json']
body=intro+'\n本地根目录：'+str(p)+'\n'
for name in names:
 f=p/name;b=f.read_bytes();t=b.decode('utf-8-sig')
 if name.endswith('.json'):t=json.dumps(json.loads(t),ensure_ascii=False,separators=(',',':'))
 body+='\n\n===== FULL '+name+' | bytes '+str(len(b))+' | SHA256 '+sha(f)+' | '+str(f)+' =====\n'+t+'\n===== END '+name+' =====\n'
body+='\n\n未直接粘贴二进制PDF/eprj2/elibz2/厂家PDF和原始每页大source/API/b64。完整hash清单包含它们，但不宣称Pro读取这些本地文件；审查所需真实实际pin/NC/封装/原始两份完整Protel2/全部算法和输入/表格已经上文直接正文。DC_RESULTS细节本地保留，完整求解代码、输入模式及81行CSV可复算，非以路径当结果。\nEND-OF-COMPLETE-FIRST-BUILD-INTEGRATED-SCHEMATIC-HOLD-RECEIPT\n'
out=p/'PRO_FIRST_BUILD_RECEIPT.txt';out.write_text(body,encoding='utf-8')
size=43000;chunks=[body[i:i+size]for i in range(0,len(body),size)];deliver=[]
for i,ch in enumerate(chunks,1):
 text=f'CIRCUIT-FIRST-BUILD-INTEGRATED-SCHEMATIC-HOLD-RECEIPT-20261001-01\nPART {i}/{len(chunks)}。严格只处理本项目。这是直接正文的一段，跨段截断连续拼接；前段只ACK，最后END后给完整统一裁定。禁止拿旧回复当新裁定。\n'+ch
 if i==len(chunks):text+='\nFINAL-PART-END-OF-COMPLETE-FIRST-BUILD-INTEGRATED-SCHEMATIC-HOLD-RECEIPT'
 f=p/f'PRO_PART_{i:02}.txt';f.write_text(text,encoding='utf-8');deliver.append({'part':i,'path':str(f),'chars':len(text),'sha256':sha(f)})
record={'marker':'CIRCUIT-FIRST-BUILD-INTEGRATED-SCHEMATIC-HOLD-RECEIPT-20261001-01','full_chars':len(body),'full_sha256':sha(out),'parts':deliver,'threadId':'69dd2e6e-e580-83ea-a898-0b9abcf3c21a'}
(p/'PRO_RECEIPT_PARTS.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record))
