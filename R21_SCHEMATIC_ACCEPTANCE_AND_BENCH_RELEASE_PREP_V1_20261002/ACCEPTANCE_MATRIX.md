# 原理图接收矩阵

| 项 | 状态 | 证据 | 边界 |
|---|---|---|---|
| 主采集拓扑 | PASS | 11Pro继承10功能追线 | 非实物性能 |
| 独立sense | PASS | FUNCTIONAL_INTERFACE_SPLIT_CHECK | 两个4.99k外侧独立 |
| 实际连接 | PASS | 514 pins107 nets36 NC176 parts | 独立冷重开 |
| 图纸主体 | PASS_WITH_COMPANION | 六页PDF+强制补充 | 独立发布HOLD |
| 注释/网名 | DOCUMENT_QUALITY_HOLD | 旧R2文字/四新网名缺字 | 不再修EDA |
| ERC | DETAIL_HOLD | 旧1209 count/no正文 | 不称clean |
| 实物性能 | NOT_VALIDATED | 本包bench0 | 容量故障时序精度待验 |
| 实物和仪器 | INPUT_UNKNOWN | 未提供样机/设备/操作人员 | 不假定可上电 |
| 首次上电 | NOT_RELEASED | 下次集中裁定Phase1 | 本包不执行 |
| PCB/采购/制造 | NOT_STARTED | 持续边界0 | 无Gerber/订单 |
