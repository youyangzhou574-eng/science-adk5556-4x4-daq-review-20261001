# 09号原生修正执行计划

仅从冻结R2新建唯一副本，旧08失败工程与所有历史证据不变。采用现有官方CLI和既有实体库身份，不新增仿真、理论研究或库查询。

1. Audit A: 新副本实际File全量168parts/498连接/104nets/36NC。
2. Page1四无源件和两反馈端口删除重建；save1，Audit B实际File。空白位置先核器件针、wire/port/junction。
3. RESET真实1k与ADC四Value修正先完成；TIA四22p仅置于核过空白位置，save2；Audit C实际File验收最终176/514/106/36。
4. 默认字号保持，必要位置与说明调整。先收集所有页面核心字段与引脚/NC/导线/端口快照（不是新实际File capture）。PDF1六页查看，最多一次局部整理/PDF2。ERC一次，只有count就保留HOLD。
5. 关闭自有session，第二session独立冷重开；Audit D第四次实际File，同时承担最终验收，比较Audit C网络成员与关前核心字段快照，避免把A/B/C/D再加冷重开变成5次capture超过4硬限。
6. 只整理台架计划，完整GitHub新目录固定版本一次性交付；同回合恢复回复owner和monitor，不发完就停。

Ruling: 最终D与冷重开capture合并为第四次；C在RESET/ADC也已落实后承担关前全量实际File检查，关前图面整理后只用官方源/实体状态快照确认电气坐标、对象、字段未改。成本是若整理触及电气，则必须停而非越限追加capture。

240min分P0 60/P1 90/P2 30/P3 60。copy1/session2/save6/captureaudit4/ERC1/PDF2；库/资料/候选及所有新仿真/解析/协议0。普通标签字号/元数据修正自主进行；09列明工程STOP及硬限必须遵守。

不运行本地Git写命令。新目录隔离替代Git worktree；不安装或开发新的工具体系。一次最终fresh-context交付审查；保留所有源与失败，不删除历史。
