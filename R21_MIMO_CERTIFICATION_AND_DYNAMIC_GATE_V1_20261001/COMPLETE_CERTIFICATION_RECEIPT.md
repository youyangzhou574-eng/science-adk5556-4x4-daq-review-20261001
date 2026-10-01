# R21 MIMO certification — reference and internal-certificate HOLD

仅SCIENCE_ADK5556_4X4_DAQ_REPLICA。新包SCIENCE_ADK5556_4X4_R21_MIMO_CERTIFICATION_AND_DYNAMIC_GATE_V1，完整消费assistant c1c48dcc-32ce-414d-b185-bdd829952edd的新480min裁定。科学STOP为REFERENCE_REALIZATION_AND_INTERNAL_CERTIFICATE_HOLD；不代表实体电路失稳，不能宣称稳定，未进动态、原生、bench。此前INVARIANT交付commit2e2829f17c2b07c95c5d5c953a5fc3fdfb0a3b98保持冻结；本次另目录交付。

## 冻结输入与实际工作

输入为上一包真实20列open/closed两拓扑构成的NEW_GC.npz，839频点、10×10、仅5V/allblank/all800状态。逐文件输入SHA在INPUT_VERIFIED.json，输入复制不改变旧文件。新包没有新增SPICE、模型/执行器、原生操作或实际状态覆盖，不把旧52求解/104分析重新算新预算。

用明确端口次序REF=[0,1]、ROW=[2,3,4,5]、TIA=[6,7,8,9]构造块对角G0候选。每个块保留Gc主子矩阵，自始到终只称代数候选；从边界端口矩阵取主块本身不能证明独立可实现的物理参考，更不能自动提供内部极点证书。采用既有功率共轭坐标、频率无关固定正尺度、广义QZ和LU/logdet，无矩阵求逆，无删低频/对称恢复。

两拓扑各三固定尺度（单位及互逆混合10^-3..10^3）实际离线重算，六个BLOCK_PENCIL.csv全839点保留复数μ、condGc/condG0、backward residual、敏感性代理、det幅相；四个SPECTRUM_COMPARISON.csv保留无穷值计数和有限匹配范围，不能用有限子集替代全谱资格。

## 已取得的数学与数值证据

### 1. 块参考的已知真值工具链

两个10状态不对称解析state-space fixture，使用与实际相同的REF2/ROW4/TIA4分组。

- 稳定fixture的完整A和块A0全部LHP，真实RHP闭合轮廓LU/logdet三固定尺度绕数约0。这两个新解析例没有调用QZ，不能称它们完成QZ资格。
- 仅跨REF/ROW块反馈造成一个已知RHP闭环pole的fixture，参考A0仍全部LHP，三固定尺度真实RHP绕数约1。
- A矩阵、完整/参考真值pole及逐尺度绕数全部保存KNOWN_BLOCK_REALIZATION_FIXTURES.json。此为已知可见状态realization资格，只证明该解析工具链能区分这两例，不能变成实际OPA宏模型的内部稳定证书。

### 2. 有限轴代理保持约0，但整谱数值资格未过

两拓扑单位尺度的Gc最大条件数约6.66e18/6.55e18。极端混合正尺度下，open/closed分别有242/252个频点出现广义无穷值导致全谱不能与单位尺度比较；0.01Hz单位尺度无穷0，某尺度无穷5。逆序尺度虽然全谱值有限，有限匹配差值最大约6.64%。这些均为双精度前向数值HOLD，不等于真实电路出现无限极点或物理失稳。

六个有限虚轴det代理绕数均约0，phase increment≤约0.058rad。代理定义为负频镜像→正频的已采样虚轴线，低频缺口及高频端用直接相位连接；这没有真实求值RHP大弧/缺口，也没有内部参考pole-zero证书，不能称GENERALIZED_NYQUIST_PASS。小backward residual和LU相位一致不补足QZ全谱前向稳定性。

### 3. 参考“无RHP传递极点”与所需证书不同

明确的proper rational解析反例：

Gc=(s+1)/(s+2)，G0=(s−1)/(s+2)，R=(s+1)/(s−1)。

Gc和G0传递函数均没有RHP pole，但G0有RHP zero。Gc零点在−1，参考零点+1；真实正向RHP轮廓R绕数−1，而Gc仍无RHP零。独立解析位置和数值真轮廓−1一致，见REFERENCE_ZERO_COUNTEREXAMPLE.json。

这说明N=0默认门必须连同参考零点/比值的极点和内部稳定性解释，不能单独从“参考传递矩阵无RHP pole”推出。此反例不是反对一个已经独立证明内部稳定且最小实现的物理参考；它指出当前端口对象与物理参考闭环pole之间尚需定义映射。

### 4. 端口数据不能辨别不可见内部RHP模态

稳定单状态A=[−1], B=[1], C=[1]和A=diag(−1,+1), B=[1,0]^T, C=[1,0]有解析上完全相同端口传递1/(s+1)，但后一系统内部含+1不稳定隐藏模态。PBH核对该RHP模态不可控/不可观，839冻结频点的浮点响应核对最大差约1.57e−16，见HIDDEN_INTERNAL_MODE_COUNTEREXAMPLE.json。

这不声称OPA模型实际有隐藏不稳定状态。它严格限制当前证据：若没有原始内部descriptor/state-space、可控可观/最小性或独立物理内部证书，仅靠端口传递拟合和单环有限fc/PM不能证明实际内部稳定。对端口拟合求得的pole不能冒称原始实现全部pole。

## 新发现的冻结频点覆盖缺口

首次预检发现旧频率轴只有0.01Hz精确，其他指定点为：

|要求Hz|实际最近Hz|绝对差Hz|
|---:|---:|---:|
|0.01|0.01|0|
|0.1|0.10004663969866433|0.00004663969866433|
|1|1.0009330114994361|0.00093301149943614|
|10|10.013998436398301|0.013998436398301|

EXACT_FREQUENCY_COVERAGE.json记录全部值。保留整条0.01–300MHz轴，没有删低频、插值填点或重写旧结果。此前“含0.1/1/10”的表达不能解释为精确包含；本包纠正为邻近点证据，EXACT_LOW_FREQUENCY_POINTS仍HOLD。旧原件与报告不回填，不把元数据取整当真实求解。

## 执行、测试、失败与预算账

新480min从收到/保存裁定的15:35:37UTC计时，不回溯旧包。阶段90/150/100/80/30共450min，余30全局保留不自动分配。操作192/32/64/1/reset96/protocol48/source8/candidate2，原生严格继承1/2/8/4/2/2且尚未进入。

- 新求解器进程0，实际OP/AC/PZ0，正常TRAN0，long0，P1/P2/P3实际科学0，原生全0，安装/资料抓取0。
- diagnostic保守17/32：最初原子预扣10（六块pencil、两反例、两已知block fixture），首次精确频点预检失败额外1；第二次写完三个open pencil后无穷μ匹配失败，保留失败并对第三次重跑六pencil额外扣6。实际完成离线六pencil+四解析案例，共10最终案例，预检与失败重放全部保守计入，不能称只有10或不计失败。没有实际分析指令，不能凭“diagnostic”启动SPICE。
- 原始错误在evidence/INITIAL_EXACT_FREQUENCY_ASSERT_FAILURE.txt及INITIAL_INFINITE_QZ_MATCH_FAILURE.txt，最终stdout/stderr和events留存。修复没有删除异常频点，而是明确无穷项及有限子集资格范围。
- 七测试全部实际GREEN。四基础契约先RED→GREEN；精确频点、无穷谱以及终审报告来源回归分别先RED→GREEN。test_certificate.py与日志完整保存。初测试35非零项的期望修正是因为36保留项中g00本身为0，不是扩大实现域。
- 当前sticky科学STOP在完整离线运行后置位，后续不再科学重跑；只报告/审查/封装/通信。剩额度不解除STOP。

## 当前门

MIMO_REFERENCE_QUALIFIED=HOLD（物理块参考realization及内部pole/zero证书缺）。
GENERALIZED_NYQUIST_PASS=HOLD（真实轮廓/缺口/无穷弧与参考计数缺）。
FULL_NETWORK_PORT_CUT_PASS=PARTIAL（沿旧VCM/VEXC/ROW0实际direct；TIA仍只有loaded域有限交越）。
TIA_LOADED_DOMAIN_CONFIRMED=PARTIAL（既有loaded有限交越不等内部稳定）。
EXACT_LOW_FREQUENCY_POINTS=HOLD。
PARTITIONED_COUPLED_DYNAMIC/R2.1_NATIVE_ECO=NOT_ENTERED，BENCH_NOT_RELEASED。
旧动态/供电/温区/故障/ERC/图面HOLD全保留；directSeriesShuntQualified=false不改。

## 集中请求完整统一下一裁定

一次fresh-context终审Critical0。解析fixture的QZ误标按Important修正为实际LU/logdet；“浮点差0”按科学来源一致性提升为同一Important修复，保留真实1.57e−16。修复仅报告/回归，未新跑科学诊断。辅助reference_contract的defaultZeroWindingSufficient字段仅作参考侧前置检查，未检查真实轮廓边界与Gc内部映射：此Minor作为后续复用限制保留，不供实际稳定门调用；所有实际门仍HOLD。

请给出唯一、可实际取得的块物理参考realization/内部pole-zero证书路线，而不是另一个未经资格的端口归一化。

1. 明确Gi/GROW/GTIA/GREF是端口函数还是内部闭环特征算子；规定如何在原始OPA宏模型、不换执行器情况下取得/资格完整内部descriptor，以及pole-zero/最小性与端口对象的映射。不能把拟合状态的隐藏模态假设成已排除。
2. 明确广义Nyquist的argument-principle计数、参考RHP零/极点/内部模态，真实RHP弧和低频缺口的证据要求；负实轴接近本身不应未经定义当稳定FAIL。
3. 裁定当前极端尺度出现242/252全谱HOLD为数值方法门，给有限精度下唯一资格路线；不掩盖低频、不任意升sigma。
4. 允许在参考路线资格后才以精确frequency补0.1/1/10，不能先启动更多SPICE取得更多同类端口数据代替内部证书。

按用户要求，此正常报告集中请求适合该唯一路线的更大有界自主范围。480min已获批但本包STOP后未用额度关闭；请求下一包保留480min上限，并把主线重分配为内部参考/证明120、条件全网证书180、条件动态100、条件准备50、完整交付30，实际分析≤192/diagnostic≤32/TRAN≤64/long1≤8min。科学gate、候选/资料/协议及原生严限继承，不扩平台额度、安装/模型/系统/PCB/制造/采购/bench。只能在技术上可取得证书且新完整裁定明确允许后执行，预算请求不追认当前余量为权限。

END-OF-COMPLETE-R21-MIMO-CERTIFICATION-REFERENCE-BLOCKED-RECEIPT
FINAL-GITHUB-COMPLETE-DELIVERY
