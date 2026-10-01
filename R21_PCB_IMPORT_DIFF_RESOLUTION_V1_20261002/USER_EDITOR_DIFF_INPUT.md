历史手动输入交接，已被用户后续 Computer Use 授权及本包实际完成回执取代。保留原文作为过程证据；当前结果请看 COMPLETE_IMPORT_DIFF_RECEIPT.md。

# 下一步只取得真实差异，不直接应用

完整新裁定 assistant f81ed2e0-961f-4de1-b2aa-1b89e74ab2a2 / parent 8ce60b58-d86f-4b5d-90b7-05de270d3567，60min差异小包。当前状态 WAITING_ACTUAL_EDITOR_DIFF_INPUT；没有开始新的EDA、同步或布线，也没有删除PCB或修改原理图。

1. 打开 [已有实际原生审查文件](../R21_PCB_FLOORPLAN_AND_LAYOUT_V1/SCIENCE_ADK5556_4X4_R21_PCB_BLOCKED_REVIEW.epro2)。也可用 [公开固定下载版本](https://raw.githubusercontent.com/youyangzhou574-eng/science-adk5556-4x4-daq-review-20261001/dfd80b342744aa21625fdf693dc1b1f81333ba56/R21_PCB_FLOORPLAN_AND_LAYOUT_V1_20261002/SCIENCE_ADK5556_4X4_R21_PCB_BLOCKED_REVIEW.epro2)。当前工作副本另见 ../R21_PCB_NETLIST_INTEGRATION_AND_ROUTING_CLOSURE_V1/SCIENCE_ADK5556_4X4_R21_PCB_CLOSURE_WORK.eprj2；若界面不支持该容器，用epro2备选。
2. 打开 PCB1，选择 **Design → Import Changes**，或点 DRC 唯一 Netlist Error 的 **Import Changes** 规则名。
3. **不要直接 Apply**。把差异列表中的器件、引脚、旧网、新网，以及 added/removed/changed 信息原样返回本聊天。若界面列表为空，也记录空结果；不能据此假定原生错误通过。

前包实际 epro2 与当前工作副本冷捕获的全部非 DOCHEAD PCB 设计记录多重集合相同，布局没有丢失；该核验不代表整个工程内部或 bytes 相同，也未假称实际GUI已验证。

原因：已有官方CLI importChanges返回true，但没有差异列表；明确JLCEDA官方PCB网表全部550项与原接受网表一致，native DRC仍保留1条NetlistError。不能靠猜测删除网络或重复同步，也不能违反任务禁用ComputerUse/界面自动化的限制。此时需要实际窗口输入，不再研究API/SDK/cache。

收到输入后只分类真实差异、决定一次是否可接受同步，并核对接受原理图仍为master；再检查真实网表/冷重开/NetlistError0，之后才布线。采购、制造、Gerber、上电、bench、本地Git和系统改动仍0。

