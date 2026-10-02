# COMPLETE R21 PLACEMENT-ONLY TWO RECTANGULAR CANDIDATES RECEIPT

包：SCIENCE_ADK5556_4X4_R21_PLACEMENT_ONLY_TWO_RECTANGULAR_CANDIDATES_V1。
裁定：CIRCUIT-PRO-R21-PLACEMENT-ONLY-TWO-CANDIDATES-20261002-23；assistant bd3ea9a9-25a3-4c1f-a4bf-5b8c882aaf15，parentuser c9f5fd57-2a0e-4d75-a45a-a083fad55360。

## 交付结果

**终审结论：本包完整接收 HOLD / STOP。以下两套图只作为未接收视觉草案。FFC body/actuator datum 尚未闭合，触及 Pro23 显式停止条件；关键距离 coverage 和全局 pad proxy 检查也未闭合。不得因选定 A/B 就解除门，不能称 Pro23 全要求通过。唯一终审 Critical0 / Important3 / Minor2，全文 FINAL_REVIEW.md；本轮只作一次证据范围与门状态修订，不重算、不改图、不增加 CAD。**

两套完整176器件纯placement草案已生成，供用户与Pro选择；不是已实施PCB或制造放行。A偏功能/接口操作，B偏边界规整、上下展开和视觉平衡。二者均不使用旧LINE/VIA/POUR作布局约束或绘图内容，没有原生AutoLayout。100×90仅历史参照，未写回板框，也未先指定80×70等目标尺寸。

主图：PLACEMENT_AB_COMPARISON.png；单图PLACEMENT_A_NO_COPPER.png / PLACEMENT_B_NO_COPPER.png。完整坐标见PLACEMENT_A.csv / PLACEMENT_B.csv，不只是20块坐标。6个大功能区用电气功能分类颜色区分，不给小岛套框充当实际器件排列。

| 指标 | A | B |
|---|---:|---:|
| 器件body自然包络/mm | 87.000 × 79.800 | 81.000 × 77.900 |
| body union投影面积/自然包络面积 | 11.7916% | 12.9741% |
| 4×4 body占用率CV，越低越均匀 | 0.41594 | 0.38788 |
| 全bbox内1mm中心采样空白proxy/mm²，非周边连续空白 | 636 | 506 |
| body overlap（已有模型）/ pad proxy子集结果 | 0 / 部分组合0，完整性UNKNOWN | 0 / 部分组合0，完整性UNKNOWN |
| 同网IC-pad→passive-pad关键pairs | 74 | 74 |
| 最大关键距离变化/mm | 7.11e-15 | 7.11e-15 |

自然包络不包含引脚外伸/全部操作空间；physicalPadAndBodyBoundingBox另列于JSON。建议板包络只是在physical包络外加3mm工程预留政策，不是厂家机械最大公差确认或最终尺寸。A建议约93.00×85.87mm，B约87.00×84.20mm。FFC10mm插线/手部预留绘于板外，不当作需要填成PCB的材料。

## 输入与外形证据

使用20号实际已保存温态FINAL_WARM_PCB.json作为176器件/552pad/514assigned/107net/36普通NC+2J2 mechanical空网authority。21号未保存CONTACT不作为输入。其它175器件的body取17号安全epro2现有封装component-shape layer48，POLY或FILL闭合原图形；不读取账户SQLite、不重开CAD。对应封装所有padnumber按实际rotation投影匹配当前数据，552个中心最大残差0.001766mm，符合原生捕获0.1mil舍入，不冒称字节相同。175原生body图形不是独立厂家max-courtyard资格，但满足本次已有原生body图形的图示优先级。原body尺寸没有人为放大/缩小。

J2实际10pad信号/机械几何和网名分别验证，1–4ROW0..3，5–8COL0..3，MP1/MP2空网。原body艺术线不作为厂家body。已有Molex2005291002PSD000revB图纸中2005290081对应A13.2±0.2、参考depth5.3及推荐land fitting-nail布局，用13.4×5.8保守2D规划包络区分signal pads/mechanical tabs，沿native90°的local+y向左开放，图中Pin1红点和插入箭头可辨。已实际查看图纸页1/3和3/3（本地渲染PAGE3/PAGE5），原厂PDF只本地，公开指向官方URL。

**限制：这个矩形是基于官方尺寸和land datum的保守工程占位，不是已由厂家确认的精确housing/actuator轮廓注册。FFC_EXACT_MANUFACTURER_DATUM_HOLD保留；不能称FFC全机械资格PASS。** actuator打开height约3.95mm只来源于侧视reference，裸板2D检查不证明机壳高度。两方案自定义规划开盖/插线2D区域内无其它器件body；该区域未证明包含实际翻盖全开扫掠，不能解除本阶段FFC STOP。10mm插线空间/2mm手部侧向余量是设计政策，不伪装厂家规格。

J1/J3/J4为既有通用header；实际匹配壳体/插头型号未给，图纸只是已有native body。位于布局外缘，可从上方操作的构图意图不等于已验证三维插拔/装配空间。没有新购线材、造板、上电或bench。

## 局部约束与普通器件重排

本阶段A级TIA/ROW/reference/ADC及power IC输入输出caps、MCU贴身cap内部保持刚性；允许整体旋转，ADC整块转90°但全部相关pad相对关系保持。关键距离按同网真实IC pad与对应无源pad计算，而非中心距。已列出的74pair before/A/B全表见KEY_PIN_DISTANCE_COMPARISON.csv；该表不是完整关键邻接 coverage。U9_IN_CAP/U9_OUT_CAP/U10_IN_CAP/U10_OUT_CAP因位号筛选遗漏，RF0–3/CF0–3经串联件关联而不满足直接同网筛选，也未列出。它们按坐标生成仍在刚性块，但未补算指定pad距离；详见REVIEW_DISPOSITION.md与KEY_CONSTRAINT_COVERAGE_GAPS.csv。非GND相关pair被显式映射，不拿全板GND网替代功能关联。

普通电源控制/分压/拉阻、supervisor分压、debug保护、reset外设重编为实际器件行列；debug支路按J3/J4对应pin的y位置排列。6功能区面积比例是各区body投影面积/全部器件body投影面积，不是画一个矩形后的比例。大区面积无需相等，未声称区域bounding boxes无交叉。

4×4栅格用真实body union交面积；CV指标及1mm空白矩形是几何视觉proxy，不是电气DRC。A与B数据均列出，不以“B视觉优先”标签假定其每项指标优于A。没有用90%器件占用率或全板填满作为目标，关键器件也不拉远填空。

## 实耗、失败与停止范围

批准240min，formal候选2、official新来源0/4（只读已有资料）、几何refinement A2/3、B3/3、最终image3/3。所有CAD/copy/session/save/import/DRC/pour/nativeExport/boardoutline/routing/simulation/Gerber/procurement/manufacturing/bench/powerup均0，未重跑21cold或使用旧22剩CAD额度。

第一次body提取只处理POLY，U6实际FILL，初失败保留EXTRACTION_FIRST_FAILURE.md并一次补足读取；不是U6实体body缺失。坐标脚本有两次空格语法预执行失败，均在reserve之前，未生成几何方案/科学进程；不记成几何PASS。A/B第一遍真实几何各有body或保守pad相碰（大BLEED器件误按0603网格、bulk与LDO外伸），GEOMETRY_*_PASS_1.json保留；A第二遍body0，B第二遍body0，B第三遍仅重整下部控制件、body0。pad proxy报告零为不完整遍历子集：groups为块名→位号列表，却用groups.get(ref)判断同块，跨块可能None==None被跳过。原始结果保留，不回填全局PASS，不据此推断存在实际碰撞。不删除初失败或回填首次成功。

冻结4个输入文件SHA末次全不变；源脚本另从旧CANDIDATE_B_PLAN.json读取membership，未纳入该四项SHA清单；本包保存了派生CONSTRAINT_BLOCKS和候选membership，但原样再生成输入冻结不完整，见终审M2。旧实际工程未改，未激活任何GUI。用户现在允许操作电脑且偏好API已记录，但本阶段Pro23要求CAD0，不因此抢跑原生实施。

## 接收门与下一步

当前交的是Pro23停止门下的A/B未接收视觉草案与完整阻断回执。GATES表明PLACEMENT_ACCEPTED=false / CAD_RELEASED=false；视觉偏好可以先讨论，但不等于完整布局接收。请Pro集中裁定FFC机械资料限据及两项关键检查缺口的有界闭合或明确工程接收路线；不继续修工具研究、不重开旧21。只有新统一范围成立才能补证或原生实施，不能由几何空白代替真实插拔条件。

按用户明确“下一正常报告申请更多有界预算”的要求，本次完整报告集中建议选定后的原生阶段480min：接口body/尺寸接收60、一次搬件/板框60、关键模拟/供电及普通重布线220、warm/cold/native80、交付60；copy2/session4/save10/import2/captureaudit6/DRC8/pour2/nativeExport1/reviewImage3，普通合法placement/route细节自主累计。**只是建议，未批不执行；必须先裁定本次STOP和缺项、有人选A/B且下一统一工程范围成立；此次480min建议是上限申请，不是默认展开验证工具研究。** 不扩大平台额度/安装/系统账户/制造采购bench权限，不另发预算微问。

END-OF-COMPLETE-R21-PLACEMENT-ONLY-TWO-CANDIDATES-REVIEW-RECEIPT
