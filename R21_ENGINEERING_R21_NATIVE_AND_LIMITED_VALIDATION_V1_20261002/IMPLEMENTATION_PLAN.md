# 08号工程执行计划

唯一包：SCIENCE_ADK5556_4X4_R21_ENGINEERING_R21_NATIVE_AND_LIMITED_VALIDATION_V1。
完整批准正文见 PRO_ENGINEERING_RULING_FULL.md；计数及时间见 EXECUTION_BUDGET.json。

1. P0（40min）：核对R2冻结输入，固定1–7kΩ验收、0.8–8kΩ保护带；列出最小ECO。十种矩阵、四选行的理想DC筛查40组，明确不代替实体精度与稳定性验证。
2. P1（120min）：最多六个优先分区短暂态，3µs切换、353µs终止；每次180s封顶。数值不收敛只记录MACROMODEL_NUMERICAL_LIMIT，已完成的明显增长/削顶或正常范围300µs失败才停止设计。重放已有32条协议回归一次。
3. P2（240min）：一份新R2工作副本；VCM/VEXC 4.99k/100p反馈、TIA22p、NRST1k及ADC Value、说明和图面最小改动。完整引脚/NC审计、冷重开、真实File原生工程和PDF；不重建168器件，不因仅ERC计数扩权。
4. P3（80min）：受控台架计划、完整报告、一次最终复核、专用公开GitHub新目录固定版本交付及配对回复接续监控。

不新增MIMO/descriptor/reference证明工具。实际bench、PCB、制造、采购、本地Git、系统修改为0。不得把数值限制称物理失稳，不把工程原生完成称全验证或制造放行。每个实际分析、协议或原生预算操作先记账再执行；失败保留。

执行安排：在已有blank宏工作点及40组静态筛查通过、前两短暂态数值限时后，P2原生可与剩余四个有界短窗重叠。08明确数值限制不作原生硬门；保留每次P1原始启动/结束时间，不扩次数或时限。
