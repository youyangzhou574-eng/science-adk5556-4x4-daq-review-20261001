from b31_core import *
import hashlib
a=json.loads((P/'FINAL_READONLY_AUDIT.json').read_text());chains=json.loads((P/'DIGITAL_INTERFACE_CHAIN_AUDIT.json').read_text())['signalPaths']
assert a['readOnlyQualificationPass']
g={'B31_METHOD':'PASS_PER_NEW_PRO','B31_CHANNEL_CELL_STRUCTURE':'PASS_FRESH_READONLY_ROLE_GEOMETRY','B31_GEOMETRY':'PASS_FROZEN_OFFLINE_GEOMETRY','B31_KEY_LOCAL_RELATIONSHIPS':'PASS_FRESH106','B31_ROW_LENGTH_TRADEOFF':'ACCEPTED_PLACEMENT_ONLY_PER_PRO','B31_POWER_INPUT_TRADEOFF':'ACCEPTED_PLACEMENT_ONLY_PER_PRO','B31_ADC_IN2_TRADEOFF':'ACCEPTED_PLACEMENT_ONLY_PER_PRO','B311_ACTUAL_DIGITAL_INTERFACE_CHAIN_AUDIT':'PASS_READONLY_5_FUNCTIONAL_PATHS','B31_OLD_MACRO_SCORE_ALL_CANDIDATES':'HISTORICAL_INCOMPLETE_NOT_RERANKED','CAD_RELEASED':False,'USER_VISUAL_ACCEPTANCE':'PENDING','manufacture':False,'bench':False,'nativePCB':False,'FFC_ACTUATOR_EXACT':'HOLD','DYNAMIC_PERFORMANCE':'HOLD','scienceSTOP':'NO_MORE_OFFLINE_PLACEMENT_WAIT_USER_VISUAL_SELECTION'}
save('GATES.json',g)
rows='\n'.join('|'+q['insideNet']+'|'+' → '.join(q['orderedNodes'])+'|'+f"{q['segment1Mm']:.6f}|{q['segment2Mm']:.6f}|{q['resistorPadSpanMm']:.6f}|{q['functionalLengthWithResistorSpanMm']:.6f}|{q['stretch']:.6f}|" for q in chains)
text='''# SCIENCE_ADK5556_4X4_R21_B311_DIGITAL_INTERFACE_CHAIN_QUALIFICATION_V1

## 完整回执：只读数字接口链核查完成，坐标冻结，等待用户视觉选择

Pro 完整新裁定 assistant37efc212-6324-4660-b4fd-4515d069eeb4，parent13478bd1-472f-4a96-8879-1b79a51ac428，批准本150min唯一资格包。已明确接受ROW0/3+7.31/+7.39mm、J1→U9+2.55mm及ADC_IN2+.15mm为placement阶段非阻断取舍，未声称动态性能或电源工艺已验证。完整原文保存，旧B31HOLD不回写；本包不重新优化这些已接受的链。

本次按实际冻结pin-net核查UART TX/RX、SWDIO/SWCLK、NRST五条功能链，经两焊盘串联R跨越 *_EXT 网名变化，没有再把同名网络检索误作完整功能路径。每条计算MCU针→R内侧针与R外侧针→连接器针两段直线；R内部pad跨度单列，也给出包含跨度的完整代理路径。路径为无方向几何关联，UART_RX/SWD/NRST不假称MCU输出，虚线不是铜线。

| 网络 | 实际完整节点 | 第一段mm | 第二段mm | R针跨度mm | 总功能跨度mm | 相对直达端点stretch |
|---|---|---:|---:|---:|---:|---:|
'''+rows+'''

五条均通过本包事前声明的有限几何筛查：总跨度/端点直达<=2，总跨度<=2×max(实际四SPI平均，MCU至J3/J4中心尺度)+5mm；J3/J4在整体几何右缘内缩<=2mm。阈值是桌面端对Pro定性“无明显绕远、与当前区域尺度匹配”的保守工程解释，不是Pro原文硬电气标准，也不证明实际波形、信号完整性、ESD、SWD速率或UART时序。参考尺度17.804493815mm、长度筛查40.608987630mm；实际总功能跨度15.2243–19.4591mm、stretch1.1352–1.4710。J3/J4右缘距全部physicalbbox右缘约1.18193/1.18195mm，接口仍同列位于规划右边缘；尚无板框，不能声称制造板边距合格。

NRST实际U7.6=PGOOD，经R_J3_5.2/1到J3.5=MCU_NRST_EXT。另记录U11.6、U12.6、U15.2的PGOOD同网支路；U15.4=PG_OK_FAST的逻辑后级不混成NRST同网。D_J保护件pad3信号、pad1GND、pad2V3V3列出但不当作可串通GND/电源的路径，不因此解除故障保护HOLD。两条V3V3参考端经4.99k到V3V3_EXT_SWD/UART单列为sense-only，不供电；U7.4只是该rail几何参照点，不叫供电源。没有新增硬件试验。

## 冻结与全量核对

所有176坐标/角度原字节不变，保持B31唯一完整PASS1；无局部数字修正，不动19锚点、TIA/ROW/ADC/Power或任何原生文件。18项原输入与副本SHA一致，包括继承旧HOLD的GATES文件（新包重命名明确为历史）。完整176/552/514/107、36ordinaryNC+2emptyJ2MP；J2.1–4ROW0..3/.5–8COL0..3/MP1/2空保持。
新只读检查15400对body/proxy相交0、minproxygap.18606mm；106距离全部不增、最大delta−.305972mm；完整TIA24/ROW16角色中心/方向重复保持，非三脚clamp所有railpad精确镜像。只是冻结离线geometry/source metadata，不是实际CADnetlist/DRC，也不扩为全电气性能。旧六区reuse证明按冻结相同坐标继承，未重跑优化；本包宏候选0。

旧Macro B1/B2评分缺数字串联接口链的历史证据保留。本包直接核查最终布局的真实链，不补写旧候选分数、不中途重选B2、不声称过去全候选排序已资格。Pro规定实际链正常即冻结，不值得再开大规模placement，因此coordinatePasses=0。原first-pad score遗漏已由旧B31修复；本包新增三测试：跨串联R重命名功能路径缺失RED→GREEN、缺外侧针不得造路径、空NC不得join。RED使用direct-only缺失输出的隔离baseline，不是重新运行旧Macro评分模块；实际五条全部从原552pin重算。

## 图和预算

唯一B311_FINAL_FROZEN_PLACEMENT.png为当前实际176件离线终稿候选图，加完整8channel contours和5实际接口两段路径关联。实际查看后报告图面限制；不是原生PCB截图、不是布线或板框。用户尚未确认视觉选择，CAD_RELEASED=false。局部普通件designator需原CSV/552pinCSV兜底。
批准150min：只读chain50/条件局部45/全audit25/单图交付30。实耗macro0/0，coordinate0/1，image1/1（导图后填写预算）；条件移动未触发。所有CAD/API/native/routing/outline/newsource/toolresearch/simulation/Gerber/采购制造bench/localGit/system0。没有以尚余45min局部额度开新placement，图满不额外polish。
FFC实际类型仍为薄软排线插槽，固定2005290081；精确actuator/mating/线材尺寸HOLD，不以图代制造机械资格。动态性能、实物100fps/300us、供电/温度/故障/bench和历史ERC/图纸限制不由本包推成PASS。

## 唯一终审与交付

一次fresh-context只读终审及处置保存，无二审、不新生成图/坐标。独立公开电路仓库新目录、固定commit，全正文和可读CSV/JSON/PNG/原trace代码直接上传，manifest和ZIP辅助；无账户SQLite/实际凭据/第三方整PDF/无关项目。远端大小/Git对象SHA/旧冻结文件和匿名公开下载SHA由送达账记录，不虚报Pro逐附件已读，不要求额外ACK门。

## 接续

按Pro本次规定，数字接口链正常后停止新增离线placement轮次，向用户展示最终候选，等待真实视觉选择，不代用户选。若用户选定，再接完整统一原生PCB搬件/反推板框/重布线新范围批准，不用本150min坐标或图余量迁移CAD。
用户明确要求下一次正常报告同时申请更大的有界执行时间/次数/自主范围，故本次集中提出仅选定后的条件原生请求480min：必要机械及板框60、搬件60、重布线220、温冷native80、交付60；copy2/session4/save10/import2/audit6/DRC8/pour2/export1/image3，仅普通已知工程流程；身份/值/J2针序冻结，制造采购bench/Gerber0，不扩模型平台额度/系统账户或工具研究。只是申请未批不执行。若Pro本次仅接受资格包待用户选择，关闭等待监控并明确用户选定门，禁止循环重做已结案包。

END-OF-COMPLETE-R21-B311-DIGITAL-INTERFACE-CHAIN-QUALIFICATION-RECEIPT
'''
(P/'COMPLETE_B311_RECEIPT.md').write_text(text,encoding='utf8');(P/'README.md').write_text('# B311数字接口链资格包\n\n五条真实MCU-串联R-接口功能链核查正常；B31完整PASS1坐标冻结，未移动任何件。离线15400proxy0/106key/8cell保持。等待用户实际视觉选择，CAD未释放。\n\n完整中文报告 COMPLETE_B311_RECEIPT.md；DIGITAL_INTERFACE_CHAINS.csv及JSON为两段实际距离；FINAL_READONLY_AUDIT.json/NRST_PGOOD_BRANCH_AUDIT.json/保护支路/18输入SHA/唯一PNG/终审/预算一并提供。供应端口是sense-only，不供电。旧Macro排序不回写，不把链几何当硬件性能。\n',encoding='utf8')
print(json.dumps({'readOnlyPass':a['readOnlyQualificationPass'],'reportBytes':len(text.encode()),'reportSHA256':hashlib.sha256(text.encode()).hexdigest().upper()}))
