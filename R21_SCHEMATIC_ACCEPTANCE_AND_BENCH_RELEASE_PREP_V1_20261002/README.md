# R2.1 accepted schematic与受控首次上电准备

[完整回执](COMPLETE_BENCH_PREP_RECEIPT.md) · [已接受固定基线](ACCEPTED_SCHEMATIC_BASELINE.md) · [接收矩阵](ACCEPTANCE_MATRIX.md) · [Phase1 release输入](PHASE1_RELEASE_CHECKLIST.md)

原理图电气基线已正式接受：176parts/514of514/107nets/36NC、主采集和独立sense/cold PASS。旧备注/四PDF网名缺字只保留文档质量HOLD，强制companions随图纸使用，不再修改EDA。

**准备包完成不等于上电放行。样机/仪器/人员及限流/硬断电数值仍未填写，BENCH_NOT_RELEASED，PCB未开始。**

六项操作资料：FIRST_POWERUP_PRECHECK.md；57工况BENCH_TEST_MATRIX.csv；46行EXPECTED_NODE_RANGES.csv（nominal/oldideal不作放行门）；BENCH_STOP_CRITERIA.md；CALIBRATION_AND_ACCEPTANCE.md；TIMING_CAPTURE_PLAN.md。

PHASE1_RELEASE_INPUTS.json是待填写的release输入。实际探点/网成员、13项冻结SHA、旧理想引用、原裁定、预算、静态表格核对与终审全部保留。没有原生副本、EDA/仿真/新协议/实体测试。标准阵列与后续动态矩阵尚未获执行批准，首次上电只请求空载有界范围。

原始epro/PDF/actualnet/companion的固定GitHub链接在基线文件，源文件不重写、不另复制。manifest/完整ZIP用于此准备包文件完整性。
