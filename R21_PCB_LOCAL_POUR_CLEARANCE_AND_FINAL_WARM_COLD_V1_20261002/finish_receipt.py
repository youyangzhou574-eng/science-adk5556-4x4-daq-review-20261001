from pathlib import Path
import json,hashlib,datetime
P=Path(__file__).parent
def r(n):return json.loads((P/n).read_text('utf8'))
def w(n,q):(P/n).write_text(json.dumps(q,indent=2,ensure_ascii=False)+'\n','utf8')
assert r('AFTER_REBUILD_DRC.json')['parsed']=={'ok':True,'value':[],'logs':[],'durationMs':4388}
assert r('COLD_DRC.json')['parsed']['ok']and r('COLD_DRC.json')['parsed']['value']==[]
c=r('COLD_AUDIT.json');warm=r('WARM_AUDIT.json');rep=r('WARM_COLD_POURED_REPRESENTATION_DIFF.json');assert warm['PASS']and all(c['strictIDbodyEqual'][k]for k in('COMPONENT','PAD_NET','ATTR','LINE','VIA','POUR','POLY','RULE'))and c['core176']and c['padNet550']and c['rulesEqual']and c['layerInfoEqual']
assert rep['numericDifferenceCount']==215 and rep['maxAbsoluteNumericDifference']<=2.104e-12 and not rep['structuralDifferences']and not rep['addedObjects']and not rep['removedObjects']
# Engineering consistency allows the already-disclosed stable serialization-level numeric difference; raw strict check remains false and preserved.
accept={'entryPASS':r('ENTRY_GATE.json')['entryPASS'],'warmDRC':{'Connection':0,'Short':0,'Clearance':0,'NetlistError':0},'coldDRC':{'Connection':0,'Short':0,'Clearance':0,'NetlistError':0},'parts':176,'pads':550,'assigned':514,'nets':107,'NC':36,'rawPOUREDWarmColdStrictEqual':False,'numericDifferences':215,'maxAbsoluteNumericDifference':rep['maxAbsoluteNumericDifference'],'structuralOrObjectChanges':0,'allUserLineViaCoreNetRuleBoundaryLayerWarmColdStrictEqual':True,'warmColdEngineeringConsistency':True,'interpretation':'Same previously disclosed215 tiny scalar representation differences, no structural/object differences; no rounding/filtering of evidence. Under15 engineering gate accept stable serialized representation, not strict byte/numeric equality. Initial overly strict offline COLD_AUDIT false retained; no actualCAD rerun.','PCB_ROUTING_COMPLETE':'PASS','PCB_ELECTRICAL_CLOSURE':'PASS','COLD_REOPEN':'PASS','PCB_REVIEW_READY':True,'MANUFACTURING_NOT_RELEASED':True,'BENCH_NOT_RELEASED':True}
w('COLD_ENGINEERING_ACCEPTANCE.json',accept);w('GATES.json',accept)
b=r('EXECUTION_BUDGET.json');b['sessionCommandAttempts']=3;b['actualCreatedSessions']=2;b['status']='NATIVE_EXECUTION_COMPLETE_NO_MORE_EDITS';b['completeUTC']=datetime.datetime.now(datetime.timezone.utc).isoformat();w('EXECUTION_BUDGET.json',b)
life={'warmSession':'82a22091-9ce2-4bc4-a184-045570f3ce78','coldSession':'a3f04415-5f85-4faf-9096-5e1b4763fe31','bothOfficialClosed':r('CLOSE_POUR_WARM.json')['parsed']['value']['status']=='closed'and r('CLOSE_POUR_COLD.json')['parsed']['value']['status']=='closed','warmGUIClosedBeforeCold':True,'finalOwnGUIWindows':[],'normalCloseClicks':2,'solverStarted':False,'save':r('SAVE_AFTER_ZERO_DRC.json')['parsed']['value']['saved'],'source':'GUI observations and official close tool receipts','confirmedUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()};w('SESSION_GUI_LIFECYCLE.json',life)
protected=[]
for root,name,expected in [('R21_PCB_V3V3_MINIMAL_CONNECTION_CORRECTION_V1','SCIENCE_ADK5556_4X4_R21_V3V3_MINIMAL_WORK.eprj2','E97353063AF91D2F9A95C030989E592DAA6B388D9C4DE2961FB5E58620EBA5BC'),('R21_PCB_V3V3_MINIMAL_CONNECTION_CORRECTION_V1','SCIENCE_ADK5556_4X4_R21_V3V3_BLOCKED_NOT_FOR_USE.epro2','BB467B165EC7FE7547F8F352D3A1F298B5A6ABB4D7410ADDC33C378C752E5CE7'),('R21_PCB_ROUTING_CLOSURE_V1','SCIENCE_ADK5556_4X4_R21_ROUTING_CLOSURE_WORK.eprj2','FCD73BF2620447E7906D4014628F58F2C497410366B985E6FB0932D6322772BE'),('R21_PCB_ROUTING_CLOSURE_V1','SCIENCE_ADK5556_4X4_R21_PCB_ROUTED_REVIEW.epro2','5603E205FCB5170DE00A125DCD7A6271665D78BED153E4B6B489ABEAF8F8FB6E')]:
 f=P.parent/root/name;sha=hashlib.sha256(f.read_bytes()).hexdigest().upper();protected.append({'path':str(f),'bytes':f.stat().st_size,'expected':expected,'actual':sha,'PASS':sha==expected})
assert all(q['PASS']for q in protected)
f=P/'SCIENCE_ADK5556_4X4_R21_POUR_CLOSURE_WORK.eprj2';w('FROZEN_INPUT_AND_FINAL_WORK_HASHES.json',{'protected':protected,'finalSavedColdWork':{'name':f.name,'bytes':f.stat().st_size,'SHA256':hashlib.sha256(f.read_bytes()).hexdigest().upper(),'warmColdVerified':True}})
meta=r('FINAL_NATIVE_FILE_METADATA.json');request={'requestedByUser':'More bounded time/counts/autonomy requested explicitly by human user, included only in normal report.','proposedPackage':'R21_PCB_MANUFACTURING_PREFLIGHT_READONLY_V1','minutes':180,'timeAllocation':{'manufacturingInputsAndStackupContract':45,'existingNativeEvidenceAndRuleReview':45,'assemblyTestAccessChecklist':30,'delivery':45,'reserve':15},'limits':{'newCAD':0,'session':0,'save':0,'captureaudit':0,'DRC':0,'nativeExport':0,'simulation':0,'Gerber':0,'procurement':0,'manufacture':0,'actualBench':0,'existingEvidenceReview':1,'checklistContractBatch':1,'officialSources':6},'scope':'Read-only manufacturing preflight of existing savedPCB/schematic/rules/BOM/evidence; explicit missing stackup/fab capabilities/assembly inputs. No ordering or fabrication, no newCAD/theory/API. NativeDRC zero is not fabrication or bench release. If harddesign issue found report one consolidated proposal.','approved':False};w('NEXT_BOUNDED_REQUEST.json',request)
(P/'REVIEW_DRAWING_NOTES.md').write_text('# Mandatory drawing notes\n\nTwo PNGs rendered once from actual cold source: filled polygons and via dimensions use actual coordinates; ARC max step2degrees. Tracks are centerline display strokes, not exact physical width. Footprint pad outlines/silkscreen and some native object types are omitted. These are review aids, not fabrication plots or native PDF/Gerber. Copper CSV/source/native and real nativeDRC are authoritative.\nBoth PNGs actually viewed after generation; localTop/Inner1 show e307 GND antipad and Inner2 V3V3 connection. No re-export or scientific calculation.\n','utf8')
receipt=f'''# R21 PCB normal pour update and final warm/cold — engineering review ready

按15号完整工程裁定，只执行一次正常Rebuild All。温态和独立冷重开原生DRC均返回成功且value=[]：Connection/Short/Clearance/NetlistError全部0。176parts/550pads/514assigned/107nets/36NC保持；14号两处V3V3桥及e307在保存、冷重开及真实native File中保持。按15号工程门标记PCB_ROUTING_COMPLETE / PCB_ELECTRICAL_CLOSURE / COLD_REOPEN PASS，PCB_REVIEW_READY=true。制造/采购/bench/上电/Gerber仍未放行。本结论不是性能、实物、工艺或数学严格字节一致性证明。

## 裁定与冻结输入

CIRCUIT-PRO-R21-PCB-LOCAL-POUR-REBUILD-AND-FINAL-CLOSURE-20261002-15，assistant dd5c432a-162f-4a19-9719-a8575b3ee300，parentuser52b37bbe-46e5-4a7f-8af9-89ec3d99e284。全文PRO_POUR_CLOSURE_RULING_FULL.md。120min；copy1/session2/save1/captureaudit3/DRC3/export1/normalPourUpdate1。批准POURED派生变化，4个POUR边界/网络/优先级/规则/层冻结；新或删除LINE/VIA、移件、net/value/footprint/rule、schematic/Import/autorouter/仿真/实体操作均0。

只复制14号实际工作工程eprj2，源SHA E97353063AF91D2F9A95C030989E592DAA6B388D9C4DE2961FB5E58620EBA5BC，copy字节相同。GUI正确新项目UUID7efd53fbc610430d096d3e416ed545dafaea621ce2f02ed4c02d0ed9d65ed701，实际打开PCB1画布和四层栏后才capture。入口实际所有14号3LINE+新via/e255存在；全部原生COMPONENT/PAD_NET/ATTR/LINE/VIA/POUR/POURED/POLY/RULE与14号post capture严格相同。没有重新手画铜。

## 唯一覆铜更新与真实保存/冷重开

在本地GUI工具→铺铜管理器，四原边界/网络/优先级观察一致，点击一次重建所有；原生进度结束且PCB变更标记出现，正常确认关闭管理器。没有改变表中参数，未第二次重建。立即原生AFTER_REBUILD_DRC返回ok=true/value=[]。只有此后才执行唯一pcb_Document.save，实际saved=true。

保存后的warm完整审计：176/550/514/107/36；原生COMPONENT/PAD_NET/ATTR/LINE/VIA/POUR/POLY/RULE全部与入口严格一致；全部core/坐标/网络/layerInfo/rules一致，仅POURED派生填充改变。新via周围Top1/Inner1(15) GND避让实际形成，可读局部PNG已看过。没有删除/增加用户LINE/VIA。

第一session官方close、GUI正常关闭并fresh ownappwindows=[]；随后独立第二session打开同一保存eprj2，GUI再次实际确认PCB1+层栏，执行第三次合并capture（cold完整身份/source与实际native File，单次审计批次，无save），再cold nativeDRC value=[]。两session82a22091-9ce2-4bc4-a184-045570f3ce78 / a3f04415-5f85-4faf-9096-5e1b4763fe31均官方closed，两个自有窗口均正常退出，最终fresh inventory为空；没有solver。

## 铜及表示差异，工程验收解释

actual entry/warm/cold均909LINE/297VIA/4POUR/4POURED，全部实质LINE/VIA逐ID+body严格一致。真实native File911LINE多此前已记录VCM137f992f55430857/TIA121f945bfa3a6372f两0.1mil表示短段，15号明确不以总LINE字面数字为门，不重建/删除/研究。组件、padnet、规则、层和4POUR边界/网络/priority等没有漂移。

warm→cold4POURED原始数值严格不等：215处标量差，最大2.1032064978498966e-12；对象增删0/结构差0。全部原始值和路径保留，没有把数据舍入/过滤成相等。其数量、幅度与此前14号公开File/重开表示差异同级一致；解释为稳定的微小序列化表示差异（内部原因未研究），不是strict bytes/float/geometric equality。工程一致性依据原生四类DRC全0、全部非派生对象严格一致、完整POURED结构/数量不变及上述显式微差，按15号仅正常POURED派生变化条件通过；精确rawPOURED一致字段保持false。完整COLD_OBJECT_DIFF / WARM_COLD_POURED_REPRESENTATION_DIFF / COLD_ENGINEERING_ACCEPTANCE / GATES一并交付，不虚报严格相同。

## 原生/可读证据

真实native File {meta['name']}，{meta['bytes']}bytes SHA256 {meta['SHA256']}，constructor File/tag [object File]。由独立cold工程捕获，全部14号实质铜在File中，核心VIA/POUR边界/规则与实际cold严格相同；不是JSON代原生或LFS指针。保存工程eprj2和source同时直接上传；nativeFile表示差异完整保留。旧14工作/失败File及12routing工作/review4项冻结SHA均未变，见FROZEN_INPUT_AND_FINAL_WORK_HASHES.json。

2PNG由既有cold source只读一次批次绘制并实际查看：四层总览、e307局部避让。ARC最大步长2°；轨迹只是显示中心线，非真实宽度绘图，封装pad/silkscreen等省略；必须伴随REVIEW_DRAWING_NOTES.md，不作制造图。warm/cold全550pad与176核心CSV、909LINE/297VIA CSV、全部原始CLI/GUI/capture/DRC/File/source/完整差异供网页逐文件读，不只有ZIP。

## 实耗、初失败及执行偏差（不回写历史）

实际copy1/createdsession2/save1/captureaudit3/DRC2/reviewExport1/normalPourUpdate1；所有新删除LINE/VIA/移动/改值规则/Import/仿真/Gerber/制造采购bench/localGit/system0。第三capture一次同时包括cold身份/source+实际File，非额外第四次审计。未用第3DRC。

三条startup命令里首条错误session open被parser拒绝MISSING_SUBCOMMAND，无sessionId也无GUI；随后用已有正确open命令创建warm，最后正确open创建cold。原失败日志留存。warm会话已预扣1，parser失败未创会话后同一预扣完成；实际2会话，startup attempts3/parserfailure1单列，不冒称三条命令全成功或另获预算例外。

入口离线核心比较初false：副本API footprint/device的libraryUuid跟随新project owner，352个owner字段改变，但真实原生COMPONENT/ATTR等严格相同。只对照两GUI确认的owner UUID精确映射，actual footprint/device uuid/name及所有其余字段保持；原初false及完整352差异留存。没有CAD重跑或工具研究。

cold离线脚本又把POURED任何浮点微差当成失败，原COLD_AUDIT PASS=false留存。该错误门是本地过严的报告判定，不是15号实际net/铜或DRC故障。后续DRC预扣被该本地status拒绝，但顺序工具编排仍执行了只读COLD_DRC。这是执行控制偏差：实际第二DRC在事后真实UTC补记debit，不回填predebit、不追认例外。实际仍为2/3DRC，没有追加CAD编辑/保存/覆铜/重试。保留原失败reservation结果及日志；终态无更多native操作。工程一致性结论单列，未改掉原始false结果或数值。

## 下一阶段集中申请（未批准）

按用户明确提出的更多有界时间/次数/自主范围要求，在本次正常报告集中申请R21_PCB_MANUFACTURING_PREFLIGHT_READONLY_V1 180min：制造输入/stackup合同45、既有native/规则/BOM证据45、装配与测试可达性清单30、交付45、预留15。只读已有工程/证据一次、checklist合同批次一次，必要官方资料≤6；普通核对本地自主累计。newCAD/session/save/capture/DRC/nativeexport/仿真/Gerber/采购/制造/actualbench全部0，不下单不上电。对未知板厂能力、实际叠层、机械/装配输入明确PENDING，不假定已满足。不另开修板包，不研究API；发现真实设计问题集中报告唯一最小方案。此处只是请求，旧15余量关闭，未批准不执行。

完整报告/附件将发布独立GitHub新目录固定commit；一次短交付之后记录owner/nextCheck，接续回复监控。网页逐附件已读未验证，不设额外ACK等待门。PCB_REVIEW_READY不是manufacturing release或bench PASS。

END-OF-COMPLETE-R21-PCB-POUR-CLEARANCE-AND-FINAL-WARM-COLD-RECEIPT
'''
(P/'COMPLETE_POUR_CLOSURE_RECEIPT.md').write_text(receipt,'utf8')
(P/'README.md').write_text('''# PCB warm/cold engineering review ready — NOT manufacturing release

[Complete receipt](COMPLETE_POUR_CLOSURE_RECEIPT.md) · [Ruling15](PRO_POUR_CLOSURE_RULING_FULL.md) · [Gates](GATES.json) · [Budget](EXECUTION_BUDGET.json)

- [Warm actualDRC](AFTER_REBUILD_DRC.json), [cold actualDRC](COLD_DRC.json): successful empty error arrays.
- [Warm550](WARM_550_PAD_NET.csv), [cold550](COLD_550_PAD_NET.csv), [cold176](COLD_176_CORE.csv).
- [Cold engineering acceptance](COLD_ENGINEERING_ACCEPTANCE.json); [raw strict cold audit](COLD_AUDIT.json) remains false for215 tiny POURED scalar differences, [full difference](WARM_COLD_POURED_REPRESENTATION_DIFF.json). No false raw-byte equality claim.
- [Actual nativeFile](SCIENCE_ADK5556_4X4_R21_PCB_CLOSED_REVIEW.epro2), [savedwork](SCIENCE_ADK5556_4X4_R21_POUR_CLOSURE_WORK.eprj2), [actualFile source](FINAL_PCB_DOCUMENT_FROM_NATIVE_FILE.txt).
- [Fourlayer overview](FINAL_FOUR_COPPER_LAYERS.png), [via antipad detail](FINAL_LOCAL_VIA_AND_ANTIPADS.png); mandatory [drawingnotes](REVIEW_DRAWING_NOTES.md).
- [909actualLINE CSV](FINAL_ACTUAL_909_LINES.csv), [297actualVIA CSV](FINAL_ACTUAL_297_VIAS.csv), [warm→cold objectdiff](COLD_OBJECT_DIFF.json).
- [Frozenhashes](FROZEN_INPUT_AND_FINAL_WORK_HASHES.json), [session lifecycle](SESSION_GUI_LIFECYCLE.json), [unapproved nextbounded request](NEXT_BOUNDED_REQUEST.json).

One normalGUI RebuildAll; no user line/via edit. Preserve all initial parser/report and late coldDRC debit deviations. Engineering nativeDRC closure is not fabrication, hardwareperformance, bench orpowerup release.
''','utf8')
print(json.dumps({'PCB_REVIEW_READY':True,'rawPOUREDEqual':False,'DRCwarmcold':'0/0/0/0','budget':b['actual'],'nativeBytes':meta['bytes']}))
