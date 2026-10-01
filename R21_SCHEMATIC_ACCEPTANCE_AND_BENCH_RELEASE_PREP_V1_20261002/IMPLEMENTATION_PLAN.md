# 11号只读工程准备计划

P0：保存完整裁定，确认已消费消息，冻结13项基线SHA和接收矩阵。P1：用既有真实网络/厂家资料/旧理想DC筛查，整理工况和节点表。P2：准备预检、停机、校准/时序及Phase1 release输入。P3：单次只读终审、完整报告、GitHub固定commit一次性交付、同回合接续回复owner/monitor。

不新增科学测试/仿真/解析/协议/EDA/原生副本/bench/PCB/采购/制造；不把旧候选reset或理论证书移入当前实际接线。用现有Node/Python及bundled Artifact Tool静态制表，不安装任何软件。用户指定CSV为输出，不增加xlsx变体；CSV来自Artifact Tool表格values的标准CSV序列化。非科学表格结构检查不冒称实验。

Ruling：电源限流、具体供电合格/断电数值、允许上电次数时长、实物/仪器身份未知不虚构；以待Pro release+实体信息为字段。成本若误把名义值当断电门会导致错误上电，故每行显式区分nominal/ideal/PENDING_RELEASE。
Ruling：只读引用旧40组理想DC数值，不重新求解，也不把理想驱动裕量作器件/实物保证。成本若越界会错误放行；表格保留来源和scope。
