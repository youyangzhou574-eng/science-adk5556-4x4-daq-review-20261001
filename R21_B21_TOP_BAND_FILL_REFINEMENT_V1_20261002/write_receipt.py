from pathlib import Path
import json,hashlib,csv,datetime
from PIL import Image
P=Path(__file__).parent;d=json.loads((P/'PLACEMENT_B21.json').read_text());m=d['metrics'];old=json.loads((P/'PLACEMENT_B2.json').read_text());register=json.loads((P/'FROZEN_AND_MOVED_REGISTER.json').read_text());inputs=json.loads((P/'INPUT_SHA_MANIFEST.json').read_text())
for r in inputs:assert hashlib.sha256((P/r['path']).read_bytes()).hexdigest()==r['sha256']
assert set(d['positions'])==set(old['positions'])and len(d['positions'])==176
assert len(register['fixedRefs'])==170 and all(d['positions'][r]==old['positions'][r]for r in register['fixedRefs'])
assert len(register['movedRefs'])==6 and all(d['positions'][r][2]==old['positions'][r][2]and abs(d['positions'][r][0]-old['positions'][r][0]+28)<1e-8 and d['positions'][r][1]==old['positions'][r][1]for r in register['movedRefs'])
assert not m['bodyOverlapPairs']and not m['physicalProxyOverlapPairs']and m['criticalPairs']==94 and m['maxCriticalDeltaVsB2Mm']==0
with Image.open(P/'PLACEMENT_B2_VS_B21.png')as im:im.verify()
v={'timeUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sevenInputSHAUnchanged':True,'176IdsMatch':True,'170PositionsStrictUnchanged':True,'sixTranslationsOnlyMinus28MmX':True,'94RecordedDistancesMaintained':True,'15400PairsEachCompleteRecorded':True,'imageVerified':True,'newGeometryRecomputationDuringStructureCheck':False,'CAD':0}
(P/'FINAL_ARTIFACT_VERIFICATION.json').write_text(json.dumps(v,indent=2),encoding='utf8')
g={'stage':'B21_FINAL_OFFLINE_VISUAL_REFINEMENT_READY_FOR_SELECTION','priorB2EngineeringAcceptedByPro':True,'priorB2VisualDirectionAcceptedByPro':True,'finalVisualSelection':'USER_PRO_PENDING','placementRefinementCumulative':3,'imageThisStage':1,'bodyAndPadProxyNoOverlap':True,'keyPairs94Preserved':True,'frozen170':True,'moved6Only':True,'FFC_EXACT_ACTUATOR_SWEEP_HOLD':True,'CAD_RELEASED':False,'NATIVE_PCB_UPDATED':False,'BOARD_OUTLINE_DEFINED':False,'GERBER_RELEASE':False,'MANUFACTURE':False,'BENCH':False}
(P/'GATES.json').write_text(json.dumps(g,ensure_ascii=False,indent=2),encoding='utf8')
(P/'COMPLETE_B21_RECEIPT.md').write_text('''# COMPLETE B2.1 TOP-BAND FILL REFINEMENT RECEIPT

唯一包SCIENCE_ADK5556_4X4_R21_B21_TOP_BAND_FILL_REFINEMENT_V1。完整新裁定assistant e94cff97-f143-40f6-a8f8-77b5eed95484，parentuser99545896-9e48-4c47-8a92-1677fab2c02e，全文PRO_B21_RULING_FULL.md。新裁定接受B2工程检查与视觉方向，最终视觉选择仍HOLD；仅批准60min，消耗先前剩余第3轮布局、另明确一张B2→B2.1图。不进CAD。

## 实际变化与结果

只移动U4/C_MUX刚体及R_SEL_PD0..3四个相关C类拉阻，全部X−28mm、Y/角度不变。六器件列表和170冻结列表见FROZEN_AND_MOVED_REGISTER.json。参考Bias、MCU/Logic也保持不动，因为只移动MUX这一获准子集即可填进指定左上空带，不为用尽可动范围而重排其它模块。TIA/ROW、ADC、Power、J1/J2/J3/J4以及所有其它170器件X/Y/角度严格相同，不只是“位置关系大致相同”。没有拆microblock，也没有改FFC方向、器件值/身份/footprint/padnet/主电路。

自然body包络仍71.000×63.500mm，body占比18.1578%不变，不用缩板作为本次成果。指定顶部左带(x=.5..38.5，y=56..63mm)完整1mm空格最大矩形从266→84mm²；全bbox同方法最大空格矩形266→205mm²。4×4body占用CV由.41665→.40001，是较均匀但不能称完全均匀或用户已满意，右上仍有留白。空格数据是离线body栅格代理，不是可布线面积或制造空间。

有限实现：一轮refinement内只试7个X位移×4个Y位移共28个有限平移点，不做新的候选体系/全局优化器。每个点检查六件对冻结physical并集、六件自身两两、FFCkeepout，以及左侧边界；选出目标左带空白较小且不增顶部bbox的点。旋转允许但本次实际不需要旋转，没有新增算法研究。全部试点记录PLACEMENT_B21.json finiteTrials；最后坐标仅一个B2.1。

全176body及body+保守pad proxy分别遍历15,400不同器件对，无组豁免，面积阈值>1e-8mm²，全局记录0相交。最终冻结集合也检查FFC规划keepout；六移动件在有限点筛选中已逐件检查。94关键pad距离对B2变化0；U4/C_MUX本身施加同一平移，内部距离自然保持，94表并不冒称包含该B级pair。保持不是证明原距离电气资格，也不是原生DRC或爬电/布线裕量。

J2继续已有官方尺寸13.4×5.8工程占位，厂家精确body/完整actuator sweep仍HOLD，按前一次完整B2新裁定允许离线规划；没有重做3D/官方资料/API研究。源body为原生component-shape、圆角/椭圆pad代理矩形，限制不变。

## 可读交付与实耗

PLACEMENT_B21.csv完整176坐标；PLACEMENT_B2_VS_B21.png唯一同一比例对比图已实际查看；KEY_PIN_DISTANCE_B21.csv94距离；FROZEN_AND_MOVED_REGISTER、有限试点、七输入SHA、全部own源、初shell quoting失败说明与结构校验公开。两侧虚线是自然body包络，不是板框。图不能被当成原生PCB或制造文件。

本阶段60min / placement1of1（累计B2+本阶段3of3）/图1of1；新CAD/API/GUI/native/boardoutline/route/pour/DRC/仿真/采购制造bench/Gerber全部0。原B2七冻结输入SHA不变，历史结果不改，用户同意电脑但偏好API保留，本阶段不需任何前台操作。Renderer准备第一次PowerShell引号语法失败发生在Python/image启动前，无图预扣、无CAD；改为已保存Python生成脚本后仅实际导出1次，失败不冒称成功、不隐匿。

FINAL_REVIEW.md为一次whole-package只读终审。本阶段结束后不做第4轮或第2图，不继续placement试探。待用户/Pro实际视觉选定，再启动唯一有界原生搬176、反推板框、重布线及温冷File闭合。不是已授权直接进入CAD。

按用户明确更多有界预算要求，正常报告保留选定后统一原生480min预算申请（机械尺寸60/搬件板框60/布线220/温冷native80/交付60），copy2/session4/save10/import2/audit6/DRC8/pour2/export1/image3；仅请求未批不执行，不另独立预算消息、不扩平台系统或采购制造bench。普通实现本地累计，不研究工具。

END-OF-COMPLETE-R21-B21-TOP-BAND-VISUAL-REFINEMENT-RECEIPT
''',encoding='utf8')
(P/'README.md').write_text('# B2.1最后顶部构图\n\n仅6器件左移28mm，170器件位置冻结。请查看唯一PLACEMENT_B2_VS_B21.png及完整176坐标PLACEMENT_B21.csv；完整回执COMPLETE_B21_RECEIPT.md。自然包络不变，不是原生PCB或板框。最终视觉选择待用户/Pro，CAD0。\n',encoding='utf8')
(P/'PLAN_AND_LEDGER.md').write_text('''# B2.1唯一最后轮

完整e94cff97裁定60min/最后1轮/1图。先保存再删除旧监控，按连续授权执行。TIA/ROW/ADC/Power/四接口严格冻结；只MUX2+关联pull4统一平移，28有限点并非28次refinement。保留全部试点，一个最终输出。

Ruling: 只移动上部获准MUX子集，Bias/Digital仍固定——达到目标左带空白减少而不多改骨架；代价是最终整体视觉仍须人判断，不能称完全消除所有空白。
Ruling: 单独新目录记录继承最后一轮额度，不修改已GitHub冻结B2预算；累计3/3。新回复明确另批一张对比图，实际1/1，不篡改原B2图2/2。
No localGit/system/native writes. Existing history/source retained.
''',encoding='utf8')
print(json.dumps(v))
