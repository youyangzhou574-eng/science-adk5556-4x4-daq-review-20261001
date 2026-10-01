# MIMO certification and dynamic gate implementation plan

> For agentic workers: use superpowers:executing-plans inline; one final fresh review. 用户连续授权优先：不重复要求审核计划，不运行本地Git，不删除证据。

**Goal:** 先验证新块参考的数学契约与实际可证明范围，只有参考/完整Nyquist/切口/TIA加载域全部通过才允许新求解及七宏动态。
**Architecture:** 先只读固定2e2829f版本及本地SHA一致的20列Gc；构造明确ROW4/TIA4/REF2主块候选，原始频点全部保留。用独立已知状态空间反例检查参考零点/隐藏模态/轮廓契约；不能将边界端口频率采样等同内部稳定证书。
**Tech:** 现有Python/NumPy/SciPy；现有ngspice47仅条件进入，不安装。
**Spec:** PRO_CERTIFICATION_RULING_FULL.md（assistant c1c48dcc-32ce-414d-b185-bdd829952edd）。

## Global constraints

- 新480min上限；阶段90/150/100/80/30min合计450，余30为全局保留，不能自动给某阶段。
- OP/AC/PZ192、diagnostic32、normalTRAN64、long1≤8min；reset96/protocol48/sources8/candidate2。
- inherited stricter native1/session2/save8/captureaudit4/ERC2/PDF2，仅动态后且解释P3为准备/条件ECO；未过门全部0。
- 先不跑新SPICE；不对称重建；不改模型/OPA/Rf/Cf/补偿，不PCB/bench/Git/系统。
- reference没有RHP pole只是必要条件：若detG0含RHP零或端口不可观测内部RHP模态，不能以N=0单独作稳定证书。未知项HOLD，不换定义冒称批准。

## Review focus

- 隐藏RHP内部模态：相同端口传递也必须保留不可识别HOLD。
- 参考RHP零与pole区分：不能用无RHP pole代替参考det无RHP零。
- 有限虚轴/直线闭合proxy：不能冒称真实RHP轮廓资格。
- 块主子矩阵仅代数候选：需验证物理参考实现及内部极点，不因取块自动PASS。
- 新预算与旧STOP隔离；离线计diagnostic，新实际求解0；后续门未过禁止发起。

## Task 1 — contract proof and diagnostics

Files: test_certificate.py, certificate_contract.py, diagnose_blocks.py, results/, evidence/.
Consumes: frozen NEW_GC.npz, original GATES.json, ruling.
Produces: exact state-space counterexample certificate, block candidate finite-axis evidence, full source/hash/budget ledger.

- [ ] TDD：hidden unstable state必须识别为不能由同端口证明；RHP reference zero必须阻止默认N0判定；block分区完整且互不重叠，closed topology来源匹配。
- [ ] 运行RED；实现最小证明辅助；运行GREEN。
- [ ] 同一冻结频率/固定尺度3种，分别两拓扑块参考QZ/LU，仅离线证据，不物理稳定结论。
- [ ] 若缺内部参考证书/真实RHP复频率响应则方法HOLD，关闭P1/P2/P3，不为端口数据缺信息新求解。

## Conditional later tasks

- [ ] Task2 P1真实参考实现/内部pole-zero证书与完整Nyquist；仅Task1资格闭合且没有数学契约阻碍才能进。
- [ ] Task3 P2七宏353us/3us；必须MIMO_REFERENCE_QUALIFIED/GENERALIZED_NYQUIST_PASS/FULL_NETWORK_PORT_CUT_PASS/TIA_LOADED_DOMAIN_CONFIRMED。
- [ ] Task4 P3原生准备/条件最小ECO；动态PASS后沿严格继承门。
- [ ] Task5 P4完整或阻断报告+SHA+CSV固定GitHub版本，集中申请唯一下一路线；一次send，历史对账、完整裁定检查、owner+后继monitor。

Ruling: 新裁定阶段总和450不等480，采用全局480与各阶段分别上限，30保留不支出；若解释错只会少用预算。
Ruling: 指定块采用Gc主块只是离线candidate，绝不宣称已物理实现；缺内部/参考资格不能用新增SPICE掩盖信息缺口。
