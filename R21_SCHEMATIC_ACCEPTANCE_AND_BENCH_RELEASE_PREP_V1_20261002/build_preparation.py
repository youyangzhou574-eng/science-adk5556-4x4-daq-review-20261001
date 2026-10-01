from pathlib import Path
import json,csv,hashlib,datetime,shutil
P=Path(__file__).resolve().parent;B=P.parent/'R21_FINAL_INTERFACE_ANNOTATION_AND_BENCH_READINESS_V1';E=P.parent/'R21_ENGINEERING_R21_NATIVE_AND_LIMITED_VALIDATION_V1'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(n,s): (P/n).write_text(s.strip()+'\n','utf8')
def dump(n,x): write(n,json.dumps(x,ensure_ascii=False,indent=2))
used={k:0 for k in ['EDA_edit','native_copy','session','save','capture','PDF','ERC','simulation','MIMO','descriptor','new_protocol','PCB','procurement','manufacturing','actual_bench']}
if not (P/'EXECUTION_BUDGET.json').exists(): dump('EXECUTION_BUDGET.json',{'package':'SCIENCE_ADK5556_4X4_R21_SCHEMATIC_ACCEPTANCE_AND_BENCH_RELEASE_PREP_V1','startedUTC':now,'approvedMinutes':240,'phases':{'P0_baseline':45,'P1_contract':75,'P2_release_checklist':60,'P3_delivery':60},'phase':'P0_baseline','phaseStartedUTC':now,'phaseHistory':[],'limits':used,'used':used,'scope':'read-only existing circuit evidence; static documents/CSV only','noUnusedPriorBudgetInherited':True,'benchReleased':False})
names=['SCIENCE_ADK5556_4X4_R21_FINAL_INTERFACE_REVIEW.epro2','SCIENCE_ADK5556_4X4_R21_FINAL_INTERFACE_REVIEW.pdf','SCIENCE_ADK5556_4X4_R21_FINAL_INTERFACE_WORK.eprj2','FINAL_COLD_CAPTURE.net','FINAL_514_PIN_NET_CHECKS.csv','FINAL_107_NETWORK_MEMBERS.csv','FINAL_36_NC.csv','FINAL_176_BOM.csv','INTERFACE_TOPOLOGY_COMPANION.md','INTERFACE_TOPOLOGY_COMPANION.csv','INTERFACE_TOPOLOGY_COMPANION.png','DRAWING_ANNOTATION_ADDENDUM.md','BENCH_VALIDATION_PLAN.md']
rows=[]
for n in names:
 data=(B/n).read_bytes(); rows.append({'path':str(B/n),'baseline_relative_path':n,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest().upper()})
dump('ACCEPTED_BASELINE_SHA.json',{'commit':'fbb7c0ed5f322f078583fadbdb353efe835e4c01','parts':176,'connectedPins':514,'nets':107,'NC':36,'records':rows,'nativeCopiedOpenedEdited':False})
core=json.loads((B/'FINAL_ARTIFACT_IDENTITY.json').read_text('utf8'))
for n in names[:3]: assert next(r for r in rows if r['baseline_relative_path']==n)['sha256']==core[n]['sha256']
write('ACCEPTED_SCHEMATIC_BASELINE.md','''# Accepted Schematic Baseline

11号裁定CIRCUIT-PRO-R21-SCHEMATIC-ACCEPT-AND-BENCH-READINESS-20261002-11，assistant0748e84e-c249-42c1-a7d0-feca458ee2b2，parentuser5744965e-89cb-4424-86ba-6f6a07a37b32正式接受电气基线。原文PRO_ACCEPTANCE_RULING_FULL.md。

固定commit **fbb7c0ed5f322f078583fadbdb353efe835e4c01**，目录R21_FINAL_INTERFACE_ANNOTATION_AND_BENCH_READINESS_V1_20261002。

[原生epro2](https://github.com/youyangzhou574-eng/science-adk5556-4x4-daq-review-20261001/blob/fbb7c0ed5f322f078583fadbdb353efe835e4c01/R21_FINAL_INTERFACE_ANNOTATION_AND_BENCH_READINESS_V1_20261002/SCIENCE_ADK5556_4X4_R21_FINAL_INTERFACE_REVIEW.epro2) SHA2821A51AFCF9BB474D895B53AE6C514A9B4B637CC3016054356FA7E43F3A97E9。

176parts/514of514connected/107nets/36NC；主采集拓扑、独立sense和actualpin-net/cold PASS。原生/PDF冻结，不复制、不打开、不保存、不导出、不改网/值。ACCEPTED_BASELINE_SHA.json记录只读新核13文件SHA，完包前再核同一集合。

强制配套：INTERFACE_TOPOLOGY_COMPANION.md/CSV/PNG、DRAWING_ANNOTATION_ADDENDUM.md、真实514针/107网/36NC/176BOM CSV。PDF主体PASS with companion；独立图纸发布HOLD。旧注释/四网名缺字仅文档质量HOLD，不再作为电路设计停止门，也不要求继续EDA/API研究。

物理性能尚未验证；BENCH_NOT_RELEASED、PCB_NOT_STARTED、容量/故障/WCET/SWD检查保留。ERC count不等于clean，也不据此回到无限原理图修改。现有芯片电气连线接受不等于已装配样机存在。
''')
write('IMPLEMENTATION_PLAN.md','''# 11号只读工程准备计划

P0：保存完整裁定，确认已消费消息，冻结13项基线SHA和接收矩阵。P1：用既有真实网络/厂家资料/旧理想DC筛查，整理工况和节点表。P2：准备预检、停机、校准/时序及Phase1 release输入。P3：单次只读终审、完整报告、GitHub固定commit一次性交付、同回合接续回复owner/monitor。

不新增科学测试/仿真/解析/协议/EDA/原生副本/bench/PCB/采购/制造；不把旧候选reset或理论证书移入当前实际接线。用现有Node/Python及bundled Artifact Tool静态制表，不安装任何软件。用户指定CSV为输出，不增加xlsx变体；CSV来自Artifact Tool表格values的标准CSV序列化。非科学表格结构检查不冒称实验。

Ruling：电源限流、具体供电合格/断电数值、允许上电次数时长、实物/仪器身份未知不虚构；以待Pro release+实体信息为字段。成本若误把名义值当断电门会导致错误上电，故每行显式区分nominal/ideal/PENDING_RELEASE。
Ruling：只读引用旧40组理想DC数值，不重新求解，也不把理想驱动裕量作器件/实物保证。成本若越界会错误放行；表格保留来源和scope。
''')
checks=[['主采集拓扑','PASS','11Pro继承10功能追线','非实物性能'],['独立sense','PASS','FUNCTIONAL_INTERFACE_SPLIT_CHECK','两个4.99k外侧独立'],['实际连接','PASS','514 pins107 nets36 NC176 parts','独立冷重开'],['图纸主体','PASS_WITH_COMPANION','六页PDF+强制补充','独立发布HOLD'],['注释/网名','DOCUMENT_QUALITY_HOLD','旧R2文字/四新网名缺字','不再修EDA'],['ERC','DETAIL_HOLD','旧1209 count/no正文','不称clean'],['实物性能','NOT_VALIDATED','本包bench0','容量故障时序精度待验'],['实物和仪器','INPUT_UNKNOWN','未提供样机/设备/操作人员','不假定可上电'],['首次上电','NOT_RELEASED','下次集中裁定Phase1','本包不执行'],['PCB/采购/制造','NOT_STARTED','持续边界0','无Gerber/订单']]
dump('ACCEPTANCE_MATRIX.json',{'columns':['item','status','evidence','limit'],'rows':checks})
write('ACCEPTANCE_MATRIX.md','# 原理图接收矩阵\n\n| 项 | 状态 | 证据 | 边界 |\n|---|---|---|---|\n'+'\n'.join('| '+' | '.join(r)+' |' for r in checks))
# Existing ideal values are quoted, not regenerated or numerically swept.
dc=list(csv.DictReader((E/'DC_ENGINEERING_40_GROUPS.csv').open(encoding='utf8'))); selected=[r for r in dc if r['pattern'] in ['all_1000','all_3300','all_7000'] and r['row']=='0' and r['col']=='0'];assert len(selected)==3
dump('EXISTING_IDEAL_DC_REFERENCE.json',{'source':str(E/'DC_ENGINEERING_40_GROUPS.csv'),'sourceSHA256':hashlib.sha256((E/'DC_ENGINEERING_40_GROUPS.csv').read_bytes()).hexdigest().upper(),'rows':selected,'newSolverRuns':0,'scope':'old ideal exact virtual-ground screening values; no line R/offset/clamp leakage/ADC INL; not nominal physical tolerance or bench PASS'})
nets={r['net']:r['members'].split(';') for r in csv.DictReader((B/'FINAL_107_NETWORK_MEMBERS.csv').open(encoding='utf-8-sig'))}
write('ACTUAL_PROBE_MAP.md','''# 已接受网表的探点映射

以下是元件脚映射，不声称已有实体test pad或样机。人员须先在实体核脚/地，夹线在断电时完成；不在相邻细脚带电移动探头。

| 信号 | 已有真实网络成员中的探点 |
|---|---|
| 输入 | J1.1 V5_IN，J1.2 GND |
| 板上5V/3V3 | U9.6 V5；U10.6 V3V3；先优选对应去耦正端核实体位置 |
| REF_2V5 | U6.2，供VCM参考；不是ADC4.096V参考 |
| VCM /VEXC | R_VCM_ISO.2 /R_VEX_ISO.2，补偿后板上输出 |
| ROW0..3 | J2.1..4，各R_ISOi.2 |
| COL0..3 | J2.5..8 |
| TIA0..3 tap | R_TIA_ISOi.2、R_ADCi.1 |
| TIA_DRV0..3 | R_TIA_ISOi.1，探驱动侧区分tap |
| ADC_IN0..3 | C_ADCi.1，U5.16/.18/.21/.23 |
| ADC_REFIO /REFCAP | C_ADC_REFIO.1 U5.5；C_ADC_REFCAP.1 U5.7 |
| PGOOD/NRST | U7.6、R_RST.2、U11.6/U12.6为PGOOD同网 |
| 外部NRST | J3.5→MCU_NRST_EXT→R_J3_5 1k→PGOOD；不是旧Schmitt/G07候选 |
| 两sense | J3.1 V3V3_EXT_SWD；J4.1 V3V3_EXT_UART；各4.99k到V3V3，不作供电输入 |

所有公共地接GND；示波器保护地/探头地先核，禁止将地夹夹ROW/TIA/REF。SWD目标供电识别脚只sense，禁止调试器另一电源与板电源并供。PGOOD两监控OD并联、R_RST上拉；外部NRST只允许后续明确OD/OC正常低与HiZ，禁止推挽高/±电压强注入。
''')
dump('PROBE_NET_MEMBERS.json',{n:nets[n] for n in ['V5_IN','V5','V3V3','REF_2V5','VCM','VEXC','PGOOD','MCU_NRST_EXT','ADC_REFIO','ADC_REFCAP','V3V3_EXT_SWD','V3V3_EXT_UART']+[f'ROW{i}' for i in range(4)]+[f'COL{i}' for i in range(4)]+[f'TIA{i}' for i in range(4)]+[f'TIA_DRV{i}' for i in range(4)]+[f'ADC_IN{i}' for i in range(4)]})
write('FIRST_POWERUP_PRECHECK.md','''# 首次上电前检查表：当前未放行

填写PHASE1_RELEASE_INPUTS.json并取得明确release后才执行。空白字段不能以0、默认仪器或设计名义值替代。样机/人员/仪器信息已向用户询问，尚未提供时只能合同待执行。

1. 样机ID、装配记录、接线照片位置、基线commit/epro SHA、176BOM/514针/107网/36NC对应性。PCB尚未开始，不能假定现有已装配正确样机；不为准备包自行采购/装配。
2. 断电目视极性、焊桥、错位、供电电容/器件额定值和散热；核U9_BLEED RC2010FK-07100RL/R2010、U10_BLEED RC1206FR-07100RL/R1206实际封装和来源。既有DC功耗只作核查输入，不宣告热PASS。
3. 断电核J1.1=V5_IN、J1.2=GND；供电地、DMM、示波器和SWD地一致/隔离方式记录，先确认仪器保护地不会短接非GND。连续性/电阻实测另需明确release，当前没有执行。
4. 传感阵列、UART和SWD保持断开。确认ROW控制预定blank，且没有外接设备向sense/NRST/串口灌电。无可信blank固件或状态控制时不能自行写新协议；Phase1先批准仅供电的受控状态方案。
5. 设备型号、校准有效期、探头阻抗/电容、额定范围、限流可重复设置、电源关断位置、人员责任和日志目录填写。示波器连接在断电时完成，优先去耦/串阻端探点。
6. Pro release必须给供电设定/限流、硬断电电流/电压/温升门、允许上电次数及持续时间、PGOOD/reset/ADCpowerdown预期、可测节点。没有数值和状态定义，不上电。
7. 获准后的Phase1只限流电源+空载板：输入/5V/3V3，再REF_2V5/VCM/VEXC，PGOOD/NRST，ADC参考和电流。表中顺序不是当前执行命令；按批准数值和窗口记录原始波形。
8. 空载正常后也不自动接阵列：标准电阻、校准、10%变化、300us、100fps属于后续阶段需单独范围放行。禁止首次上电混入短路、±强故障、反灌、60s热测试。

每项填检查者/UTC/原记录位置/结论；出现接线矛盾或停止条件，先关断再保存记录，不带电修线、不改元件值。
''')
write('BENCH_STOP_CRITERIA.md','''# 台架立即停止条件

本包没有上电。后续release需将数值填入PHASE1_RELEASE_INPUTS.json；EXPECTED_NODE_RANGES的nominal和ideal栏不是硬断电阈值。

- 极性/接地错误、焊桥/接线与接受基线不一致、探头地短接非GND：不允许起动；已上电时立即输出OFF。
- 烟雾、异味、异常声响、明显器件发热、热像/测温超过批准温度或温升：立即OFF。不靠“电路通过了”继续观察。
- 输入电流达到批准硬断电值、持续限流折返/轨压塌陷、任何供电/参考超过批准边界：立即OFF，不增加限流尝试恢复。
- 空载正常建立窗口结束后VCM/VEXC/ROW/TIA仍失常，持续削顶、增长振荡、PGOOD/NRST反复动作或参考不建立：OFF并保留波形。启动瞬态、复位低和ADCRST/PD低本身须按批准预期解释，不能把正常powerdown下未启参考假判损坏或无限等待。
- 后续阵列试验若正常域削顶、意外输出/无法解释串扰、ADC标签/帧不完整、异常时序失效：退出采集并按风险OFF；不继续扩大工况，也不重拟合隐藏问题。
- 任何供电口被外接sense/UART/SWD回灌，或操作人员无法确定仪器范围/连接：OFF。

OFF后等待放电、确认安全残压，再断开夹线；放电安全阈值和等待要求随实体电容/仪器release填写。不短接电容放电、不施加负电压排故。记录最后正常样本、触发原因、时间、电流/轨压/温度/示波器原始文件和本次设置。一次异常停止后不自动重试，集中回报决定下一步。
''')
write('CALIBRATION_AND_ACCEPTANCE.md','''# 校准与验收合同：尚无实测

固定1–7kΩ正常域、0.8–8k保护带，4行4列8线。阵列16个电阻逐个测量并记录真实参考值/不确定度/线阻/温度；名义1k不代实测1k。不新增采购，未具备标准件的工况保持未执行。

每单元沿用已冻结八状态合同：D=mean(8 active ADC codes)-mean(8相邻blank codes)。保留48bit原码、channel/device/range标签及8状态/时间戳；各4通道每状态9次的首个dummy不进入均值。不把TIA单端电压当差分D。

1k/6.8k两点：以每单元独立实际标准值R_L/R_H和D_L/D_H拟合既有线性电导读数，G=1/R、D=A*G+B（Rhat=A/(D-B)）。这里只给使用口径，没有运行新的拟合/解析测试或生成新的固件。A、B和校准日期/温度/输入量程一次冻结，后续验证/每帧不能重新拟合。D_L-D_H异常小、符号/标签错或D-B接近0，不产生漂亮阻值：停止验收并保留原码。

独立3.3k、7k、棋盘/行列异质阵列和可用2.2k/4.7k为验证；1k/6.8k校准点只作校准后检查，不能作为独立精度证明。所用标准若不独立，报告这一限制，不重复算作验证。电导拟合是否适配真实电路仍须实测检验。

精度目标：对每个工况/每个单元，e_ij=100*(mean(Rhat_ij)-Rref_ij)/Rref_ij；目标|e_ij|<=1%，同时报告全16点最大绝对误差/平均绝对误差及不确定度，不用signed mean相互抵消。重复性：固定输入、校准参数不变，拟议采1000个连续完整有效帧，每单元SD(Rhat)/Rref*100<=0.2%，用sample SD(N-1)；报告N、丢/错/无效帧率。只筛掉已冻结资格拒绝的帧并保留拒绝记录，不能为达标删离群值。

10%：分别记录改变前后参考电阻和全16点读数，单点、整行、全阵列有矩阵工况。1k→1.1k、3.3k→3.63k属于正常域；7k→6.3k为正常负10%；7k→7.7k属于保护带，只独立标guardband，不能算正常精度PASS。目标分辨变化且邻居误差仍符合上述<=1%口径，不以“看见一点变化”代合格；保留变化幅度、噪声、邻居和真实时序。

300us建立、真实100fps、reset20–30C、容量/故障是独立验收项，不能由静态精度或离线32GREEN替代。无故障强注入；首次上电仅Phase1。所有数值是后续验收目标，本包observations=0。
''')
write('TIMING_CAPTURE_PLAN.md','''# 时序采集计划：只读合同

使用已冻结八状态BLANK0/ROW0..BLANK3/ROW3，300us建立等待、每状态先等待300us，再4通道×9次×25us=900us，合计1200us；8状态9600us，加400us其他开销为100fps目标。每帧288传输/32dummy/256有效。48clocks@4MHz为12us设计输入，不等于硬件实测。

A. 动态建立（后续已批准的标准阵列阶段）：触发ROW_SEL，至少同时捕获ROW、TIA_DRV、TIA tap、ADC_IN；示波器通道不足分组，保留同一触发/阵列/探头条件，不冒称分组是同次耦合波形。用既有探头高阻设置，记录输入C/带宽/采样率/地线方式，负载可能改动态。观察开关后0–300us和更长稳定段，依据实测最终稳定均值测300us残余；继承目标100uV的量测需满足噪声/分辨率，达不到仪器能力就标未验证，不用屏幕分辨率宣告PASS。增长振荡/削顶按停止条件退出。

B. SPI：抓CS/SCLK/MOSI/SDO与ROW_SEL；沿用冻结mode1/falling-edge采前稳定位合同，核48bit、16前导+16数据+4通道+2器件+3量程+7尾位，量程0x06 0–5.12V。先用实际rawclock/CS边界核标签和位序，不通过Python回归自证硬件edge正确。ADC配置/复位读回记录必须来自真实既有固件/设备；本包不写新固件。

C. 100fps/WCET：逻辑分析仪/DMA/ISR记录实际有效转换、状态边界、完整帧序号/epoch和采集完成时间。报告完整有效帧计数/壁钟时长、间隔分布、最大DMA/ISR占用和400us余量，丢/错/无效帧率单列。接收时间不替代采集时间，连续1000帧的设计观察窗口约10s；时钟、传输和采样率须从设备实测。已有25us周期空档和离线预算不能说已经100fps。

D. reset后续正常20–30C阶段：只用被批准的外部OD/OC低和HiZ释放，记录J3.5(外侧MCU_NRST_EXT)、PGOOD/MCU NRST、HW_ENABLE和ADC_RESET_N；J3.5串阻实际1k。观察安全blank、reset/config资格、epoch及两个完整好帧恢复；不复用旧47k/G17/G07候选连接，不假称10.25ms缺完整帧阈值证明<=10ms故障失效。

Phase1空载上电只采电源/参考/PGOOD/NRST建立，A/B/C/D并未获执行批准。保留仪器原文件、UTC、触发、原码/标签、帧资格拒绝记录；导出CSV/PNG只是可读附件，原采集文件和SHA也须保留。
''')
release={'status':'NOT_RELEASED','baselineCommit':'fbb7c0ed5f322f078583fadbdb353efe835e4c01','sampleId':None,'assemblyEvidence':None,'sampleBaselineMatchConfirmed':None,'operator':None,'supplyModel':None,'supplyCalibration':None,'DMMModel':None,'scopeModel':None,'probeImpedance':None,'probeCapacitance_pF':None,'debuggerModel':None,'groundingIsolationPlan':None,'blankControlExistingFirmwareIdentity':None,'ADCResetPowerdownExpectedState':None,'inputSetpoint_V':None,'currentLimit_mA':None,'hardOffCurrent_mA':None,'normalSupplyWindows_V':None,'hardOffVoltageWindows_V':None,'referenceSettleDeadline_ms':None,'maxTemperature_C':None,'maxTemperatureRise_C':None,'maxEnergizations':None,'maxPoweredDuration_s':None,'safeDischargeVoltage_V':None,'physicalUserBenchAuthorization':None,'proPhase1Ruling':None,'allFieldsRequireExplicitValuesBeforeBench':True}
dump('PHASE1_RELEASE_INPUTS.json',release)
write('PHASE1_RELEASE_CHECKLIST.md','''# 受控首次上电release输入

准备完成不等于允许执行。请在样机/仪器/操作人信息明确后，由Pro统一规定Phase1电源限流、探点顺序、正常范围、异常断电数值、建立等待与最大次数/时长，并保持用户实际bench授权边界。所有PHASE1_RELEASE_INPUTS.json未知字段保持null；无样机/无仪器时只能等待实体条件，不新建PCB或采购。

拟议唯一首轮范围：限流电源+空载板，传感阵列/外接设备断开；核J1/板上轨/REF2.5/VCM2.5/VEXC2.25/PGOOD/NRST/ADC参考、电流。空载允许状态（firmwareblank、ADCreset/powerdown是否保持）须写清；不能用未启动的ADC参考缺失证明错误，也不能为测参考擅自驱动逻辑。

只请求有界Phase1接收方案。标准阵列、校准、10%变化、300us、100fps、reset动作、任何短路/±强注入/反灌/60s热测试全排除该首轮。Phase1异常一次即停，不自行改电路/限流或重复。实物/操作/限流缺失是明确执行条件，文档缺字/ERCcount仅记录，不再回头修原理图。
''')
dump('GATES.json',{'SCHEMATIC_ELECTRICAL_BASELINE_ACCEPTED':True,'PIN_NET_COLD_PASS':[176,514,107,36],'PDF_READABLE_WITH_COMPANION':True,'PDF_STANDALONE_RELEASE':False,'LEGACY_ANNOTATION_DOCUMENT_QUALITY_HOLD':True,'INTERFACE_NET_LABEL_DOCUMENT_QUALITY_HOLD':True,'EDA_FROZEN_NO_REPAIR_REQUIRED':True,'BENCH_CONTRACT_PREPARED':True,'BENCH_NOT_RELEASED':True,'PHYSICAL_SAMPLE_AND_INSTRUMENTS_UNKNOWN':True,'PHASE1_NUMERIC_LIMITS_AWAIT_RULING':True,'HARDWARE_PERFORMANCE_NOT_VALIDATED':True,'FAULT_PROTECTION_HOLD':True,'REFERENCE_CAPACITANCE_BENCH_HOLD':True,'HARDWARE_WCET_PENDING':True,'PCB_NOT_STARTED':True,'actualBench':0})
write('SOURCE_INDEX.md','''# 既有证据来源

1. 11号完整裁定PRO_ACCEPTANCE_RULING_FULL.md：工程接受、240min、所有native/simulation/bench0、下一次Phase1集中release。
2. 固定基线commit fbb7c0ed5f322f078583fadbdb353efe835e4c01：actual107成员/176BOM/514针/cold/companion/addendum。ACCEPTED_BASELINE_SHA.json记录原文件SHA，引用不复制原生。
3. 08包DC_ENGINEERING_40_GROUPS.csv /DC_ENGINEERING_SUMMARY.json：旧40组理想DC、仅等效输入；本包EXISTING_IDEAL_DC_REFERENCE.json引用3组，不新算。温区、线阻、宏动态、器件实际饱和未由此证明。
4. 既有FIRST_BUILD sources/ADS8684.pdf.txt Section8.3.9、pinout：REFSEL低/内部4.096V、REFIO/REFCAP；并非REF3025的2.5V。本包只读厂家已存文本，不新下载。
5. 旧R2_VERIFICATION RESET_AND_TIMING_CONTRACT.md八状态/48clk/25us段，仅时间合同；旧复位候选已不适用当前J3.5实际1k直接PGOOD。当前reset接线只以已接受actualnet为准。

Pro已说明复看材料；这里只记录其声明，不冒称网页端逐个附件字节全读。新包只读证据，不开EDA/仿真/测试，不改变旧SHA。
''')
# Flat matrix: one cell-level condition per experiment row; R00..R33 define whole array.
matrix=[]
def case(i,stage,pattern,values,role='validation',frames=1000,notes=''):
 assert len(values)==16
 normal=all(x is not None and 1000<=x<=7000 for x in values)
 matrix.append([i,stage,pattern,role,*values,frames,normal,'NOT_EXECUTED_NOT_RELEASED',notes,'11_PRO_AND_FROZEN_BASELINE'])
case('P01','Phase1','no_array',[None]*16,'no_resistors_attached',0,'Empty R cells mean array not attached; never a short. Phase1 only after explicit release')
case('C01','Phase3','all_1000',[1000]*16,'calibration_low',1000,'actual R separately measured; not independent accuracy validation')
case('C02','Phase3','all_6800',[6800]*16,'calibration_high',1000,'freeze per-cell A/B once')
for r in [1000,3300,7000,2200,4700]: case('V'+str(r),'Phase2_3',f'all_{r}',[r]*16,role='calibration_check_only' if r==1000 else 'validation',notes='1000 is calibration check only; other independent standards required' if r==1000 else 'independently measured standard required; no procurement authorized')
case('VCHK','Phase2_3','checker_1000_7000',[1000 if (i//4+i%4)%2==0 else 7000 for i in range(16)])
case('VROW','Phase2_3','row_alt_1000_7000',[1000 if i//4%2==0 else 7000 for i in range(16)])
case('VCOL','Phase2_3','col_alt_1000_7000',[1000 if i%4%2==0 else 7000 for i in range(16)])
for b in [1000,3300]:
 for k in range(16):
  v=[b]*16;v[k]=b*11/10;case(f'D{b}_R{k//4}C{k%4}','Phase4',f'single_plus10_from_{b}',v,'change_validation',1000,'paired baseline and after; all16 neighbours retained')
 for k in range(4):
  v=[b*11/10 if i//4==k else b for i in range(16)];case(f'D{b}_ROW{k}','Phase4',f'row_plus10_from_{b}',v,'change_validation',1000,'paired baseline and after; unchanged rows retained')
 case(f'D{b}_ALL','Phase4',f'all_plus10_from_{b}',[b*11/10]*16,'change_validation')
case('D7000_MINUS','Phase4','single_minus10_from_7000',[6300]+[7000]*15,'change_validation',1000,'normal-domain boundary; paired all7000 baseline')
for r in [800,8000]:case(f'G{r}','excluded_guardband',f'all_{r}',[r]*16,'guardband_not_normal_acceptance',0,'not in first normal/Phase1 scope; separate future release')
case('G7700','excluded_guardband','single_7000_plus10',[7700]+[7000]*15,'guardband_not_normal_acceptance',0,'7000+10%=7700 outside1-7k; do not use for normal PASS')
cols=['case_id','phase','pattern','role']+[f'R{r}C{c}_ohm' for r in range(4) for c in range(4)]+['planned_complete_frames','normal_domain','execution_status','notes','source']
table=[cols]+matrix
nodeCols=['node','state','nominal_V','reference_lower_V','reference_upper_V','unit','probe_member','acceptance_threshold_status','hard_off_threshold_status','source','scope']
nodes=[]
def node(n,st,nom,low,high,pin,source,scope):
 nodes.append([n,st,nom,low,high,'V',pin,'PENDING_PHASE1_RELEASE','PENDING_PHASE1_RELEASE',source,scope])
for n,v,pin in [('V5_IN',5,'J1-1'),('V5',5,'U9-6'),('V3V3',3.3,'U10-6'),('REF_2V5',2.5,'U6-2'),('VCM',2.5,'R_VCM_ISO-2'),('VEXC',2.25,'R_VEX_ISO-2')]:node(n,'no_array_expected',v,None,None,pin,'11_PRO /actualnet','nominal target only; supply tolerances/stop windows require release')
for n,pin in [('ADC_REFIO','U5-5'),('ADC_REFCAP','U5-7')]: node(n,'ADC_enabled_internal_ref',4.096,None,None,pin,'existing ADS8684 Section8.3.9','only enabled internal reference; reset/powerdown state must be specified; effective MLCC pending')
for i in range(4):
 node(f'ROW{i}','blank',2.5,None,None,f'R_ISO{i}-2','frozen nominal VCM','no physical settling guarantee')
 node(f'ROW{i}','selected',2.25,None,None,f'R_ISO{i}-2','frozen nominal VEXC','ROW driver differs with sum row load; not same as sensor-side output')
 node(f'TIA{i}','blank/no_array',2.5,None,None,f'R_TIA_ISO{i}-2','frozen nominal VCM','offset/leakage/startup not validated; high impedance probes')
 for r in selected:
  R=int(float(r['R_ohm']));node(f'TIA{i}',f'all{R}_selected',float(r['TIA_tap_V']),None,None,f'R_TIA_ISO{i}-2','old08 DC40 row0col0','quoted old ideal value only; not range/tolerance/stop criterion')
  node(f'ADC_IN{i}',f'all{R}_selected',float(r['ADC_V']),None,None,f'C_ADC{i}-1','old08 DC40 row0col0','quoted ideal; ADC INL/reference/leakage not validated')
node('PGOOD/MCU_NRST','reset_release',3.3,None,None,'U7-6','11_PRO /actualnet','OD node may validly remain low during startup/undervoltage; timing window pending')
node('MCU_NRST_EXT','external_reset_low',None,None,0.4,'J3-5','09_addendum normal OD/OC VOL<=0.4','existing normal reset input contract, not Phase1 power threshold; no push-pull or fault injection')
dump('TABLE_INPUTS.json',{'BENCH_TEST_MATRIX.csv':table,'EXPECTED_NODE_RANGES.csv':[nodeCols]+nodes,'purpose':'static reproducible bench input contract, no measurements','CSVOnly':True})
releaseCount=len(matrix);assert len({r[0] for r in matrix})==releaseCount
q=json.loads((P/'EXECUTION_BUDGET.json').read_text('utf8'));q['phaseHistory'].append({'phase':'P0_baseline','startedUTC':q['phaseStartedUTC'],'endedUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()});q['phase']='P1_contract';q['phaseStartedUTC']=datetime.datetime.now(datetime.timezone.utc).isoformat();dump('EXECUTION_BUDGET.json',q)
print(json.dumps({'matrixRows':len(matrix),'nodeRows':len(nodes),'nativeCopies':0,'bench':0,'simulation':0}))
