from placement_geometry import *
import csv,hashlib,datetime
from PIL import Image
d=json.loads((P/'PLACEMENT_B2.json').read_text(encoding='utf8'));m=d['metrics'];b=json.loads((P/'EXECUTION_BUDGET.json').read_text());rows=list(csv.DictReader((P/'KEY_PIN_DISTANCE_B2.csv').open(encoding='utf-8-sig')))
assert len(d['positions'])==176 and set(d['positions'])==set(G)
assert m['allDistinctPairsExamined']==15400 and not m['bodyOverlapPairs']and not m['physicalProxyOverlapPairs']and not m['FFCPlanningKeepoutCollisions']
# Verify functional series association from frozen actual pad nets, not inferred names alone.
links=[]
for row in rows:
    if row['association'].startswith('FUNCTIONAL_'):
        ref=row['association'].split('VIA_')[1];nets={p['net']for p in G[ref]['pads']};assert {row['icNet'],row['passiveNet']}==nets
        links.append({'passiveRef':row['passiveRef'],'seriesRef':ref,'icNet':row['icNet'],'passiveNet':row['passiveNet'],'actualSeriesPadNets':sorted(nets)})
    else:assert row['icNet']==row['passiveNet']
assert len(rows)==94 and len(links)==16 and max(abs(float(r['deltaMm']))for r in rows)<1e-8
(P/'FUNCTIONAL_SERIES_PAIR_NET_AUDIT.json').write_text(json.dumps(links,indent=2),encoding='utf8')
inputs=json.loads((P/'INPUT_SHA_MANIFEST.json').read_text());checks=[]
for r in inputs:
    actual=hashlib.sha256((P/r['path']).read_bytes()).hexdigest();assert actual==r['sha256'];checks.append(dict(path=r['path'],shaUnchanged=True))
images=[]
for n in ('PLACEMENT_B2_NO_COPPER.png','PLACEMENT_OLD_B_VS_B2.png'):
    with Image.open(P/n)as im:im.verify()
    with Image.open(P/n)as im:images.append({'path':n,'width':im.width,'height':im.height,'sha256':hashlib.sha256((P/n).read_bytes()).hexdigest()})
verification={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'componentIds176Match':True,'padSourceCount':552,'criticalPairs94':True,'functionalSeriesLinks16ActualNets':True,'completePairEnumeration15400Recorded':True,'bodyAndPadProxyNoIntersectionRecorded':True,'inputs':checks,'images':images,'nativeCAD':0,'note':'Structural frozen delivery checks, no extra placement refinement; not native DRC or mechanical/signal integrity qualification.'}
(P/'FINAL_ARTIFACT_VERIFICATION.json').write_text(json.dumps(verification,indent=2),encoding='utf8')
g={'stage':'B2_OFFLINE_PLACEMENT_READY_FOR_USER_VISUAL_SELECTION_WITH_LIMITS','components':176,'pads':552,'assigned':514,'electricalNets':107,'normalNC':36,'J2MechanicalEmptyPads':2,'bodyOverlapModel0':True,'padProxyAllDistinctPairs0':True,'criticalPairs94Maintained':True,'functionalSeriesPairNetAudit16':True,'rigidMicroblockPreserved':True,'FFCPlanningKeepoutNoCollision':True,'FFC_EXACT_ACTUATOR_SWEEP_HOLD':True,'FFCStageDisposition':'New complete ruling explicitly permits offline placement while exact actuator sweep remains HOLD. This is not manufacturer qualification.','PCB_UPDATED':False,'CAD_RELEASED':False,'USER_SELECTION_REQUIRED':True,'BOARD_OUTLINE_DEFINED':False,'MANUFACTURE':False,'BENCH':False,'normalPerformanceValidated':False}
(P/'GATES.json').write_text(json.dumps(g,ensure_ascii=False,indent=2),encoding='utf8')
report=f'''# COMPLETE B2 INTERLOCKING PLACEMENT RECEIPT

包 SCIENCE_ADK5556_4X4_R21_PLACEMENT_B2_INTERLOCKING_V1。执行完整回复 assistant636d471a-c983-4b4c-a177-8cd22b5aad0c，parentuser8d72fefb-b873-4999-8fad-5682acc74577；全文PRO_B2_RULING_FULL.md。

## 结果

唯一B2完整176器件/552pad无铜方案已生成。图PLACEMENT_B2_NO_COPPER.png附1mm空白占用图，PLACEMENT_OLD_B_VS_B2.png为同真实比例/同坐标尺度旧B对比；两图实际查看。CSV含176实际位号、X/Y/角度/层/功能/约束/外形来源，没有用20框冒充176器件。功能靠颜色分组，没有六大区矩形边界；关键小块可平移旋转，普通器件填凹槽，整体包络自然产生。实际PCB、板框、铜、原理图没有改。

| 指标 | 旧B冻结值 | B2 |
|---|---:|---:|
| 自然body包络/mm | 81.000×77.900 | {m['naturalWidthMm']:.3f}×{m['naturalHeightMm']:.3f} |
| body面积/自然bbox | 12.9741% | {m['bodyFraction']*100:.4f}% |
| 宽高比 | 1.0398 | {m['aspectRatio']:.4f} |
| 4×4body占用CV（越低越均匀） | .38788 | {m['gridCV']:.5f} |
| 空白栅格proxy/mm² | 506（旧中心采样、边缘可能越界） | {m['largestEmptyFullCellRectangleAreaMm2']}（完整无body相交1mm单元） |

空白proxy算法不同，不能把506→266声称同一方法下精确改善百分比；图能直接看布局变化。B2的CV略差于旧B，也不能称所有均匀性指标都更优。占用只有body面积，不含焊盘/布线/装配操作，仍有真实留白，尤其左上带状空区。图是供用户判断是否够规整，不冒称已经排满/用户满意或已选B2。尺寸是body自然包络，不是制造板尺寸或面积最小目标。

## 输入、硬约束与有限实现

ACTUAL_GEOMETRY / CONSTRAINT_BLOCKS / BODY_SOURCE_REGISTER来自23已冻结安全提取；完整membership在本包，不读取额外未冻结旧membership。七输入逐字SHA未变。厂家整PDF、账户SQLite不复制公开；本包只有own几何和官方链接。175native component-shape不等于独立厂家最大courtyard；J2仍用13.4×5.8mm已有官方尺寸保守工程占位而不是13.2nominal当最大尺寸。精确body注册/翻盖3D扫掠HOLD，最新完整回复明确此项不阻止离线排布；不把该路线变化回写旧23STOP。

保留176身份、552pad源/514assigned/107net/36NC+2J2 MP空网；ROW1–4/COL5–8、原器件值/封装/信号未变。现有LINE/VIA/POUR完全忽略，没有新原生工程。

A级TIA/ROW/reference/ADC/powercaps/MCU及14个关键/重复小块按整体刚体变换；全部块内器件中心pair误差≤7.11e-15mm，另列实际pad关键表94项。原74直接同网pair，加4个U9/U10 cap.1↔IC5/6、RF/CF每通道两端共16功能pair。RF/CF的关联经R_TIA_ISO/R_COL_SENSE串联，不冒称直接同网；FUNCTIONAL_SERIES_PAIR_NET_AUDIT.json逐项用真实series两端net验证，94pair最大绝对距离变化{m['maxCriticalDeltaMm']:.3g}mm。这个保持检查不扩为布线稳定性、耦合/精度或实物资格。

所有176不同器件组合15,400对分别检查native-body与body+保守pad proxy，没有groups字典豁免。已有body overlap0、proxy overlap0；矩形圆角pad代理比真实圆角保守，不是原生DRC或已保证工艺间距。普通件贪心位置有0.20mm物理包络规划间隙政策；骨架只要求不相交，未声称全板0.20mm间隙。J2自定义插线/开盖2D区域内其它physical0，完整actuator扫掠仍HOLD。

有限算法：先14micro-block及四接口骨架；普通件53个按面积排序；1mm占用网格只筛有限凹槽/host附近候选，每件≤152个候选中心、4角度，实际逐件次数GREEDY_CANDIDATE_TRACE.csv。cost用bbox新增面积、宽高比、host邻接、局部空洞距离proxy和同功能对齐。不是全局优化器/遗传算法/MILP/AutoLayout，不做插件/API研究。没有额外local-swap重放；max3是上限不是必须用尽。本次layout两轮：第一轮真实MUX与ADC去耦包络相碰，PASS_1_SKELETON_FAILURE保留；第二轮只把MUX刚体移到上沿并转90°，之后有限填缝完整通过。不是删除失败或首轮PASS。

## 额度、门与下一步

180min；layout refinement实际2/3；final images2/2；CAD/API/GUI/native/boardoutline/routing/pour/DRC/simulation/Gerber/采购制造bench全部0。用户允许电脑但偏好API保留，本阶段禁止CAD所以无窗口操作。实际报告结构检查不属于第三轮布局或新增图。历史21/23未改，初失败和所有源保留。

本包只供用户视觉选定，CAD_RELEASED=false。用户选定后才启动新的统一原生搬176器件、反推板框、重布线、CONTACT与温冷File收尾；未执行这些步骤，不循环重开旧21。FFC完整机械和各接口匹配/机壳/制造CAM仍待接续工程，普通几何草案不是制造或上电放行。

按用户明确“下次正常报告申请更多有界执行时间/次数/自主范围”的要求，本次正常报告集中保留建议选定后统一原生阶段480min（机械/尺寸60、一次搬件/板框60、重布线220、温冷/native80、交付60）；copy2/session4/save10/import2/audit6/DRC8/pour2/export1/image3。仅请求，未批不执行，不另发预算消息、不扩大平台/系统/采购制造bench。若仅待用户选定，保存此包不空转，也不自选B2。

唯一最终审查见FINAL_REVIEW.md及REVIEW_DISPOSITION.md（如有）；接收限制以GATES为准。

END-OF-COMPLETE-R21-B2-INTERLOCKING-PLACEMENT-RECEIPT
'''
(P/'COMPLETE_B2_RECEIPT.md').write_text(report,encoding='utf8')
(P/'README.md').write_text('# B2咬合式离线布局\n\n先看PLACEMENT_B2_NO_COPPER.png及PLACEMENT_OLD_B_VS_B2.png。完整176坐标PLACEMENT_B2.csv、94关键真实pad距离、占用图、完整来源与首轮真实失败保留。\n\nCAD0，未定板框。精确FFC翻盖扫掠HOLD但本次新裁定允许离线排布；用户选择后才能原生实施。完整COMPLETE_B2_RECEIPT.md/GATES/FINAL_REVIEW。\n',encoding='utf8')
print(json.dumps({'structuralVerification':True,'inputsUnchanged':len(checks),'pairs':len(rows),'functionalLinks':len(links),'images':len(images),'refinement':b['actual']['placementRefinement']}))
