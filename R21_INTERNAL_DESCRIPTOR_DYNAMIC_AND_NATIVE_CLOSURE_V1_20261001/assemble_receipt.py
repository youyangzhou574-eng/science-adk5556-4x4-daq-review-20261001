from pathlib import Path
import json,csv,hashlib,datetime
r=Path(__file__).resolve().parent;utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();b=json.loads((r/'EXECUTION_BUDGET.json').read_text());assert b['scienceStopped']and b['stopReason']=='DESCRIPTOR_EXTRACTION_NOT_QUALIFIED'
b['stopObservedAtUTC']=utc();b['stopBudgetFileMtimeUTC']=datetime.datetime.fromtimestamp((r/'EXECUTION_BUDGET.json').stat().st_mtime,datetime.timezone.utc).isoformat();b['rejectedDispatches']=[{'case':'qual_4macro','reason':'SCIENCE_STOP_PENDING_NEW_RULING','actualExecutorStarted':False,'predebitSucceeded':False,'resultsDirectoryExists':(r/'results/qual_4macro').exists(),'detail':'Dependent start command was queued in same tool orchestration after local reference comparison, before root inspected returned failure. Sticky register rejected before folder or executor creation. No exception authorized.'}];(r/'EXECUTION_BUDGET.json').write_text(json.dumps(b,indent=2))
cases=[]
for p in sorted((r/'results').glob('*/STATUS.json')):
 s=json.loads(p.read_text());s['nativeAnalysesPreDebited']=next(x['chargeCounts']['DC_AC_PZ']for x in b['cases']if x['name']==s['case']);s['netlistSHA256']=hashlib.sha256((r/'cases'/ (s['case']+'.cir')).read_bytes()).hexdigest().upper();cases.append(s)
with (r/'CASE_EXECUTION_INDEX.csv').open('w',newline='')as f:
 fields=['case','ownedPID','startedUTC','endedUTC','status','exitCode','analysisStatus','wallSeconds','nativeAnalysesPreDebited','netlistSHA256'];w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(cases)
gates={'stickySTOP':'DESCRIPTOR_EXTRACTION_NOT_QUALIFIED','stopCase':'qual_ref2','LINEARIZED_MNA_DESCRIPTOR_QUALIFIED':False,'REFERENCE_DESCRIPTOR_REGULAR':False,'REFERENCE_INTERNAL_SPECTRUM_AVAILABLE':False,'finiteInfiniteStaircaseImplemented':False,'fullNetworkStatesTested':0,'newNormalTransient':0,'nativeAllOperations':0,'directTIA':False,'holds':['DESCRIPTOR_EXTRACTION_NOT_QUALIFIED','REFERENCE_REALIZATION_AND_INTERNAL_CERTIFICATE_HOLD','DYNAMIC_VALIDATION_HOLD','FAULT_PROTECTION_HOLD','REFERENCE_CAPACITANCE_HOLD','ERC_DETAIL_HOLD','DRAWING_LAYOUT_HOLD','BENCH_NOT_RELEASED','RESET_THRESHOLD_ENVELOPE_HOLD','FAULT_LATENCY_CONTRACT_HOLD','COUPLED_MODEL_CONVERGENCE_HOLD','EXACT_LOW_FREQUENCY_POINTS_FULL_NETWORK_HOLD']};(r/'GATES.json').write_text(json.dumps(gates,indent=2))
official={'source':'Existing official ngspice47 bundled manual','path':b['officialSources'][0]['path'],'SHA256':b['officialSources'][0]['sha256'],'URL':'https://ngspice.sourceforge.io/docs/ngspice-manual.pdf','usedSections':['8.2.7 PWL Controlled Source','8.2.12 Alternative Analog Switch'],'summary':'PWL controlled source has smoothing input_domain; pswitch has default control input resistance 1e12 and rounded log/linear transition. The static iteration pointer is not itself proof of a dynamic realization. Quadratic corner derivative is an inferred implementation candidate corroborated by two actual follower OP primitive probes and local AC, not a global code-model proof.'};(r/'OFFICIAL_SOURCE_INDEX.json').write_text(json.dumps(official,indent=2))
receipt='''# 07号内部 descriptor 包完整阻断回执

`SCIENCE_ADK5556_4X4_R21_INTERNAL_DESCRIPTOR_DYNAMIC_AND_NATIVE_CLOSURE_V1`

本包在 P0 局部 VCM/VEXC 双宏 AC 资格失败后触发 **DESCRIPTOR_EXTRACTION_NOT_QUALIFIED**。没有进入 P1/P2/P3，没有新完整板级数据、暂态或原生工程。剩余额度不能解除 STOP。本回执不是内部稳定性证书，不判定物理电路失稳。

## 输入、授权与冻结范围

完整07号裁定 `CIRCUIT-PRO-R21-REFERENCE-BLOCKED-ACCEPT-INTERNAL-DESCRIPTOR-CERTIFICATION-20261001-07`，assistant104a4b67-268e-428d-b069-1490441ec58a，parentuser5cc2d468-e291-4d36-8c4e-31f97fa110a2 已全文读取保存为 PRO_DESCRIPTOR_RULING_FULL.md。旧06号余量不结转。新包480min，P0/P1/P2/P3/P4分别150/120/100/80/30min；开始UTC2026-10-01T16:09:29。§6/20批准新的 P0 局部资格 OP/AC；§15禁止未通过三门前的 full-network port AC。本包只用了前者。

固定4行4列8线、800–8000Ω、5V+3V3、VCM2.5V、VEXC2.25V/E.25V、Rf4.99k/Cf2.2nF、100fps目标；ROW/VCM/VEXC1k/4.99k/100p、TIA1k/22p候选。原模型 SHA 保持，旧模型、协议及原生未改，不做第三轮补偿扫描。当前局部真实资格 TEMP=27°C，不扩展旧25°C directNRST范围。PCB/制造/采购/bench/本地Git/系统改动全0，无安装、新执行器或新模型包。

## 实际实现和证据边界

专用 source-preserving flatten reader 处理实际 R/C/V/I/E/G/H/S 与 subckt、params、局部模型和续行；forward-mode表达式导数处理实际激活的 VALUE/LIMIT/IF/PWR。标准 MNA 电压源/受控源 branch 均保留。原始 follower227宏primitive加4顶层元件，共231。

原生 `listing e` 揭示 PSA 新增的 B 电压源、内部节点、A pswitch/PWL。processed.py 读取实际展开清单，保留这些代数节点和电压 branch；follower252展开元件/170未知量，全部变量名与原生 OP 的170向量逐名一致，ROW176、TIA178、REF2 344变量也已保留。变量名对应不是内部谱证书；没有 minimal realization、pole筛除或 port-only拟合。

原始硬 TABLE 端点截断不足：实际 follower 正向控制0.2500001316567726、负向−0.2500001316567726。两 PWL 原生探针各 OP+3AC（1/100M/300M Hz）显示正向导数8.658125911920636e−6、负向导数1.122386189789580e−5，负向不是零。pwl.py 的二次角点平滑是依据参数和探针推导的**候选公式**，两个实际 OP 导数与原生一致；未证明所有内部角点/温区/限幅/其他工作点。没有把模型改成行为替代品。pswitch 默认控制端1e12Ω遗漏经先RED后GREEN修复；transition band仍HOLD。

raw OP 原先同名 v(vdd)/i(vdd)相互覆盖的读取错误经先RED后GREEN修复，电压与电流分别映射为节点名和 branch: 名。原始 raw/log 未修改。18个基础回归实际GREEN，只验证已实现解析/符号/变量保留与两个实测导数，不充当完整 staircase/有限谱资格。

## 局部 AC 结果

精确12点为0.01/0.1/1/10/100/1k/10k/100k/1M/10M/100M/300M Hz；近零绝对归一化 floor在资格程序中固定1e−9，未在失败后改阈值。

|实际case|完整descriptor维数|实际比较数量|最大复数相对误差|范围结论|
|---|---:|---:|---:|---|
|原始 follower近似|128|12|9.964463969898566e−4|仅原始primitive近似，PSA变量不完整|
|processed follower|170|12|9.68245188639181e−8|12点局部响应通过0.2%，无谱证书|
|ROW|176|48|1.1729977447914115e−3|12点4输出局部响应通过，无交越资格|
|loaded TIA|178|72|1.1349698886659347e−3|12点6输出局部响应通过，无交越资格|
|VCM/VEXC REF2|344|72|2.172645969728587e−1|资格FAIL，立即sticky STOP|
|已准备4宏分区|未求解|0|未得|启动被STOP守卫拒绝|

REF2最大误差在0.1Hz、cmminus：ngspice(4.025965269494058e−8+j1.019401533866064e−8)，descriptor(4.928269504572371e−8+j1.019381451561036e−8)，绝对差9.02304235301796e−9，相对约21.726%。0.01/1/10Hz同一响应分别约9.704%/7.018%/.458%。这是很小的内部反馈差分响应，不能把百分比扩大成VCM实体输出21.7%错误或物理不稳定。矩阵求解出现 rcond≈1e−18等警告；失效可能涉及数值缩放/OP一致性/剩余Jacobian，但本包没有完成根因归属，不能声称唯一原因。

所有原生分析进程正常终态；局部宏求解有 dynamic/true gmin stepping失败后 source stepping完成日志。各 AC 会重新初始化工作点，当前保存的单次OP与多次AC再求OP的一致性尚未独立证实；不得因为进程exit0称每项资格通过。精确响应CSV保留全部非零/近零和失败数据。dense交越数据已原生输出，但交越fc/phase对照未完成；没有把“无交越”视为PASS。

有限/无限 staircase、解析 hidden-mode证书fixture、参考同维cross-block stamp差分、内部极点/真实RHP contour全部未实施。完整10宏D0-D3、六七宏动态/供电/温区/故障全0，既有合同/reset范围只沿用此前有限证据，不重新宣称100fps或≤10ms物理门通过。directSeriesShunt=false保持记录；没有误当本包STOP原因。

## 预算、控制偏差和停止

7实际ngspice进程：显式7 OP+58 AC=65/192分析命令；其中每个局部12精确AC+denseAC预扣13AC。AC内部初始化及 stepping是原生分析内部工作，不另冒称新增独立资格case。diagnostic13/48=7实际case+5原子预扣离线比较+1早期事后记账探针。新逻辑资料1/8（已存在官方manual阅读）；normalTRAN0/64、full-long0/1、reset0/96、protocol0/48、candidate0/2、native全部0。

偏差1：早期128维单个.01Hz离线探针在离线预算预扣前执行，已如实事后增加1diagnostic，未超限，但不是预扣PASS，不回填时间。随后离线诊断统一走原子预扣。

偏差2：REF2比较和后续4宏启动命令同处一个顺序工具编排，根agent未先审查返回值就排入依赖启动；REF2先设置sticky STOP，4宏 register立即报SCIENCE_STOP_PENDING_NEW_RULING，在预扣/目录/child生成前被拒绝。实际4宏求解0、没有科学STOP后的新executor。控制守卫生效，编排依赖审查仍需改为“资格结果检视后才提交下一启动”。不追认例外。

STOP实际预算文件mtime及观察时间见EXECUTION_BUDGET.json，保留fail原账，不以余量重试、修参数、重抽Jacobian或跨门。继续工作仅为只读证据整理、独立终审和交付。旧冻结文件与模型SHA由公开发布检查；全部自有solver终态见CASE_EXECUTION_INDEX.csv。

## 保持的门与集中新裁定请求

DESCRIPTOR_EXTRACTION_NOT_QUALIFIED / REFERENCE_REALIZATION_AND_INTERNAL_CERTIFICATE_HOLD / DYNAMIC_VALIDATION_HOLD / FAULT_PROTECTION_HOLD / REFERENCE_CAPACITANCE_HOLD / ERC_DETAIL_HOLD / DRAWING_LAYOUT_HOLD / BENCH_NOT_RELEASED / RESET_THRESHOLD_ENVELOPE_HOLD / FAULT_LATENCY_CONTRACT_HOLD / COUPLED_MODEL_CONVERGENCE_HOLD。旧 fullnetwork .1/1/10Hz仅邻近采样的纠正保持；本次局部精确点不代替完整板级精确点。

请统一裁定唯一下一包：处理完整 processed MNA 的固定等价缩放、near-zero floor/主要响应定义与同一OP Jacobian/原生AC一致性，再完成五类局部资格和finite/infinite staircase。只有真PASS才继续原07的同维reference/internal finite spectrum与条件动态/原生；不回 port-only normalized reference，不放行bench。

**按用户明确提出的“下次正常报告同时申请更多执行时间、计算次数和自主范围”要求**，在本次集中报告申请一个480min有界下一包（P0提取器/数值资格150、条件内部谱120、动态100、条件原生80、交付30min），新的分析192、diagnostic48、normalTRAN64、full-long1≤8min、reset96/protocol48/source8/candidate2、条件native1/2/8/4/2/2。用途是一次完成上述连续路线，普通实现和进度本地累计，重大方法/范围变化或真实STOP集中报告。当前余量关闭，不结转；这只是请求，未获批不执行，不扩模型平台额度/账号权限/模型包或PCB/制造/采购/bench/system范围。若网页采用更窄唯一资格修复包，以统一裁定为准。

## 文件与可读交付

完整裁定、预算、GATES、source/model hash、全部七cases原始stdout/stderr/OP raw与AC txt、精确comparison CSV、完整E/A/B NPZ、全部stamp/变量JSON、程序与18基础测试逐文件交付；4macro未运行但准备netlist保留并标未执行。可读索引README.md/CASE_EXECUTION_INDEX.csv/OFFICIAL_SOURCE_INDEX.json，SHA256_MANIFEST和完整source/evidence ZIP（辅助，非唯一读取形式）。官方手册大段摘录保留本地，不重复公开复制；公开提供官方索引/页段和SHA，排除项可核。失败数据不会只藏在压缩包。

网页实际是否读取未验证，不虚报，不把读回ACK加为科学执行门。固定版本一次性摘要提交后记录送达、历史确认、回复owner与nextCheck，建立接续monitor。ACK/旧07裁定不能解除本STOP。最终独立审查结果附FINAL_REVIEW.md，批注修复仅限证据/控制，不在STOP后科学重算。

END-OF-COMPLETE-R21-INTERNAL-DESCRIPTOR-P0-BLOCKED-RECEIPT
'''
(r/'COMPLETE_DESCRIPTOR_RECEIPT.md').write_text(receipt,encoding='utf-8')
(r/'README.md').write_text('''# Internal descriptor P0 qualification — blocked

[完整报告](COMPLETE_DESCRIPTOR_RECEIPT.md) · [完整07裁定](PRO_DESCRIPTOR_RULING_FULL.md) · [预算与偏差](EXECUTION_BUDGET.json) · [门](GATES.json) · [原生执行清单](CASE_EXECUTION_INDEX.csv)

STOP: **DESCRIPTOR_EXTRACTION_NOT_QUALIFIED**. REF2最大相对误差21.726%发生于约4e−8的小内部反馈响应，绝对差9.023e−9；不是实体输出误差/物理失稳的证明。完整谱/暂态/原生0。

- [REF2失败全部CSV](results/qual_ref2/DESCRIPTOR_AC_COMPARISON.csv) / [资格](results/qual_ref2/QUALIFICATION.json) / [完整变量stamp](results/qual_ref2/STAMP_MAP.json) / [原生日志](results/qual_ref2/stdout.log)
- [ROW对照CSV](results/qual_row/DESCRIPTOR_AC_COMPARISON.csv) / [TIA对照CSV](results/qual_tia/DESCRIPTOR_AC_COMPARISON.csv) / [processed follower CSV](results/PROCESSED_FOLLOWER_EXACT_AC_COMPARISON.csv)
- [PWL实际探针映射](PWL_PROBE_SOURCE_MAP.json) / [正向原生AC](results/pwl_actual_op_0/ac_0.txt) / [负向原生AC](results/pwl_actual_op_1/ac_0.txt)
- [官方资料来源](OFFICIAL_SOURCE_INDEX.json) / [资格cases](LOCAL_QUALIFICATION_CASES.json) / [原始primitive来源](PRIMITIVE_INVENTORY.json)

全部source、原始raw/log/txt、NPZ、CSV与失败证据直接文件提供；archive仅辅助。局部精确AC通过不代表内部hidden-mode、finite/infinite staircase或bench资格。独立终审见FINAL_REVIEW.md。
''',encoding='utf-8')
print(json.dumps({'processes':len(cases),'nativeAnalyses':b['used']['DC_AC_PZ'],'diagnostics':b['used']['diagnostics'],'STOP':gates['stickySTOP']}))
