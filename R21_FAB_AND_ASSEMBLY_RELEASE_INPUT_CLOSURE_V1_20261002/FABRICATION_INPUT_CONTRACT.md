# 四层实验室验证板制造输入合同（推荐版，尚未下单）
18号接受的电气PCB/J2基线固定于 [17包commit](https://github.com/youyangzhou574-eng/science-adk5556-4x4-daq-review-20261001/tree/bcafa5c6b834c20539774cd335d34586442453be/R21_EXTERNAL_ARRAY_PLUGGABLE_INTERFACE_AND_FAB_INPUT_CONTRACT_V1_20261002)；原生SHA801149F292E86CF34AB2872F177125099D640421B48B62F3F9044EF2151DB241。没有新CAD、DRC、导出或Gerber。本轮给出确定的推荐参数，厂商及真实CAM接受保留待填。

推荐FR-4四层、100×90mm、1.6mm nominal、外/内各1oz、绿色阻焊、ENIG、普通贯通via、铣外形。参照厂内层默认0.5oz，故内1oz需明确选择；不默认加厚2oz。层顺序保持Top/L2 GND/L3供电/Bottom；实际core/prepreg厚度、料号与总厚公差由厂商最终stackup确认。无受控阻抗要求。
默认详表见DEFAULT_FAB_PARAMETERS.csv；参数状态明确区分已有设计、推荐输入和待CAM，不把建议当用户选厂/下单。

必须单列的CAM项：
- 原生最小线宽6mil，但冻结TrackTrack规则约4mil。不能只选择6/6mil能力并声称全部适配；须覆盖既有4mil间距规则并由实际生产资料复核。pad-track约6mil、pour10mil，不统一替换。
- 297贯通via名义孔0.3048/盘0.6096，环0.1524mm贴近参照厂多层1oz绝对下限。名义几何不是加工孔位容差保证。
- J2厂家finished PTH为1.14±0.05mm（1.09–1.19）。普通参照通孔+0.13/-0.08mm落到1.06–1.27，不满足同一合同。须订单逐列J2八孔特殊公差并取得书面CAM/工艺确认；不得把焊接连接器误称为press-fit。参照厂“press-fit孔”±.05服务条款不自动适用于J2焊接孔。厂商拒绝时集中报告具体工艺差异，不擅自改孔/改铜/换件。
- U5/U9/U10既有阻焊桥约0.096774/0.090081/0.090081mm低于参照绿色0.10mm。标FAB_CAM_CONFIRM_REQUIRED：厂商决定是否能够保留或需批准并窗，装配厂确认桥风险/钢网。没有授权现在修改footprint或native openings。
- 历史最小孔边间距0.31115mm仅旧只读screen，当前未重做孔对类别资格。不同via-via/pad-hole规则不能混用；完整钻孔分类由CAM核查，不能称严格CAM PASS。
- 极小原生丝印和完整mated空间/装配工具空间按实际工艺确认；不因此自动返工已接受PCB。

板厂待填FABRICATOR_PENDING；板数、服务档、实际材料/层叠、J2孔公差、阻焊桥、via环/孔间距分类、钢网/拼板/e-test接受号等待真实输入。未生成制造文件、未联系厂商、未下单。[官方能力参照](https://jlcpcb.com/capabilities/pcb-capabilities)只支持一般可用工艺，不是本板放行。
