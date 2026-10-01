# 08 Engineering receipt — BLOCKED / DO NOT USE NATIVE

本包因我实施ECO后出现实际pin-net错误，依08第7条停止。没有新合格R2.1原理图；所有BLOCKED原生/PDF只作失败证据，禁止装配/制造/上电。

先读 [完整回执](COMPLETE_ENGINEERING_RECEIPT.md)、[门状态](GATES.json) 和 [预算](EXECUTION_BUDGET.json)。工程正常范围1–7kΩ、~10%变化，0.8–8kΩ保护带；不再研究MIMO/descriptor证明。

| 可读附件 | 内容 |
|---|---|
| DC_ENGINEERING_40_GROUPS.csv / DC_ENGINEERING_SUMMARY.json | 40组选行理想DC / 160单元输出；非实体精度证明 |
| MACRO_BLANK_OP.csv / TRANSIENT_OBSERVED_LOG_ENDS.csv | 6次blank OP、6次180s有限TRAN未完成；完整切换trace0 |
| PROTOCOL_FINAL_RUN.log / PROGRESS_FINAL_RUN.log | 21+11=32实际离线回归PASS，硬件WCET/100fps待验 |
| BASELINE_COPY_AUDIT.json | 复制后498/498、104网、36NC PASS |
| POST_ECO_ALL_514_PIN_CHECKS.csv / POST_ECO_AUDIT.json | ECO后334/514，180错误，99实际网/106目标网 FAIL |
| PLACEMENT_COLLISION_DIAGNOSIS.json | 4新电容重叠4旧器件，造成网络合并 |
| ACTUAL_BLOCKED_BOM.csv / MINIMAL_ECO.csv | 实际176器件字段、计划最小ECO；不能作为合格BOM |
| NATIVE_PAGE_1..6_SOURCE.txt | 各页真实原生源码，可读导出 |
| BLOCKED_PDF_PAGE-1..6.png / PDF_VISUAL_REVIEW.json | 六页实际render/view，超大重叠标签，图面FAIL |
| BENCH_VALIDATION_PLAN.md / TIMING_ARITHMETIC.json | 仅准备的受控台架计划、算术时序，不是上电授权 |
| *.epro2 / *.eprj2 / *.pdf | 明确失败副本，BLOCKED_NOT_FOR_USE |
| cases/ / models/ / 原始JSON及日志 | 全部初失败、命令/终止、模型来源SHA、真实File和实际网表证据 |

没有冷重开、没有新ERC/DRC、没有实际bench/PCB/制造/采购/本地Git/系统修改。仅申请下一240min原生连接及图面修正包；未批不执行。历史理论HOLD保留但不成为新原生准入门。
