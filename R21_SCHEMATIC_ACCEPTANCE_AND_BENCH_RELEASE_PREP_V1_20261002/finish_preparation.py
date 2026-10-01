from pathlib import Path
import json,datetime,hashlib,csv
P=Path(__file__).resolve().parent;B=P.parent/'R21_FINAL_INTERFACE_ANNOTATION_AND_BENCH_READINESS_V1';D=P.parent/'GITHUB_FINAL_INTERFACE_DELIVERY_20261002'
def write(n,s): (P/n).write_text(s.strip()+'\n','utf8')
def dump(n,x): write(n,json.dumps(x,ensure_ascii=False,indent=2))
now=datetime.datetime.now(datetime.timezone.utc).isoformat();q=json.loads((P/'EXECUTION_BUDGET.json').read_text('utf8'));q['phaseHistory'].append({'phase':q['phase'],'startedUTC':q['phaseStartedUTC'],'endedUTC':now});q['phase']='P2_release_checklist';q['phaseStartedUTC']=now;q['overallHandlingStartedUTC']='2026-10-01T19:56:21.050+00:00';q['clockNote']='First builder start retained; conservative overall handling includes triggering heartbeat/ruling read before document builder.';dump('EXECUTION_BUDGET.json',q)
rows=json.loads((P/'ACCEPTED_BASELINE_SHA.json').read_text('utf8'))['records'];checks=[]
for row in rows:
 data=Path(row['path']).read_bytes();checks.append({'path':row['baseline_relative_path'],'sha256':hashlib.sha256(data).hexdigest().upper(),'bytes':len(data),'unchanged':hashlib.sha256(data).hexdigest().upper()==row['sha256'] and len(data)==row['bytes']})
assert all(x['unchanged'] for x in checks);dump('ACCEPTED_BASELINE_FINAL_SHA_PASS.json',checks)
ts=list(csv.DictReader((P/'BENCH_TEST_MATRIX.csv').open(encoding='utf8'))); ns=list(csv.DictReader((P/'EXPECTED_NODE_RANGES.csv').open(encoding='utf8')))
assert len(ts)==57 and len(ns)==46 and all(x['execution_status']=='NOT_EXECUTED_NOT_RELEASED' for x in ts)
assert next(x for x in ts if x['case_id']=='P01')['R0C0_ohm']==''
assert next(x for x in ts if x['case_id']=='V1000')['role']=='calibration_check_only'
assert all(x['acceptance_threshold_status']=='PENDING_PHASE1_RELEASE' and x['hard_off_threshold_status']=='PENDING_PHASE1_RELEASE' for x in ns)
assert not any(x.get('status')=='PASS' for x in ts)
dump('PREPARATION_CONTRACT_CHECK.json',{'matrixRows':57,'nodeRows':46,'caseIDsUnique':len({x['case_id'] for x in ts})==57,'no_arrayNotZeroOhm':True,'calibrationPointNotIndependentValidation':True,'allRowsUnexecuted':True,'noInventedPhase1Thresholds':True,'all13BaselineSHAsUnchanged':True,'benchOperations':0,'newScientificTests':0,'staticContractChecksOnly':True})
dump('TABLE_VISUAL_REVIEW.json',{'bothTablePreviewsActuallyViewed':True,'nodeHeaderWidthsAdjusted':True,'calibrationRoleShortenedNoClipping':True,'previewScope':'opening ranges only; full CSV typed values reconciled to all original JSON rows','staticTablesNotMeasurements':True,'xlsxNotRequestedNotCreated':True})
old=json.loads((D/'COMMUNICATION_STATE.json').read_text('utf8'));old.update(status='FULL_11_RULING_CONSUMED_PREPARATION_EXECUTING',assistantRulingId='0748e84e-c249-42c1-a7d0-feca458ee2b2',newPackageRoot=str(P),monitorStatus='automation_deleted_after_full11');(D/'COMMUNICATION_STATE.json').write_text(json.dumps(old,ensure_ascii=False,indent=2)+'\n','utf8')
write('COMPLETE_BENCH_PREP_RECEIPT.md','''# R2.1原理图正式接收与受控首次上电准备回执

SCIENCE_ADK5556_4X4_R21_SCHEMATIC_ACCEPTANCE_AND_BENCH_RELEASE_PREP_V1，11号裁定0748e84e-c249-42c1-a7d0-feca458ee2b2，parent5744965e-89cb-4424-86ba-6f6a07a37b32。完整原文PRO_ACCEPTANCE_RULING_FULL.md。本包只读工程资料准备完成，实际上电/实体测试未执行。

## 正式接收

Pro独立复看固定commit fbb7c0ed5f322f078583fadbdb353efe835e4c01后接受主采集拓扑、J3/J4独立sense、176器件/514of514引脚/107网/36NC及独立冷重开。SCHEMATIC_ELECTRICAL_BASELINE_ACCEPTED。epro2 SHA2821A51AFCF9BB474D895B53AE6C514A9B4B637CC3016054356FA7E43F3A97E9。原生/PDF及13项配套证据只读重新核SHA，完包全部不变；没有复制/打开/编辑/保存/捕获/导出原生。

旧注释、PDF四端口网名缺字属于文档质量HOLD；PDF主体PASS with companion，独立发布HOLD。强制companion MD/CSV/PNG与annotation addendum及实际CSV属于接受图纸的组成部分，固定链接见ACCEPTED_SCHEMATIC_BASELINE.md。不再修EDA或研究setter、ERCcount、理论证明。接受不表示已有实物样机、不表示实物性能通过。

## 可执行合同结构

六项要求全部交付：FIRST_POWERUP_PRECHECK.md，BENCH_TEST_MATRIX.csv，EXPECTED_NODE_RANGES.csv，BENCH_STOP_CRITERIA.md，CALIBRATION_AND_ACCEPTANCE.md，TIMING_CAPTURE_PLAN.md；另有PHASE1_RELEASE_CHECKLIST.md/PHASE1_RELEASE_INPUTS.json、ACTUAL_PROBE_MAP.md/PROBE_NET_MEMBERS.json、接收矩阵/来源与冻结SHA。

测试矩阵57个未来工况：空载Phase1；1k/6.8k两校准工况；1k校准后检查与独立3.3k/7k/可用2.2k/4.7k；棋盘及行/列交替；1k和3.3k两基点各16单点+4行+全阵列正10%；7k→6.3k正常负10%；0.8k/8k及7k→7.7k仅另列排除guardband。每行16独立R00..R33值；空载为缺席空字段，不能解释为0Ω短路。计划完整帧数和工况不等于批准的实验次数，全部NOT_EXECUTED_NOT_RELEASED。

节点表46行：输入/5V/3V3/REF2.5/VCM/VEXC、ADC内部参考、ROWblank/active、TIAblank及旧三标准理想TIA/ADC、PGOOD/正常reset输入。V5=5、V3V3=3.3、VCM=2.5、VEXC=2.25只是名义值。所引1k/3.3k/7k输出逐项来自08既有理想DC CSV，未重新求解；真实线阻/失调/钳位/ADCINL/动态/温区不由理想值保证。ADC_REFIO/REFCAP≈4.096仅内部参考被启用时，reset/powerdown下状态需在release定义；不是REF3025的2.5V。所有供电合格窗和硬断电阈值PENDING_PHASE1_RELEASE，不把设计值、绝对最大值或旧理想margin当新放行门。

实际探点按接受网表：J1.1输入/J1.2地、R_VCM_ISO.2/R_VEX_ISO.2、J2row/col、TIA tap/driver分开、C_ADCi.1到U5.16/.18/.21/.23。PGOOD/MCU NRST为U7.6，J3.5通过实际1k到PGOOD；未误用旧G17/G07/47k候选。sense不能供电、SWD4.99k低速起步要求保持。映射只指元件pin，不声称已有实体test pad。

## 验收口径和阶段隔离

1k/6.8k电导两点拟合口径A/B冻结，以active8−adjacentblank8差分D形成读数；未计算新校准系数/未写固件。独立验证按每工况每单元绝对均值误差<=1%，报告最大/平均绝对误差和不确定度，不能signed mean抵消。重复性计划1000完整连续帧、sampleSD(N−1)/Rref<=0.2%，拒绝帧保留，不人为删离群值。10%单点/行/全阵列保留16点及邻居；7k+10%不算正常PASS。

时序沿用8状态/300us等待、每状态900us采集+300us等待=1200us、8状态9600us+400us、288传输32dummy256有效、48clk@4MHz/mode1既有合同。300us残余100uV目标需真实探头/分辨率；接收时刻不代采集时刻；100fps/WCET必须真实SPI/DMA/ISR/帧记录。旧离线GREEN和设计预算不是实体证据。正常20–30C reset仅后续OD/OC及HiZ，不混±故障/反灌/热测试。

首次上电只拟议限流电源+空载板：供电、参考、PGOOD/NRST、电流。标准阵列、校准、10%变化、300us/100fps和reset动作分后续阶段，不自动升级。异常断电、地/极性/接线错、持续限流/轨塌陷、增长振荡、热/烟/异味等停止口径明确；实际数值等待release，不带电修线或自行增大限流重复。

## 待实体输入与唯一下一次裁定

样机ID/装配/匹配SHA、人员、设备型号/校准/探头/地方案、既有blank控制固件或GPIO状态、ADCreset/powerdown状态未知。已在本聊天向用户询问现有样机与仪器，未回复不能假定存在。PCB/采购/制造0，不为缺样机扩权造板。PHASE1_RELEASE_INPUTS.json明确null字段，不用0或默认设备填平。

下一次请Pro仅决定受控首次上电Phase1的方案/放行条件，补电源设定/限流、仪器连接/先测节点、正常阈值、异常立即断电阈值、建立时限、允许次数/时长；实际执行仍要匹配用户bench授权、实体/操作人及完整输入。缺实体条件时接受准备资料并列出具体输入即可，不返回EDA/理论修复。

按用户明确要求更多有界时间/次数/自主范围，集中请求下一阶段180min：Phase1输入核对30、仅在实体与授权齐备后受控空载检查45、读数/异常审阅45、交付60。集中拟议上限3次正常空载供电、每次<=15s、累计<=45s（不是60s热应力试验），仅供Pro按实体条件评估；任一异常第一次即停、不自动重试。最终允许次数/时长、限流和硬断电门必须由release具体裁定后登记；不自定安全数值，也不把这个申请当执行批准。若实体输入未齐，限定只读等待与合同填写，actualbench仍0。所有EDA/仿真/新协议/PCB/采购/制造/强故障0；不扩平台额度或系统权限。不得为了更多次数越过异常一次即停的条件。

## 实耗与完整性

新240min包，45/75/60/60阶段；旧10剩余关闭。实际EDAedit/nativecopy/session/save/capture/PDF/ERC/仿真/MIMO/descriptor/新协议/PCB/采购/制造/actualbench全0。仅只读材料、静态文件/CSV和公开交付。CSV用已存在bundledArtifactTool typedvalues构建/逐行核对，recalculate为表格处理，不是科学分析；两opening previews实际查看，完整57/46行值与源JSON完全一致，没有额外xlsx。CSV空值/校准点role与guardband均明确。

最初静态读取CSV BOM导致KeyError net，改utf-8-sig读已有文件，原文件未改；失败记录保留，原起始UTC保留。无EDA/solver/新协议运行，不把文档构造失败扩成工具研究。ACCEPTED_BASELINE_FINAL_SHA_PASS.json全部13源未变。

单次fresh-context终审结果见FINAL_REVIEW.md。完整公开GitHub新目录固定commit一次告知配对Pro，同回合建立新owner/nextCheck/monitor，报错留账、不重复送达正文。原生文件继续引用已接受固定版本，不新增native副本，不只交本地路径。

END-OF-COMPLETE-R21-SCHEMATIC-ACCEPTANCE-AND-BENCH-RELEASE-PREP-RECEIPT
''')
write('README.md','''# R2.1 accepted schematic与受控首次上电准备

[完整回执](COMPLETE_BENCH_PREP_RECEIPT.md) · [已接受固定基线](ACCEPTED_SCHEMATIC_BASELINE.md) · [接收矩阵](ACCEPTANCE_MATRIX.md) · [Phase1 release输入](PHASE1_RELEASE_CHECKLIST.md)

原理图电气基线已正式接受：176parts/514of514/107nets/36NC、主采集和独立sense/cold PASS。旧备注/四PDF网名缺字只保留文档质量HOLD，强制companions随图纸使用，不再修改EDA。

**准备包完成不等于上电放行。样机/仪器/人员及限流/硬断电数值仍未填写，BENCH_NOT_RELEASED，PCB未开始。**

六项操作资料：FIRST_POWERUP_PRECHECK.md；57工况BENCH_TEST_MATRIX.csv；46行EXPECTED_NODE_RANGES.csv（nominal/oldideal不作放行门）；BENCH_STOP_CRITERIA.md；CALIBRATION_AND_ACCEPTANCE.md；TIMING_CAPTURE_PLAN.md。

PHASE1_RELEASE_INPUTS.json是待填写的release输入。实际探点/网成员、13项冻结SHA、旧理想引用、原裁定、预算、静态表格核对与终审全部保留。没有原生副本、EDA/仿真/新协议/实体测试。标准阵列与后续动态矩阵尚未获执行批准，首次上电只请求空载有界范围。

原始epro/PDF/actualnet/companion的固定GitHub链接在基线文件，源文件不重写、不另复制。manifest/完整ZIP用于此准备包文件完整性。
''')
now=datetime.datetime.now(datetime.timezone.utc).isoformat();q=json.loads((P/'EXECUTION_BUDGET.json').read_text('utf8'));q['phaseHistory'].append({'phase':q['phase'],'startedUTC':q['phaseStartedUTC'],'endedUTC':now});q['phase']='P3_delivery';q['phaseStartedUTC']=now;q['scienceAndNativeOperationsComplete']=True;dump('EXECUTION_BUDGET.json',q)
print('Read-only preparation receipt and13 frozen-source checks complete; one final review then publication')
