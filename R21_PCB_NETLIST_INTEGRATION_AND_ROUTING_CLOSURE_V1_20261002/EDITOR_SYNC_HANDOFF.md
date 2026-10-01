# 唯一可操作的编辑器交接

不是要求修软件或重新设计电路。请在嘉立创专业版打开本包 SCIENCE_ADK5556_4X4_R21_PCB_CLOSURE_WORK.eprj2 的 PCB1，在 DRC 的唯一 Netlist Error 行点击规则名 **Import Changes**。这是保存的原生错误正文明确提供的操作。查看并保存弹出的原理图/PCB差异明细，尤其是哪一器件/哪一针或哪个属性；不要直接接受改网或新器件，不改原接受原理图。

请把实际差异明细及必要操作回传本聊天，或由网页指定一条已支持的、可操作的编辑器同步路线。若差异窗口为空，也记录真实空结果，不能解释成 Netlist Error 自动通过。本包已做一次官方 importChanges+save，实际全部176/550及非DOCHEAD记录未变，冷DRC仍1条Netlist Error。没有继续查API/SDK/cache或再尝试全板autoroute。

只有确认该网络整合门通过才继续手工关键模拟布线；现在不要下单、出Gerber或上电。已有100×90四层布局及93段局部线保留，不推翻布局。

若界面不支持直接打开 eprj2 工作容器，可打开 [前包实际原生 epro2 固定版本](https://github.com/youyangzhou574-eng/science-adk5556-4x4-daq-review-20261001/blob/dfd80b342744aa21625fdf693dc1b1f81333ba56/R21_PCB_FLOORPLAN_AND_LAYOUT_V1_20261002/SCIENCE_ADK5556_4X4_R21_PCB_BLOCKED_REVIEW.epro2)。PRIOR_PCB_DESIGN_RECORD_EQUALITY.json 已只读核验前包 native 捕获与本包冷 C 的全部非 DOCHEAD PCB 设计记录多重集合相同；不宣称整个工程内部或原始 bytes 等价。请记录实际打开工程后取得的差异，不把此打开备选说成已经在 GUI 验证过。
