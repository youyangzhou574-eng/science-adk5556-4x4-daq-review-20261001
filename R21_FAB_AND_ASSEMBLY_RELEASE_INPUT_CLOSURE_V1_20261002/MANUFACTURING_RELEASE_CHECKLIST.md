# 放行清单
MANUFACTURING_RELEASE_CHECKLIST.csv是当前分项authority；HISTORICAL_PREFLIGHT_MATRIX_R16.csv保留原阶段输入，不覆盖18接受状态。
- 已有PASS：原理图/电气PCB/温冷/实际J2针序与2D封装。PCB_REVIEW_READY=true。
- 下单前必填：厂商、数量、实际层叠铜重/厚度/finish、生产文件和用户制造采购权限。已有默认合同可询价；不是所有参数都空着。
- CAM必须确认：细桥、J2八个tightfinishedhole、via环/孔位、既有4milspace规则、钻孔对分类、实际生产数据/拼板。
- 装配输入：J1/J3/J4准确manufacturer/MPN；真实线径OD/端子/压接；CPL/极性/钢网/回流与检查方式；线束真实连续记录。
- 不要求重开PCB的事项：J2缺ROW/COL文字已接受但companion强制；genericdevice/旧3D仅正确MPN与几何authority覆盖；历史UTF8/909911不作为工具研究。
- 物理能力保持待验：参考有效容量/100fps/WCET/300us/温区/故障/真实精度、SWD及首上电。PCB审查就绪不等于制造或bench放行。

若厂商实际拒绝某CAM条件才带具体差异集中报告，获新范围裁定前不自动改板。当前没有真实factory答复、没有Gerber、没有询价下单、没有physicalsample。
