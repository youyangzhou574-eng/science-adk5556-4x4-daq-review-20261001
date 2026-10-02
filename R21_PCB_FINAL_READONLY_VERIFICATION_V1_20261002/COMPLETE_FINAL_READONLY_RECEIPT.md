# 最终 PCB 只读验收：2 项真实 V3V3 未连接，按门停止

交付包：SCIENCE_ADK5556_4X4_R21_PCB_FINAL_READONLY_VERIFICATION_V1。
消费裁定：CIRCUIT-PRO-R21-PCB-ROUTING-IMPLEMENTATION-ACCEPT-FINAL-READONLY-VERIFY-20261002-13，assistant 283ebe11-1efa-4017-8cf6-39a0833cef01，parent user 6a6edc1e-752e-43ac-93b1-99e17437fa35。

**实际有效 warm DRC 为 Connection Error=2、Short=0、Clearance=0、NetlistError=0。工程仍是已布线候选，PCB_REVIEW_READY=false。** 两项是真实 native 明细，不是画布未激活错误。本轮没有修板；按13号“有真实电气错误保存明细并STOP”终止，独立 cold 阶段没有启动。

## 剩余的两个对象

| Net | 对象 | native primitive ID | x/y (mil) |
|---|---|---|---|
| V3V3 | C_MCU1_1 SMD pad | f92440ed9f542d81e15 | 3200.7865 / 1822.8346 |
| V3V3 | via e255 | d9d6381bb71f0d80 | 3317.55 / 1830.7 |

原始 [WARM_DRC.json](WARM_DRC.json)、[分类](WARM_DRC_CLASSIFIED.json)、[可读明细 CSV](ACTUAL_REMAINING_CONNECTIONS.csv) 保留完整错误；文字均为与同网其他对象未连接。不能把两个对象数量解释成两个独立物理故障，也不先验判定唯一修复路径。相比上包桥接前最后有效DRC的8项，本轮真正有效DRC只剩这2项；这次没有再加铜。

## 实际 GUI 与 native 获取

精确输入是上包最终保存的 SCIENCE_ADK5556_4X4_R21_ROUTING_CLOSURE_WORK.eprj2，不创建副本，不打开旧master。
project UUID 315433ef1f45b1184319722b4f2939c77ef021639b42a2c9559dabe747dba45a；PCB UUID 268e6597399ebcce。

用户明确允许本地 Computer Use。本轮用实际 GUI 观察工程名称、PCB1 页签、PCB画布和完整层栏后，才预扣一次capture、一次DRC并实际调用。此前两个自有历史窗口仍存在：官方session.close登记关闭不等于GUI窗口已退出；初次双击PCB1会转到旧窗口。本轮仅正常关闭两旧自有窗口，重观察它们消失后，再打开当前窗口PCB1，不改文件、不研究API/SDK内部。

[GUI_WARM_READY_FINAL.txt](GUI_WARM_READY_FINAL.txt)记录实际正确文档；早期project tree观察也保留，不追认成画布已就绪。唯一新session 0f4f5001-b4ba-4456-9735-fe059ed1997a、GUI窗口4395510。成功capture和DRC以后触发STOP，官方关闭，并正常关闭GUI；fresh窗口清单确认本次及两个旧自有窗口均消失。见[CLOSE_READONLY_WARM.json](CLOSE_READONLY_WARM.json)、[GUI_CLOSE_CONFIRMED.json](GUI_CLOSE_CONFIRMED.json)。未操作其他项目或浏览器。

## 温态身份核查真实通过的范围

- 176 parts / 550 pads / 514 assigned / 107 非空pad nets / 36 NC。
- 550/550 pad/net逐针与先前成功实际capture相同；176/176器件 name/footprint/device/uniqueId/manufacturerId/props/x/y/rotation 相同。
- 与最终原生File中PCB段逐对象核对：COMPONENT176、PAD_NET550、ATTR529、VIA296、POUR4、POLY1、RULE16 的ID+完整body多重集合严格相同。
- 当前rules与上包实际warm rules相同。没有删NC、补假网、改MPN/值/封装/位置。

[550针 CSV](WARM_ALL_550_PAD_NET_COMPARE.csv)、[176核心 CSV](WARM_ALL_176_CORE_COMPARE.csv)、[实际warm源](ACTUAL_WARM_PCB_SOURCE.txt)、[完整capture](WARM_CAPTURE.json)、[汇总](FINAL_READONLY_EVIDENCE_SUMMARY.json)是证据。**此处PASS只限温态身份；没有冷态PASS、最终电气闭合PASS、实体性能PASS。**

## 必须报告的原生File→重新打开画布差异

冻结上包最终File源是909 LINE；本轮实际warm画布源是907 LINE。其余907条LINE的ID及完整body完全相同，无新增/更改，只缺以下两条冻结极短线：

| ID | Net | 原端点 (mil) | 宽度 |
|---|---|---|---|
| 137f992f55430857 | VCM | (1152.4,2048.5)→(1152.4,2048.6) | 6 mil |
| 21f945bfa3a6372f | TIA1 | (1261.7,1673.2)→(1261.7,1673.3) | 6 mil |

它们没有出现在本轮实际warm源中，不能验证本轮两端附着，更不能说已证明“自动切分”或已保留同网短段。它们在冻结File中存在的历史证据不改写。本轮无编辑/save；**消失原因未独立确认，SHORT_SEGMENT_REOPEN_DIFFERENCE_HOLD。** DRC无对应short/clearance明细不等于附件检查PASS。

4个POURED对象的ID和结构/非数值内容相同，但215个数值标量存在浮点差，绝对数值差最大2.1032064978498966e-12，原始完整值保留；未做单位混同/几何舍入/过滤。数值量级很小，只能报告观测值，**不能冒称严格几何或字节相等**。POUR边界本体严格相同，未调用重铺铜。

[全对象差异](FROZEN_NATIVE_VS_WARM_OBJECT_DIFF.json)、[POURED每个数值差](POURED_NUMERIC_DIFF.json)、[两短段结果](TWO_SHORT_SEGMENT_READONLY_CHECK.json)完整保存。这是固定输入重开审计，不是工具内部研究；不为此新开EDA或重复DRC。早期离线脚本strict-all断言失败及短段缺失StopIteration暴露了真实差异，修正报告脚本保留原始输入和差异结果，未用于驱动板子修改。

## 冻结文件实际没有改变

与上一公开payload逐字节比对均PASS，见[FROZEN_INPUT_HASH_CHECK.json](FROZEN_INPUT_HASH_CHECK.json)：

- 工作eprj2：2949120 bytes，SHA FCD73BF2620447E7906D4014628F58F2C497410366B985E6FB0932D6322772BE。
- 实际原生epro2：810028 bytes，SHA 5603E205FCB5170DE00A125DCD7A6271665D78BED153E4B6B489ABEAF8F8FB6E。

两文件直接可读下载保持在固定历史commit [ce6a8fc78b7ea7b545b2c2c678484086eb8d8b85的routing目录](https://github.com/youyangzhou574-eng/science-adk5556-4x4-daq-review-20261001/tree/ce6a8fc78b7ea7b545b2c2c678484086eb8d8b85/R21_PCB_ROUTING_CLOSURE_V1_20261002)。本包copy0/export0，不用新生成伪native替代实际File；本包可读capture/source与历史File引用共同交付。

## 实耗、停止门和未执行项

120min包开始2026-10-02T01:00:49Z；真实电气错误STOP记于2026-10-02T01:07:46.302478Z。

| 额度 | 批准 | 实耗 |
|---|---:|---:|
| session | 2 | 1 |
| save | 0 | 0 |
| capture/audit | 4 | 1 |
| detailed DRC | 4 | 1 |
| review export | 1 | 0 |
| copy/edit/move/via/pour/import/schematic | 0 | 0 |
| 仿真/Gerber/制造/采购/bench/本地Git | 0 | 0 |

[EXECUTION_BUDGET.json](EXECUTION_BUDGET.json)逐项原子预扣实账。没有画布null失败capture/DRC；一次正常invoke帮助读取用于调用已知接口，没有API/SDK研究。独立cold未启动，因为真实Connection Error的STOP优先于继续冷核验。余额关闭、不结转，不以剩额度解STOP。没有自有solver启动，没有遗留pending session。

```
WARM_IDENTITY = PASS_WITH_EXPLICIT_COPPER_SOURCE_DIFFERENCE
WARM_CONNECTION_ERROR = 2
WARM_SHORT = 0
WARM_CLEARANCE = 0
WARM_NETLIST_ERROR = 0
FINAL_COLD_IDENTITY = NOT_STARTED_ON_REAL_ERROR_STOP
COPPER_STRICT_IDENTITY = HOLD
SHORT_SEGMENT_REOPEN_DIFFERENCE = HOLD
PCB_ELECTRICAL_CLOSURE = HOLD
PCB_REVIEW_READY = FALSE
MANUFACTURING_NOT_RELEASED = TRUE
BENCH_NOT_RELEASED = TRUE
```

## 集中申请的唯一下一步（仅请求，未执行）

**以下更多有界工作预算是用户明确提出的要求**，用于减少小步骤反复请示，不扩大平台额度或制造/bench权限。

建议唯一包 SCIENCE_ADK5556_4X4_R21_PCB_V3V3_MINIMAL_CONNECTION_CORRECTION_V1：180min，局部铜修正30、温冷核验45、完整交付60、异常/余量45。copy≤1/session≤2/save≤2/captureaudit≤4/DRC≤4/reviewExport≤1；componentMove0、新库0、参数/主值0、ImportChanges0、schematic0、全部simulation/autorouter/Gerber/制造/采购/bench0。

只允许针对上述C_MCU1_1与e255的同网局部连接，使用既有线宽与层规则，先由实际明细选择最小桥接，不重新布整板、不展开工具或理论研究。将907/909与两个短段缺失交由工程裁定：允许保留实际重开表示并明示原因未知，或明确其他处理；不自行删除/重建短段。完整warm/cold pad/net/core及实际铜比较+四类DRC全0才可标PCB_REVIEW_READY。若仍真实错误，保存明细停止集中报告；不盲目循环。Pro可以按实际最小范围收紧该请求。

本回执为完整阻断交付，非制造放行。下一裁定到达后全文保存、核parent及是否消费；新提交必须有本聊天owner、nextCheck及后续monitor。消息已送达不等于网页逐附件读完，不额外设置网页读回ACK门。

END-OF-COMPLETE-R21-PCB-FINAL-READONLY-CONNECTION-BLOCKED-RECEIPT
