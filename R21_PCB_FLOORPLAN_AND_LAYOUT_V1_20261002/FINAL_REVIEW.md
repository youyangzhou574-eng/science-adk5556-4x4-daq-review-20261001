# R21 PCB fresh-context 只读终审

结论：**当前包可以作为 BLOCKED floorplan / 局部布线审查证据交付；不能作为完成第一版完整 PCB、原生网络闭合、DRC clean、制造或上电放行。** 当前文档对主要失败和未完工事实已有明确披露。本轮未发现将 typed pad assignment PASS 冒称 native compiler PASS，未发现伪造原生 PDF / Gerber 或已填铜证明。Critical 0；Important 2（已披露的实际工程阻断）；Minor 3（证据和文档质量）。

本审查于 2026-10-02 进行，依据本包 `PRO_PCB_RULING_FULL.md`、`USER_PCB_AUTHORIZATION.json`、`IMPLEMENTATION_PLAN.md` 与实际保存文件。审查只读取文件及两张已有图像，只新建本文件；未调用 EDA、浏览器、其他对话、安装、仿真、设计修改、Git 写入或工具内部研究。评级基于用户实际收到的部分完成结果，不把公开 HOLD 当作隐藏失败，也不增加理论研究门。

## 本轮独立核验

| 核验对象 | fresh 结果 | 可支持的结论 |
|---|---|---|
| `PCB_FINAL_WARM_CAPTURE.json` / `PCB_FINAL_COLD_CAPTURE.json` 的实际 `parts` 和 `pads` | 两者均 176 唯一器件、550 唯一物理 pad、514 非空网络赋值、107 非空网络、36 空网 NC | 与原接受 514 pin、107 network member、36 NC CSV 逐项同名、同成员一致；不是 compiler 放行 |
| 实际器件身份 | 176 个 resolved device name / footprint name 逐项等于原接受 `FINAL_176_BOM.csv` | 没有从 global/local UUID 差异推断封装替换；不代替器件 datasheet / 制造资格认证 |
| warm / cold 状态 | `parts` 完全相同；source 全部非 DOCHEAD JSON 记录多重集合相同；rules、layerInfo 相同 | 同一工作文件冷打开后保持设计状态；raw source bytes 不同是已披露事实 |
| warm / cold source SHA256 | warm `B959F57DC9D78D24F7A668672E022281EABF2A7EC0210FBC710E2973F373DBDE`；cold `54DC579E217538C8FC6F52E20C3A6906461AD34C4AE7D356D8E6EEA8A2FD835E` | 与 `WARM_COLD_COMPARE.json` 一致 |
| 原 9 项冻结输入 | 重新读取原目录文件并重算 bytes / SHA256，9/9 等于 `FROZEN_INPUT_SHA.json` | 本轮可确认这 9 项未变；13 项 inherited ledger 没有在本轮等价于 fresh 13 项认证 |
| 原生审查 `SCIENCE_ADK5556_4X4_R21_PCB_BLOCKED_REVIEW.epro2` | 763271 bytes；SHA256 `0A7C888194A248939E6FA9C08ECD597F17FD2E4430C35FF368851C372B3F3CE3`；逐字节等于 `PCB_NATIVE_FILE.json` 实际 File base64；ZIP CRC 无错误 | 是实际导出文件，不是空壳或 LFS pointer |
| 原生 epro2 中 PCB 文档 | COMPONENT 176 / PAD_NET 550 / LINE 93 / POLY 1 / POUR 1 / ATTR 529 的 id + body 集合逐项等于 cold 捕获 | 主要实际设计内容与最终捕获对应；不宣称整个 archive 与工作容器字节或内部全工程等价 |
| 实际布局 | 激活 copper layer id 1 / 2 / 15 / 16；93 条 LINE 全为 L1、width 6 mil；1 个闭合 POLY 在 layer 11，约 100×90 mm；1 个 GND POUR boundary 在 layer 15 | 四层临时矩形 floorplan + 局部线；没有 filled plane / stitch / 全部回流认证 |
| 原生 DRC 01 / 02 / 03 | 初始 2 clearance + 452 connection + 1 netlist；第二次同样失败；最终原始树为 452 connection + 1 netlist，未列 clearance | 两条 5.9 mil 问题的失败和后续消除都有实际树证据；最终仍不是 DRC clean |
| `FINAL_DRC_DETAILS.csv` | 453 行，逐字段等于最终原始树展开；452 Connection Error + 1 Netlist Error | 明细不是仅从手写 summary 推导；452 不是 452 个独立网络 |
| 原生 netlist 比较 | `NATIVE_NETLIST_COMPARE.json` 与 `SET_AUTHORITATIVE_NET.json` 均 107 项，每项 net2 空，net1 总计 514 成员且等于原接受网络 | `setNetlist` 返回 updated/saved true 未修复官方比较；实际 pad assignment 通过不能覆盖该错误 |

`OPEN_PCB_FINAL_COLD.json` 明确从本包 `SCIENCE_ADK5556_4X4_R21_PCB_WORK.eprj2` 绝对路径打开后，执行 cold 捕获，再关闭自有 session。工作文件 LastWriteTime 05:02:36 早于后续 `setNetlist` 返回，时间戳本身不能据此判定持久化失败；本包已提供冷打开实际状态证据。epro2 是本轮核对到的主要原生审查交付，eprj2 保留为工作容器证据。

## 分级发现

### Critical

无。本轮未发现隐瞒阻断、制造 / bench 越权放行、重复 autoroute、原冻结输入变化，或实际原生文件与报称字节 / SHA 不一致。该判断限于保存文件和命令记录，不是对所有未记录动作的绝对证明。

### Important

1. **完整 PCB 交付目标尚未达到。** `PRO_PCB_RULING_FULL.md` 要求完成第一版布局布线和 DRC 审查；实际仅 93 条局部 L1 导线，最终 452 connection entries 与 1 netlist error 保留，官方 107 网 PCB members 全空。用户得到的是可审查的部分工程结果，完整 routing / native netlist integration / clean DRC 三者均 HOLD。回执和 gates 已准确披露，本审查不要求通过工具修理或额外理论门来掩盖现状。
2. **L2 连续参考面工程目标尚无实现认证。** 原始记录证明只有 GND pour 边界，未提供填铜结果、全部 GND pad 接通、stitch 或回流连续性证据；最终 GND 子树仍含 119 条 Connection Error。图中的绿色背景不是实际铜面证明。已有 gates / rules 对此保持 false / 未认证，后续常规 PCB 工程需要闭合该已有目标，当前不可放行制造或上电。

### Minor

1. **自动 warm/cold 检查的 source type 名称与实际 schema 不一致。** `finish_pcb_receipt.py` 的 `records()` 筛选 `PAD`、`POLYLINE`，实际 source 是 `PAD_NET`、`POLY`，所以 `allComponentPadTrackOutlinePourAttributesMultisetEqual` 的自动标签未覆盖真实 pad-net / outline source 记录。实际 `parts` 包含 pad 状态，且本轮独立比对全部非 DOCHEAD 记录确认真实 PAD_NET / POLY 也相同，因此没有发现实际状态不一致；修正报告或 helper 的检查覆盖表述即可。
2. **现有计数账不是所有尝试的完整账。** 原 `EXECUTION_BUDGET.json` 有 98 条 native command records，kind 分布 doc 54 / invoke 34 / session 5 / open 4 / functions 1，successful saved=true 16。WinError206 的 pre-launch 尝试和 static correction 的失败未出现在该 operations 结构中，只在失败回执描述。审查期间新增 `FINAL_ALL_SESSIONS.json` 后实际 JSON command records 为 99、session kind 为 6，原回执仍是旧 98 条口径。应统一快照截止时刻，区分 CLI command、open-created session、pre-launch 子进程 0、静态 helper attempt；不能把未批准的未来计数写成已批准额度。无需重新执行 PCB 操作。
3. **回执可读性及授权证据定位不足。** 英文大量无空格连接（如 `Actualcounts`、`allrequestsnotcurrentapproved`）降低审阅速度。`User explicitly requested larger bounded budget` 在本包两个主要授权文件中没有可逐字定位的独立引文；当前 360 min 授权和未来申请应分别引用来源。未来段已写成 requests / not current approved，未发现被冒称为新批准；可通过补证据定位和中文可读排版修正。

## 图像、超时和范围核对

两张 PNG 已实际查看。`PCB_FULL_LAYOUT.png` 展示功能器件区和稀疏局部线；`PCB_ANALOG_DETAIL.png` 展示 ROW / reference / TIA / ADC 区域，部分标签拥挤。`render_pcb.py` 使用 native 捕获的 pad geometry / L1 line 坐标、floorplan envelope，并自行绘制绿色背景与板框，属于外部重绘。它们适合粗布局审阅，不能作为原生 editor PDF、Gerber、实际 L2 填铜、丝印或 assembly courtyard / DFM 认证。现有回执已经说明该边界。

两次 50000 ms invoke 均保存 `REQUEST_TIMEOUT`（实际约 49750 ms，结果可能仍在 renderer 运行）：`ROUTE_CRITICAL` 与 `NATIVE_NETLIST_BEFORE_READ`。第一例后只读 `ROUTE_STATE_READ` 记录 176 parts / 0 lines / 1 polyline，关闭对应自有 `2a28c8a7-7c09-4246-9d7e-266084f169e7` session 后才重新打开；第二例关闭 `90c2ee56-bdcf-4437-9d3c-c17c0613f0d7` 后重新打开。已保存命令中 `autoRouting(` 仅 1 次，后续是普通局部线创建。四个自有 session 各有成功 close receipt；新增 `FINAL_ALL_SESSIONS.json` 的官方 list 也确认四者 status=closed。没有从超时返回推断成功，未见重复 autoroute 或杀其他进程的记录。

当前执行预算为 360 min；已保存预算起止 04:33:05 至 05:12:42（Asia/Shanghai），约 39.62 min，是交付预备快照，不包含后续只读终审 / 最终 list / 文档 fixpass。应在最终交付账中更新该快照口径。API `doc` / documented native calls 是当前 PCB 必要接口资料；保存文件未见 SDK / cache / DB / activation 或工具理论研究。制造、采购、bench、仿真、本地 Git 写入均没有执行记录，制造和 bench gates 均 false。未来 `PCB_NETLIST_INTEGRATION_AND_ROUTING_CLOSURE_V1` 的 360 min 和 counts 是申请，当前没有被赋予新的批准状态；本审查不批准或触发该申请。

## Declined to judge

- 原生 compiler 对 107 空 members 的根因和唯一支持的修复路径；本轮没有运行 EDA 或调查工具内部，也不把错误直接定性为电路理论问题。
- 原生 epro2 在新应用环境打开、原生 PDF / Gerber 可用性、整个工程容器内部全语义等价；本轮仅验证保存实际 File、CRC、可读 PCB 记录及已有工作文件冷打开捕获。
- 已 filled / stitched 的 GND plane、回流连续性、全部 route 完成、DFM / 生产层叠 / 厚度 / 孔径资格、装配 courtyard、机械接口最终确认。
- 主电路理论和真实封装 datasheet 重认证；本轮只核对与已接受 baseline 相同的网络、MPN 名称和 pad numbering。
- 实物性能、300 µs / 100 fps / 精度目标、采购 / 制造 / 上电 / bench release；均不属于当前已放行结果。
- accepted commit / 远端交付 / 用户真实收到的最终消息 / 未来预算批准来源的会话外事实；未调用 Git、浏览器或其他对话核查。

终审维持：`BLOCKED_NOT_FOR_MANUFACTURE_OR_POWERUP`。上述 Minor 可以做一次证据 / 文档修正，不需要修改电路或修理 EDA；公开工程 HOLD 不因此转为 PASS。
