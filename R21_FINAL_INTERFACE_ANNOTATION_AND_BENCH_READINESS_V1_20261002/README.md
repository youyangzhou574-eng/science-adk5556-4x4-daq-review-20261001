# R2.1独立sense接口修正审查包

[完整回执](COMPLETE_FINAL_INTERFACE_RECEIPT.md) · [真实拓扑接线图](INTERFACE_TOPOLOGY_COMPANION.md) · [图纸备注补充](DRAWING_ANNOTATION_ADDENDUM.md) · [台架输入合同：未执行](BENCH_VALIDATION_PLAN.md)

实际176parts/514of514/107nets/36NC，独立冷重开PASS。仅四针由共网拆成SWD/UART两独立外侧sense，每条4.99k，510其他针及元件主值不变。CORE拓扑由10号Pro独立审查通过，不代表实物指标。

**最终PDF页5四个新端口网名未打印，旧R2备注也仍在；必须连同接线图和补充阅读。BENCH_NOT_RELEASED，禁止按此审查包装配制造上电。**

- 原生：SCIENCE_ADK5556_4X4_R21_FINAL_INTERFACE_REVIEW.epro2；工作副本.eprj2；六页PDF与六PNG。
- 实际证据：FINAL_514_PIN_NET_CHECKS.csv、FINAL_107_NETWORK_MEMBERS.csv、FINAL_36_NC.csv、FINAL_176_BOM.csv、两actualnet、全页source。
- 结构复核：FUNCTIONAL_INTERFACE_SPLIT_CHECK.json、COLD_REOPEN_COMPARE.json、FINAL_COLD_AUDIT.json。
- 限制：GATES.json、DRAWING_VISUAL_REVIEW.json、ANNOTATION_SINGLE_ATTEMPT_RESULT.json、ACTUAL_FILE_TEXT_ENCODING_NOTE.json。
- 原裁定/计划/预算/闭会话/冻结源SHA与全部原CLI证据保留。

本包新仿真/新协议/实际bench/PCB/制造/采购0；原生硬额度已用尽，禁止自行继续修字。公开manifest逐文件SHA及ZIP用于完整性核对。
