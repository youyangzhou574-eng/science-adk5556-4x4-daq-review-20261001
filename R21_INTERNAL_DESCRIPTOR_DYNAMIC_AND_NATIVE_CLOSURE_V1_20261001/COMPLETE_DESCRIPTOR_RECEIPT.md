# 07号内部 descriptor 包完整阻断回执

`SCIENCE_ADK5556_4X4_R21_INTERNAL_DESCRIPTOR_DYNAMIC_AND_NATIVE_CLOSURE_V1`

本包在 P0 局部 VCM/VEXC 双宏 AC 资格失败后触发 **DESCRIPTOR_EXTRACTION_NOT_QUALIFIED**。没有进入 P1/P2/P3，没有新完整板级数据、暂态或原生工程。剩余额度不能解除 STOP。本回执不是内部稳定性证书，不判定物理电路失稳。

## 输入、授权与冻结范围

完整07号裁定 `CIRCUIT-PRO-R21-REFERENCE-BLOCKED-ACCEPT-INTERNAL-DESCRIPTOR-CERTIFICATION-20261001-07`，assistant104a4b67-268e-428d-b069-1490441ec58a，parentuser5cc2d468-e291-4d36-8c4e-31f97fa110a2 已全文读取保存为 PRO_DESCRIPTOR_RULING_FULL.md。旧06号余量不结转。新包480min，P0/P1/P2/P3/P4分别150/120/100/80/30min；开始UTC2026-10-01T16:09:29。§6/20批准新的 P0 局部资格 OP/AC；§15禁止未通过三门前的 full-network port AC。本包只用了前者。

固定4行4列8线、800–8000Ω、5V+3V3、VCM2.5V、VEXC2.25V/E.25V、Rf4.99k/Cf2.2nF、100fps目标；ROW/VCM/VEXC1k/4.99k/100p、TIA1k/22p候选。原模型 SHA 保持，旧模型、协议及原生未改，不做第三轮补偿扫描。当前局部真实资格 TEMP=27°C，不扩展旧25°C directNRST范围。PCB/制造/采购/bench/本地Git/系统改动全0，无安装、新执行器或新模型包。

## 实际实现和证据边界

专用 source-preserving flatten reader 处理实际 R/C/V/I/E/G/H/S 与 subckt、params、局部模型和续行；forward-mode表达式导数处理实际激活的 VALUE/LIMIT/IF/PWR。标准 MNA 电压源/受控源 branch 均保留。原始 follower227宏primitive加4顶层元件，共231。

原生 `listing e` 揭示 PSA 新增的 B 电压源、内部节点、A pswitch/PWL。processed.py 读取实际展开清单，保留这些代数节点和电压 branch；follower252展开元件/170未知量，全部变量名与原生 OP 的170向量逐名一致，ROW176、TIA178、REF2 344变量也已保留。processed的line字段原为ngspice deck卡片编号，已增listingCardNumber和stdout物理行定位，完整processed到冻结LIB原始源行桥接尚未闭合。变量名对应不是内部谱证书；没有 minimal realization、pole筛除或 port-only拟合。

原始硬 TABLE 端点截断不足：实际 follower 正向控制0.2500001316567726、负向−0.2500001316567726。两 PWL 原生探针各 OP+3AC（1/100M/300M Hz）显示正向导数8.658125911920636e−6、负向导数1.122386189789580e−5，负向不是零。pwl.py 的二次角点平滑是依据参数和探针推导的**候选公式**，两个实际 OP 导数与原生一致；未证明所有内部角点/温区/限幅/其他工作点。没有把模型改成行为替代品。pswitch 默认控制端1e12Ω遗漏经先RED后GREEN修复；transition band仍HOLD。

raw OP 原先同名 v(vdd)/i(vdd)相互覆盖的读取错误经先RED后GREEN修复，电压与电流分别映射为节点名和 branch: 名。原始 raw/log 未修改。18个基础回归在后续控制补丁前实际GREEN，只验证已实现解析/符号/变量保留与两个实测导数，不充当完整 staircase/有限谱资格。

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

用户已亲自与网页端沟通。随后内部只读取得两条完整新回复：assistant251f50e6-b184-4097-95a7-cba66dd8168c及5c1a3804-d8cb-4bb5-997d-63b9c983b84f。网页端明确承认验证目标漂移，要求工程目标优先，停止新增MIMO/descriptor/reference-normalization研究作为原理图硬门，回到R2.1原理图最终化＋有限工程验证。**本包就此作为历史阻断证据结案，不再申请继续修descriptor。** 先前写入的工具修复申请仅作为历史草稿留存，已被本段工程接续请求替代，不属于待执行下一包。

接续应围绕实际工作点、饱和/余量、300µs建立、明显增长振荡、精度/速度与故障边界；宏模型跑不动可依新裁定标数值限制，不再升级数学证明。ROW/VCM/VEXC100p、TIA22p、NRST1k直连候选、八状态与progress watchdog、参考/ADC去耦、元数据/图面审计等成熟修订应及时落图。实际bench/PCB/制造/采购仍0，只能准备受控台架验证方案，不自动执行；原生连接审计和具体安全/工程风险继续保留。网页最新提及1–7kΩ/约10%变化，历史冻结范围800–8000Ω，待统一工程裁定明确目标与工程验收，不自行改冻结输入。

**依用户明确提出的“下次正常报告同时申请更多执行时间、计算次数和自主范围”要求**，在本次正常交付集中申请一个有界工程包480min：资料/范围与最小ECO冻结40、有限DC/分区动态120、原生与连接图面审计240、完整交付80min；OP/AC≤32、短正常暂态≤12且单次≤180s、full-long0、PZ/MIMO/descriptor新研究0、reset解析≤32/protocol≤48/原厂资料≤8/candidate≤2/库身份≤4；原生copy1/session2/save8/captureaudit4/ERC2/PDF2。普通实现本地累计，重大设计/风险/真实阻塞集中裁定，避免小步骤重复请示。具体项目包名、准入门与计数由下一完整工程裁定统一确定；旧07余量不结转，这只是集中预算申请，未批不执行。不扩平台额度、安装/执行器/模型包/账户或bench/PCB/system范围。已获得用户教育网页端的结果，不在此重复工具路线辩论。

## 文件与可读交付

完整裁定、预算、GATES、source/model hash、全部七cases原始stdout/stderr/OP raw与AC txt、精确comparison CSV、完整E/A/B NPZ、全部stamp/变量JSON、程序与18基础测试逐文件交付；4macro未运行但准备netlist保留并标未执行。可读索引README.md/CASE_EXECUTION_INDEX.csv/OFFICIAL_SOURCE_INDEX.json，SHA256_MANIFEST和完整source/evidence ZIP（辅助，非唯一读取形式）。官方手册大段摘录保留本地，不重复公开复制；公开提供官方索引/页段和SHA，排除项可核。失败数据不会只藏在压缩包。

网页实际是否读取未验证，不虚报，不把读回ACK加为科学执行门。固定版本一次性摘要提交后记录送达、历史确认、回复owner与nextCheck，建立接续monitor。ACK/旧07裁定不能解除本STOP。最终独立审查结果附FINAL_REVIEW.md，批注修复仅限证据/控制，不在STOP后科学重算。


独立终审Critical0、Important4、Minor1：四项netlist SHA改为实际CRLF文件字节hash，保留旧LF值；processed卡片编号与物理行明确区分，原始LIB桥接未资格；两个follower失败统一stickySTOP；supervise增加STOP/唯一预扣/phase/限时/防日志覆盖和独占claim。最后两项是控制补丁，未复跑科学或回归，仅22 Python文件静态ast语法检查PASS，不声称终态代码运行资格已过。详见FINAL_REVIEW.md及evidence。

END-OF-COMPLETE-R21-INTERNAL-DESCRIPTOR-P0-BLOCKED-RECEIPT
