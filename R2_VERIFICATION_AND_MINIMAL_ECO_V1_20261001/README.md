# R2.1 实际模型验证与最小ECO候选 — 阻断交付

项目 SCIENCE_ADK5556_4X4_DAQ_REPLICA，独立电路仓库。本版没有生成新的原生工程，BENCH_NOT_RELEASED。

先读 [完整回执](COMPLETE_R21_RECEIPT.md) 和 [新裁定全文](PRO_R21_GATE_FULL.md)。ngspice实际资格通过，八状态及接收契约21测试通过；单环路/单TIA有真实原厂模型结果，整板耦合暂态未闭合，复位/完整≤10ms门仍有缺口。

| 材料 | 入口 |
|---|---|
| 完整回执与范围 | [COMPLETE_R21_RECEIPT.md](COMPLETE_R21_RECEIPT.md) |
| 执行索引/原始日志 | [CASE_EXECUTION_INDEX.csv](CASE_EXECUTION_INDEX.csv)、[results](results/) |
| 单环路指标 | [LOOP_METRICS.json](results/LOOP_METRICS.json)、[可读曲线CSV](readable/) |
| 有效采样边沿 | [完整单TIA指标](results/TIA_R2_FULL_STATE_METRICS.json)、[事件表](results/EIGHT_STATE_EVENTS.csv) |
| 波形图片 | [资格](plots/P0_QUALIFICATION.png)、[环路](plots/SINGLE_LOOP_SCREENS.png)、[单TIA边沿](plots/SINGLE_TIA_VALID_EDGES.png) |
| 数据资格代码/测试 | [protocol.py](protocol.py)、[test_protocol.py](test_protocol.py)、[测试日志](results/PROTOCOL_TESTS.log)、[旧反例](results/LEGACY_COUNTEREXAMPLES.json) |
| 复位与时序候选 | [RESET_AND_TIMING_CONTRACT.md](RESET_AND_TIMING_CONTRACT.md)、[角点](results/RESET_CORNERS.json) |
| 容量与保护路径 | [CAPACITANCE_AND_PROTECTION.md](CAPACITANCE_AND_PROTECTION.md) |
| 统一误差口径 | [UNIFIED_ERROR_BUDGET.csv](UNIFIED_ERROR_BUDGET.csv) |
| 原厂模型/算例 | [models](models/)、[cases](cases/) |
| 执行器与原厂来源 | [sources](sources/)、[原始官方便携包](runtime/ngspice-47_64.7z) |
| 实耗与校验 | [EXECUTION_BUDGET.json](EXECUTION_BUDGET.json)、[文件清单/SHA](MANIFEST.csv) |

未改的R2输入保持 [固定commit da6ca87b](https://github.com/youyangzhou574-eng/science-adk5556-4x4-daq-review-20261001/tree/da6ca87b9f49c5af03a16c24af6186d7c5c2e0d3/FIRST_BUILD_ELECTRICAL_CLOSURE_AND_SCHEMATIC_R2_V1_20261001)，无须重传。

本目录逐文件可读交付，无LFS指针；原始二进制执行器仅为复现附件，报告/表格/波形直接可读。原厂资料均带来源及限制。本版不会因单环路或软件结果自动解除既有HOLD，也不会自行恢复旧预算。
