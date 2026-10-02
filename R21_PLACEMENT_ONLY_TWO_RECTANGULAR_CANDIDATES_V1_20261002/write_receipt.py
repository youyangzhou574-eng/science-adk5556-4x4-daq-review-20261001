from pathlib import Path
import json,csv,hashlib,datetime
P=Path(__file__).parent
a=json.loads((P/'PLACEMENT_A.json').read_text(encoding='utf8'))['metrics']
b=json.loads((P/'PLACEMENT_B.json').read_text(encoding='utf8'))['metrics']
budget=json.loads((P/'EXECUTION_BUDGET.json').read_text(encoding='utf-8-sig'))
sources=json.loads((P/'INPUT_SHA_MANIFEST.json').read_text(encoding='utf8'))
frozen=[{'path':r['path'],'sha256Before':r['sha256'],'sha256After':hashlib.sha256(Path(r['path']).read_bytes()).hexdigest()}for r in sources]
assert all(r['sha256Before']==r['sha256After']for r in frozen)
(P/'FROZEN_INPUT_RECHECK.json').write_text(json.dumps(frozen,indent=2),encoding='utf8')
with(P/'CANDIDATE_COMPARISON.csv').open('w',encoding='utf-8-sig',newline='')as f:
    rows=[{'metric':k,'A':a[k],'B':b[k]}for k in ('naturalWidthMm','naturalHeightMm','bodyAreaOverNaturalBBox','gridCoefficientOfVariation','largestEmptyRasterRectangleAreaMm2','maxCriticalDistanceDeltaMm')]
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
ka=list(csv.DictReader((P/'KEY_PIN_DISTANCES_A.csv').open(encoding='utf-8-sig')))
kb=list(csv.DictReader((P/'KEY_PIN_DISTANCES_B.csv').open(encoding='utf-8-sig')))
with(P/'KEY_PIN_DISTANCE_COMPARISON.csv').open('w',encoding='utf-8-sig',newline='')as f:
    out=[]
    for x,y in zip(ka,kb):
        assert tuple(x[k]for k in ('icRef','icPad','passiveRef','passivePad','net'))==tuple(y[k]for k in ('icRef','icPad','passiveRef','passivePad','net'))
        out.append({k:x[k]for k in ('group','icRef','icPad','passiveRef','passivePad','net','beforeMm')}|{'A_mm':x['afterMm'],'B_mm':y['afterMm']})
    w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
gates={'stage':'PLACEMENT_ONLY_READY_FOR_HUMAN_REVIEW_WITH_MECHANICAL_LIMITATIONS','formalCandidates':2,'componentsEach':176,
 'geometryOverlapAudit':{'A_body':len(a['bodyOverlapPairs']),'B_body':len(b['bodyOverlapPairs']),'A_padProxy':len(a['conservativePadEnvelopeOverlapPairs']),'B_padProxy':len(b['conservativePadEnvelopeOverlapPairs'])},
 'criticalPairsEach':74,'keyDistancesMaintained':True,'FFC2DConservativeKeepoutBodyCollisions':{'A':a['FFC2DKeepoutBodyCollisions'],'B':b['FFC2DKeepoutBodyCollisions']},
 'FFC_EXACT_MANUFACTURER_DATUM_HOLD':True,'CONNECTOR_MATING_HOUSING_AND_CHASSIS_HOLD':True,
 'userSelectionRequired':True,'CAD_RELEASED':False,'PCB_REVIEW_READY_AFTER_THIS_STAGE':False,'NATIVE_DRC_DONE':False,
 'BOARD_OUTLINE_FINAL':False,'GERBER_RELEASE':False,'MANUFACTURING_RELEASE':False,'BENCH_RELEASE':False,
 'imageExports':budget['actual']['finalImageExports'],'refinementA':budget['actual']['refinementA'],'refinementB':budget['actual']['refinementB']}
(P/'GATES.json').write_text(json.dumps(gates,ensure_ascii=False,indent=2),encoding='utf8')
receipt=f'''# COMPLETE R21 PLACEMENT-ONLY TWO RECTANGULAR CANDIDATES RECEIPT

包：SCIENCE_ADK5556_4X4_R21_PLACEMENT_ONLY_TWO_RECTANGULAR_CANDIDATES_V1。
裁定：CIRCUIT-PRO-R21-PLACEMENT-ONLY-TWO-CANDIDATES-20261002-23；assistant bd3ea9a9-25a3-4c1f-a4bf-5b8c882aaf15，parentuser c9f5fd57-2a0e-4d75-a45a-a083fad55360。

## 交付结果

两套完整176器件纯placement草案已生成，供用户与Pro选择；不是已实施PCB或制造放行。A偏功能/接口操作，B偏边界规整、上下展开和视觉平衡。二者均不使用旧LINE/VIA/POUR作布局约束或绘图内容，没有原生AutoLayout。100×90仅历史参照，未写回板框，也未先指定80×70等目标尺寸。

主图：PLACEMENT_AB_COMPARISON.png；单图PLACEMENT_A_NO_COPPER.png / PLACEMENT_B_NO_COPPER.png。完整坐标见PLACEMENT_A.csv / PLACEMENT_B.csv，不只是20块坐标。6个大功能区用电气功能分类颜色区分，不给小岛套框充当实际器件排列。

| 指标 | A | B |
|---|---:|---:|
| 器件body自然包络/mm | {a['naturalWidthMm']:.3f} × {a['naturalHeightMm']:.3f} | {b['naturalWidthMm']:.3f} × {b['naturalHeightMm']:.3f} |
| body union投影面积/自然包络面积 | {a['bodyAreaOverNaturalBBox']:.4%} | {b['bodyAreaOverNaturalBBox']:.4%} |
| 4×4 body占用率CV，越低越均匀 | {a['gridCoefficientOfVariation']:.5f} | {b['gridCoefficientOfVariation']:.5f} |
| 1mm采样最大空白矩形面积/mm² | {a['largestEmptyRasterRectangleAreaMm2']} | {b['largestEmptyRasterRectangleAreaMm2']} |
| body overlap / 保守pad包络overlap | 0 / 0 | 0 / 0 |
| 同网IC-pad→passive-pad关键pairs | 74 | 74 |
| 最大关键距离变化/mm | {a['maxCriticalDistanceDeltaMm']:.3g} | {b['maxCriticalDistanceDeltaMm']:.3g} |

自然包络不包含引脚外伸/全部操作空间；physicalPadAndBodyBoundingBox另列于JSON。建议板包络只是在physical包络外加3mm工程预留政策，不是厂家机械最大公差确认或最终尺寸。A建议约{a['recommendedBoardEnvelopeMm'][2]-a['recommendedBoardEnvelopeMm'][0]:.2f}×{a['recommendedBoardEnvelopeMm'][3]-a['recommendedBoardEnvelopeMm'][1]:.2f}mm，B约{b['recommendedBoardEnvelopeMm'][2]-b['recommendedBoardEnvelopeMm'][0]:.2f}×{b['recommendedBoardEnvelopeMm'][3]-b['recommendedBoardEnvelopeMm'][1]:.2f}mm。FFC10mm插线/手部预留绘于板外，不当作需要填成PCB的材料。

## 输入与外形证据

使用20号实际已保存温态FINAL_WARM_PCB.json作为176器件/552pad/514assigned/107net/36普通NC+2J2 mechanical空网authority。21号未保存CONTACT不作为输入。其它175器件的body取17号安全epro2现有封装component-shape layer48，POLY或FILL闭合原图形；不读取账户SQLite、不重开CAD。对应封装所有padnumber按实际rotation投影匹配当前数据，552个中心最大残差0.001766mm，符合原生捕获0.1mil舍入，不冒称字节相同。175原生body图形不是独立厂家max-courtyard资格，但满足本次已有原生body图形的图示优先级。原body尺寸没有人为放大/缩小。

J2实际10pad信号/机械几何和网名分别验证，1–4ROW0..3，5–8COL0..3，MP1/MP2空网。原body艺术线不作为厂家body。已有Molex2005291002PSD000revB图纸中2005290081对应A13.2±0.2、参考depth5.3及推荐land fitting-nail布局，用13.4×5.8保守2D规划包络区分signal pads/mechanical tabs，沿native90°的local+y向左开放，图中Pin1红点和插入箭头可辨。已实际查看图纸页1/3和3/3（本地渲染PAGE3/PAGE5），原厂PDF只本地，公开指向官方URL。

**限制：这个矩形是基于官方尺寸和land datum的保守工程占位，不是已由厂家确认的精确housing/actuator轮廓注册。FFC_EXACT_MANUFACTURER_DATUM_HOLD保留；不能称FFC全机械资格PASS。** actuator打开height约3.95mm只来源于侧视reference，裸板2D检查不证明机壳高度。两方案保守开盖/插线2D访问包络内无其它器件body；10mm插线空间/2mm手部侧向余量是设计政策，不伪装厂家规格。

J1/J3/J4为既有通用header；实际匹配壳体/插头型号未给，图纸只是已有native body。位于布局外缘，可从上方操作的构图意图不等于已验证三维插拔/装配空间。没有新购线材、造板、上电或bench。

## 局部约束与普通器件重排

本阶段A级TIA/ROW/reference/ADC及power IC输入输出caps、MCU贴身cap内部保持刚性；允许整体旋转，ADC整块转90°但全部相关pad相对关系保持。关键距离按同网真实IC pad与对应无源pad计算，而非中心距。74pair before/A/B全表见KEY_PIN_DISTANCE_COMPARISON.csv；非GND相关pair被显式映射，不拿全板GND网替代功能关联。

普通电源控制/分压/拉阻、supervisor分压、debug保护、reset外设重编为实际器件行列；debug支路按J3/J4对应pin的y位置排列。6功能区面积比例是各区body投影面积/全部器件body投影面积，不是画一个矩形后的比例。大区面积无需相等，未声称区域bounding boxes无交叉。

4×4栅格用真实body union交面积；CV指标及1mm空白矩形是几何视觉proxy，不是电气DRC。A与B数据均列出，不以“B视觉优先”标签假定其每项指标优于A。没有用90%器件占用率或全板填满作为目标，关键器件也不拉远填空。

## 实耗、失败与停止范围

批准240min，formal候选2、official新来源0/4（只读已有资料）、几何refinement A2/3、B3/3、最终image3/3。所有CAD/copy/session/save/import/DRC/pour/nativeExport/boardoutline/routing/simulation/Gerber/procurement/manufacturing/bench/powerup均0，未重跑21cold或使用旧22剩CAD额度。

第一次body提取只处理POLY，U6实际FILL，初失败保留EXTRACTION_FIRST_FAILURE.md并一次补足读取；不是U6实体body缺失。坐标脚本有两次空格语法预执行失败，均在reserve之前，未生成几何方案/科学进程；不记成几何PASS。A/B第一遍真实几何各有body或保守pad相碰（大BLEED器件误按0603网格、bulk与LDO外伸），GEOMETRY_*_PASS_1.json保留；A第二遍0，B第二遍0，B第三遍仅重整下部控制件，0。不删除初失败或回填首次成功。

冻结4个输入文件SHA末次全不变；旧实际工程未改，未激活任何GUI。用户现在允许操作电脑且偏好API已记录，但本阶段Pro23要求CAD0，不因此抢跑原生实施。

## 接收门与下一步

当前交的是带机械限制的placement人工选择包，GATES表明CAD_RELEASED=false / userSelectionRequired=true。请用户与Pro看A/B，选定后再给一次有界原生搬件+新板框+重布线+warm/cold/实际epro2的统一阶段。FFC精确body注册、通用header匹配壳体、真实插拔/装配条件在原生机械准备中仍须明确，不能由本次几何空白代替。

按用户明确“下一正常报告申请更多有界预算”的要求，本次完整报告集中建议选定后的原生阶段480min：接口body/尺寸接收60、一次搬件/板框60、关键模拟/供电及普通重布线220、warm/cold/native80、交付60；copy2/session4/save10/import2/captureaudit6/DRC8/pour2/nativeExport1/reviewImage3，普通合法placement/route细节自主累计。**只是建议，未批不执行；必须先有人选A/B且下一统一工程范围成立。** 不扩大平台额度/安装/系统账户/制造采购bench权限，不另发预算微问。

END-OF-COMPLETE-R21-PLACEMENT-ONLY-TWO-CANDIDATES-REVIEW-RECEIPT
'''
(P/'COMPLETE_PLACEMENT_RECEIPT.md').write_text(receipt,encoding='utf8')
(P/'README.md').write_text('# 两套纯器件布局候选\n\n先看PLACEMENT_AB_COMPARISON.png。完整结论与机械限制见COMPLETE_PLACEMENT_RECEIPT.md。A/B各176坐标CSV；body来源与74组关键pin距离可读。实际PCB未改；选定前不启动原生搬件或布线。\n',encoding='utf8')
(P/'OFFICIAL_SOURCE_LINKS.md').write_text('# 已有官方来源，原文二进制只本地\n\n- Molex2005290081: https://www.molex.com/en-us/products/part-detail/2005290081\n- Manufacturer drawing: https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/200/200529/2005290061_sd.pdf\n\nManufacturer body exact registration remains HOLD; conservative2D bounds are planning evidence only. No new official source fetched in this stage.\n',encoding='utf8')
print(json.dumps({'bodyOverlapPairs':[len(a['bodyOverlapPairs']),len(b['bodyOverlapPairs'])],'pairs':len(out),'inputSHAUnchanged':len(frozen),'CAD':0}))
