# 一次 fresh-context 完整工程包终审

审查日期：2026-10-02。范围：R21_PCB_MANUFACTURING_PREFLIGHT_READONLY_V1，按16号裁定、IMPLEMENTATION_PLAN.md及 executing-plans 的 whole-package final review 执行。仅阅读已有文档、CSV、JSON、脚本和指定PNG；本审查未执行脚本、CAD、DRC、仿真、导出、联网资料查询、工具安装或新几何计算。唯一写入为本报告；未派生审查代理，未开展第二次review。

## 结论

**只读制造前审查包可以交付；Critical 0、Important 0、Minor 3。制造、采购、台架及上电仍未放行。**

没有发现本包遗漏了一个已被现有证据证实、必须立即修改PCB的无条件ECO。此结论不等于封装/工艺全合格，更不等于工厂CAM/装配接受。矩阵的PASS限于各行scope；G04/G18/G20/G22和C01–C10等PENDING不得因本报告消失。

## 已核实的优点与关键边界

- PRO_MANUFACTURING_PREFLIGHT_RULING_FULL.md冻结了e9c1b72基线，接受既有电气DRC与cold reopen。本包G01明确继承而未重新运行DRC，GATES.json将MANUFACTURING_RELEASE、BENCH_RELEASE、PROCUREMENT_RELEASE全部保持false。
- FABRICATION_INPUT_CONTRACT.md、MANUFACTURING_OPEN_ITEMS.md第1–3项及矩阵G04/G20保留6mil与铜厚的适用限制，U9/U10约0.090081mm、U5约0.096774mm的mask桥估计没有被当作满足0.10mm工艺。NATIVE_SAME_PACKAGE_MASK_GAPS.csv和ASSEMBLY_GEOMETRY_SUMMARY.json支持这些已记录估计，脚本方法限同封装几何距离减mask扩展，未声称Gerber/CAM结果。
- 实际查看ASSEMBLY_AND_PROBE_REVIEW.png及sources中的LM73100 p50、TPS3890 p25、ADS8684 p66、BAT54S p5 PNG。LM的5/6长焊盘、corner land和混合节距，TPS的1–3 SMD/4–6 NSMD示例，ADS的38脚/0.5mm与1.5mm示例land，以及BAT54S的2+1针图均与文档所限定的结论相容。TPS/ADS及ST land差异已列PENDING，未用pin-count PASS替代装配批准。
- 175个nominal body无2D相交仅作为有限筛查；U6缺支持body、courtyard/3D/工具空间未知均明确列出。脚本读取layer48、图中red marking来自layer49，与“非生产丝印认证”说明一致。
- NATIVE_550_PAD_GEOMETRY.csv:2–3、153–170显示J1/J4约1.1mm、J2约1.0mm、J3约1.2mm原生孔；不会把API摘要的1/10尺度或polygon假孔误判ECO。FROZEN_176_MANUFACTURING_BOM.csv:2、69–71保留四个generic header空Manufacturer/MPN；Description不在字段中。
- EXTERNAL_ARRAY_J2_WIRING.md的J2.1–8 ROW0–3/COL0–3对应NATIVE_550_PAD_GEOMETRY.csv:153–160。现有接口为单排8针2.54mm，成品双排IDC不能直接插，线缆/阵列端和具体MPN待输入；没有宣称排线接入已完成或默许CAD修改。
- SOURCES.json保留六来源范围和ST HTTP567失败，无伪造本地PDF SHA。OPA/TMUX针映射明确继承既有接受，不声称本次额外官方复查。finish_preflight.py记录前后清单相等检查；冻结native SHA在BEFORE:336及AFTER:338一致。审查读取此记录而未重新hash全部原始文件。

## Critical

无。

## Important

无。本包确有工艺及机械待项，但已在合同、矩阵和openitems明确阻止制造放行，不重复计为报告缺陷。

## Minor（建议记账，不触发新的分析或CAD）

1. **PGOOD候选文字与图/CSV引用不统一。** ASSEMBLY_AND_TEST_ACCESS_CHECKLIST.md:21、MANUFACTURING_PREFLIGHT_MATRIX.csv:24写R_RST.2；EXISTING_TEST_ACCESS_CANDIDATES.csv:8及图索引7实际为R_J3_5.2。NATIVE_550_PAD_GEOMETRY.csv:237、253证明两者都接PGOOD，因此不是错网或危险探点，但查图时会定位到两个相隔较远的位置。以后普通文档统一以CSV选定R_J3_5.2为主，或明确R_RST.2只是另一个同网候选；无需重新运行探点选择。

2. **nativeDrill20PTH键名不能直接当钻孔清单使用。** assembly_and_access.py:78以`nativeDrill_mm is not None`筛选，ASSEMBLY_GEOMETRY_SUMMARY.json该数组尾部因此也包含U6的三个0.0mm、layer1 pad。二十个真实连接器PTH和报告孔径结论没有因此改变；但后续读者不可用这个数组长度作为钻孔数。保留原始输出，注明仅正孔径且具有对应PTH层语义的条目才是钻孔；当前不生成drill文件，不需重算。

3. **OVAL被矩形包络近似，方法说明应更明确。** assembly_and_access.py:32–33对非POLYGON且非ELLIPSE形状使用box；NATIVE_550_PAD_GEOMETRY.csv:485–516实际标U7为OVAL。它在此图/距离筛查中是保守矩形包络，不能读作U7完整真实圆角land渲染。主风险U5/U9/U10并非由该OVAL近似产生，且全部输出已限定非CAM，所以不推翻本次PENDING结论；以后只需补记此近似，不为本minor开启重算或工具修理。

## Declined to judge

- 工厂最终可制造性、mask桥可接受性、厚铜线距、最终孔公差和装配良率：尚无选定工艺/CAM/assembler contract，本包有明确PENDING；本报告不替工厂放行。
- 176全器件极限courtyard、3D、生产丝印和插接工具空间：已有证据只覆盖175 nominal body及有限标记；不把缺少完整几何等同已证明碰撞。
- 外部阵列、成品线缆或IDC系统真正接入可用性：用户尚未给实际连接器/线缆/阵列端输入，J2针网表只能证明板端电气接口，不能证明机械配对落地。
- 新的器件内部pin-function重验证与第七份资料查询：接受既有电气基线，只核本包声明范围，不扩资料上限。ST未下载本地PDF这一限制已公开，未将其当完整可重复离线原件证据。
- 实体探测安全、上电、时序/测量性能、SI/PI/热/模拟稳定性：只有现有pad候选，无实体release，16号明确不批准这些测试或新计算。
- 全部操作历史的独立取证、94个源文件重新hash、远端公开交付/固定commit可达性：本review读取保留的记录、脚本和本地包，没有执行新命令来重证历史，也未网络访问远端；公开交付仍须执行者另作交付确认。

终审收口：交付本只读报告及明确PENDING即可；不需再次review，不因三个Minor开启CAD、资料扩展或科学重算。
