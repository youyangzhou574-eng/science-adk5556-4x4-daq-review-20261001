# 14号局部V3V3修正

只有C_MCU1 pin1和viae255两对象。180min，copy1/session2/save2/capture4/DRC4/export1。预扣后执行，不继承13余额。实际GUI先确认PCB1及DRC对象，再按已有12mil同网局部电源规则桥接最近已连通铜；最多2局部bridge、必要1via，不移动器件/改值/改其他网/Import/autorouter/大范围布线。

先实际pre-capture和DRC、GUI点击两对象。已知API完成允许的局部铜创建（优先GUI观察而非盲坐标），不SDK研究。第一次修正后立即DRC；若仅同区域V3V3连接剩余，最多一次最小第二pass；其他网或Short/Clearance/Netlist立即STOP。Warm四类0且176/550/514/107/36与非V3V3铜不漂移才保存、正常关闭官方session与GUI、独立cold重开，先确认画布再capture/DRC。冷仍正常且局部连接持久才PCB_REVIEW_READY，制造bench不放行。

历史File909、prefixed实际907、postfixN分账；历史两个0.1mil不重建，CAUSE_UNKNOWN工程表示差异接受。POURED浮点差保留不冒称字节一致。一次整包fresh review，固定GitHub新目录全报告附件一次发Pro，同回合后续owner/nextCheck/monitor。
