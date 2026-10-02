from pathlib import Path
import json,csv,datetime,hashlib,shutil,re,collections
P=Path(__file__).parent; BASE=P.parent; OLD=BASE/'R21_EXTERNAL_ARRAY_PLUGGABLE_INTERFACE_AND_FAB_INPUT_CONTRACT_V1'; PRE=BASE/'R21_PCB_MANUFACTURING_PREFLIGHT_READONLY_V1'
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
URL='https://jlcpcb.com/capabilities/pcb-capabilities'
REPO='https://github.com/youyangzhou574-eng/science-adk5556-4x4-daq-review-20261001'
OLDURL=REPO+'/tree/bcafa5c6b834c20539774cd335d34586442453be/R21_EXTERNAL_ARRAY_PLUGGABLE_INTERFACE_AND_FAB_INPUT_CONTRACT_V1_20261002'
def write(name,text): (P/name).write_text(text,encoding='utf8')
def js(name,obj):write(name,json.dumps(obj,ensure_ascii=False,indent=2))
def csvout(name,rows,fields=None):
 with (P/name).open('w',encoding='utf8',newline='')as f:
  w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)
bom=json.loads((P/'BOM_STRUCTURAL_176_FROM_COLD.json').read_text('utf8'))
assert len(bom)==176 and len({r['Designator']for r in bom})==176
bom.sort(key=lambda r:re.sub(r'(\d+)',lambda m:m.group().zfill(4),r['Designator']))
csvout('BOM_STRUCTURAL_176.csv',bom)
groups=collections.defaultdict(list)
for r in bom:groups[(r['Manufacturer'],r['MPN'],r['Value'],r['Footprint'])].append(r)
grouped=[dict(Manufacturer=k[0],MPN=k[1],Value=k[2],Footprint=k[3],Quantity=len(v),Designators=';'.join(x['Designator']for x in v),qualification='STRUCTURAL_FIELDS_ONLY_NOT_PROCUREMENT_RELEASE' if k[1]else'MPN_MANUFACTURER_REQUIRED')for k,v in groups.items()]
assert sum(r['Quantity']for r in grouped)==176
csvout('BOM_GROUPED.csv',grouped)
missing=[r for r in bom if r['missingManufacturer']or r['missingMPN']]
assert {r['Designator']for r in missing}=={'J1','J3','J4'}
csvout('BOM_MISSING_MANUFACTURER_MPN.csv',missing)
byMPN=collections.defaultdict(set)
for r in bom:
 if r['MPN']:byMPN[(r['Manufacturer'],r['MPN'])].add((r['Value'],r['Footprint']))
conflicts=[{'Manufacturer':k[0],'MPN':k[1],'variants':sorted(v)}for k,v in byMPN.items()if len(v)>1]
js('BOM_STRUCTURAL_CHECK.json',{'UTC':NOW,'rows':176,'uniqueDesignators':176,'groupRows':len(grouped),'groupQuantity':176,'populatedMPNRows':173,'missingRefs':['J1','J3','J4'],'sameMPNValueFootprintConflicts':conflicts,'scope':'Native fields extracted from frozen cold17 evidence. Not new independent manufacturer qualification, availability, substitute, procurement or physical inventory.'})
assert not conflicts
for name in ['J2_PINOUT_AND_BODY.png','J2_ACTUAL_8PIN_HARNESS.csv','J2_CONNECTOR_AND_HARNESS_SPEC.md']:
 shutil.copyfile(OLD/name,P/name)
# Bounded prior-source excerpts and existing geometry are traceable snapshots, not fresh CAD.
shutil.copyfile(PRE/'MANUFACTURING_PREFLIGHT_MATRIX.csv',P/'HISTORICAL_PREFLIGHT_MATRIX_R16.csv')
shutil.copyfile(PRE/'NATIVE_SAME_PACKAGE_MASK_GAPS.csv',P/'HISTORICAL_MASK_GAPS_R16.csv')
sources=[
 {'id':'F18-S1','type':'fresh official capability reference','url':URL,'retrievedDateUTC':'2026-10-02','recordedUTC':NOW,'uniqueSourceCount':1,'facts':'1oz multilayer spacing .09mm; inner .5oz default; standard PTH +.13/-.08mm vs conditional tight .05mm; green mask bridge .10mm; process reference not factory selection or CAM approval'},
 {'id':'F18-S2','type':'frozen accepted native input','path':'../R21_EXTERNAL_ARRAY_PLUGGABLE_INTERFACE_AND_FAB_INPUT_CONTRACT_V1/COLD_PCB.json','SHA256':hashlib.sha256((OLD/'COLD_PCB.json').read_bytes()).hexdigest().upper(),'publicFixedFolder':OLDURL,'scope':'176 parts identity and existing pad/net authority'},
 {'id':'F18-S3','type':'frozen engineering geometry/preflight','path':'../R21_PCB_MANUFACTURING_PREFLIGHT_READONLY_V1/GEOMETRY_SUMMARY.json','SHA256':hashlib.sha256((PRE/'GEOMETRY_SUMMARY.json').read_bytes()).hexdigest().upper(),'scope':'prior native dimensions/screen; not CAM or new exact fullgeometry run'},
 {'id':'F18-S4','type':'current Pro18 ruling','path':'PRO_FAB_INPUT_CLOSURE_RULING_FULL.md','SHA256':hashlib.sha256((P/'PRO_FAB_INPUT_CLOSURE_RULING_FULL.md').read_bytes()).hexdigest().upper(),'scope':'accepted J2 variance and180min doc-only contract'},
 {'id':'F18-S5','type':'manufacturer J2 drawings already qualified in17','publicFixedFolder':OLDURL,'headerDrawingSHA':'134202F9425A2E1617E303052B4FCAAC697C526CF51FB54B6F3C5F2F16E1F048','housingDrawingSHA':'79B00AD4CE684EA09261FBC48F9B66E90A0842EC5C0D24825122670587555243','scope':'same vendor-authored drawings; old revision/provenance limitations unchanged, no new source/candidate'}
]
js('SOURCES.json',sources)
write('OFFICIAL_CAPABILITY_REFERENCE.md',f'''# 当前工艺页核对（不是板厂选定或CAM批准）
F18-S1：[{URL}]({URL})，2026-10-02读取。同一URL重复读取按一个独立来源记账，未增加连接器候选。
短摘要：FR-4四层、1.6mm厚度±10%；多层1oz，内层默认0.5oz，可指定1oz；支持ENIG及HASL。1oz多层线距能力约0.09mm；常规通孔公差+0.13/-0.08mm，特定条件紧孔±0.05mm需指定孔及确认。绿色1oz阻焊桥参考下限0.10mm。普通通孔via能力覆盖本板约0.305/0.610mm，但本板环宽约0.152mm贴近其多层1oz绝对下限0.15mm。
这是一般能力页的简短核对，不是本板CAM接受；实际报价订单层叠、孔径及阻焊必须由选定厂商确认。公开报告未拷贝第三方全文。没有联络板厂/下单/生成生产文件。
''')
params=[
 ('F01','fabricator','FABRICATOR_PENDING','PREORDER_REQUIRED','尚未选厂；JLC仅能力参照，不代表订单'),
 ('F02','material','FR-4, ordinary rigid four-layer','RECOMMENDED_INPUT','指定厂商标准FR4；实际牌号/Tg及认证由厂商确认，不凭空填UL号'),
 ('F03','layers','4: Top/L2 GND/L3 supply/Bottom','ACCEPTED_DESIGN','保持冻结铜层与网络；介质各厚度未定，需最终stackup'),
 ('F04','outline','100 x 90 mm nominal rectangle; routed','ACCEPTED_DESIGN_RECOMMENDED_PROCESS','不加孔/倒角/机箱约束；无新机械改板'),
 ('F05','finishedThickness','1.60 mm nominal; reference +/-10% (1.44-1.76)','RECOMMENDED_INPUT','实际层叠由厂商确认；连接器尾长/装配过程同时确认'),
 ('F06','copper','outer1oz / inner1oz preferred','RECOMMENDED_INPUT','inner1oz非参照厂默认.5oz；必须明确选项，不悄然接受.5或2oz'),
 ('F07','finish','ENIG preferred; HASL only after assembler/CAM acceptance','RECOMMENDED_INPUT','细间距装配优先平整表面；不是已下单工艺'),
 ('F08','mask','green LPI; retain native openings','RECOMMENDED_INPUT_CAM_REQUIRED','不全局改开窗；U5/U9/U10桥.090-.097mm待CAM'),
 ('F09','legend','existing native silk + mandatory companion','ACCEPTED_VARIANCE','J2仅J2/方形1脚/三角，ROW/COL完整文字未印在板上'),
 ('F10','traceWidth','minimum6mil (0.1524mm), existing6/12/16/20','ACCEPTED_GEOMETRY','不把所有间距也宣称6mil'),
 ('F11','spacingCapability','support frozen4mil track-track rule (.1016mm); pad-track6mil; pour10mil','FAB_CAM_CONFIRM_REQUIRED','6mil-only spacing服务不能默认适配；不改冻结规则'),
 ('F12','via','ordinary through-via drill0.3048 / copperdiam0.6096 mm','RECOMMENDED_INPUT_CAM_REQUIRED','nominal annular ring0.1524mm; needs drill registration/CAM acceptance'),
 ('F13','J2 finishedPTH','1.14 +/-0.05 mm, eight round PTH; pad~1.70','FAB_CAM_CONFIRM_REQUIRED','manufacturer specified1.09..1.19; ordinary+0.13/-0.08 would1.06..1.27 and is not equivalent'),
 ('F14','other holes','native J1/J3/J4 and297 vias; no blind/buried/new slots','FAB_CAM_CONFIRM_REQUIRED','最终Excellon/CAM未生成，现值为冻结CAD名义值'),
 ('F15','hole spacing','historical overall minimum0.31115mm, pair class not requalified here','FAB_CAM_CONFIRM_REQUIRED','via-via vs pad-hole要求不同；须板厂按实际钻孔分类核查，旧screen不是CAM PASS'),
 ('F16','via mask treatment','ordinary mask-covered/tented preference, assembler/fab confirm','RECOMMENDED_INPUT_CAM_REQUIRED','不默认为树脂填孔或塞孔合格；不得更改已有mask记录'),
 ('F17','panel/tooling','single-board routed preferred; assembler-defined rails/fiducials if required','ASSEMBLER_INPUT_REQUIRED','不新加板内定位孔/mark；拼板资料未生成'),
 ('F18','stencil','assembler-approved finepitch stencil/apertures/reflow','ASSEMBLER_INPUT_REQUIRED','不凭空锁厚度/开口比；U9/U10/U11/U12底面焊接不可当普通手焊已可靠'),
 ('F19','impedance','no controlled-impedance requirement added','NOT_APPLICABLE','不引入新SI/PI或HDI课题'),
 ('F20','quantity/test','prototype quantity and factory e-test/inspection to be agreed','PREORDER_REQUIRED','板数/交期/预算未选择；无采购授权')
]
rows=[dict(id=a,parameter=b,proposedValue=c,status=d,note=e)for a,b,c,d,e in params]
csvout('DEFAULT_FAB_PARAMETERS.csv',rows)
write('FABRICATION_INPUT_CONTRACT.md',f'''# 四层实验室验证板制造输入合同（推荐版，尚未下单）
18号接受的电气PCB/J2基线固定于 [17包commit]({OLDURL})；原生SHA801149F292E86CF34AB2872F177125099D640421B48B62F3F9044EF2151DB241。没有新CAD、DRC、导出或Gerber。本轮给出确定的推荐参数，厂商及真实CAM接受保留待填。

推荐FR-4四层、100×90mm、1.6mm nominal、外/内各1oz、绿色阻焊、ENIG、普通贯通via、铣外形。参照厂内层默认0.5oz，故内1oz需明确选择；不默认加厚2oz。层顺序保持Top/L2 GND/L3供电/Bottom；实际core/prepreg厚度、料号与总厚公差由厂商最终stackup确认。无受控阻抗要求。
默认详表见DEFAULT_FAB_PARAMETERS.csv；参数状态明确区分已有设计、推荐输入和待CAM，不把建议当用户选厂/下单。

必须单列的CAM项：
- 原生最小线宽6mil，但冻结TrackTrack规则约4mil。不能只选择6/6mil能力并声称全部适配；须覆盖既有4mil间距规则并由实际生产资料复核。pad-track约6mil、pour10mil，不统一替换。
- 297贯通via名义孔0.3048/盘0.6096，环0.1524mm贴近参照厂多层1oz绝对下限。名义几何不是加工孔位容差保证。
- J2厂家finished PTH为1.14±0.05mm（1.09–1.19）。普通参照通孔+0.13/-0.08mm落到1.06–1.27，不满足同一合同。须订单逐列J2八孔特殊公差并取得书面CAM/工艺确认；不得把焊接连接器误称为press-fit。参照厂“press-fit孔”±.05服务条款不自动适用于J2焊接孔。厂商拒绝时集中报告具体工艺差异，不擅自改孔/改铜/换件。
- U5/U9/U10既有阻焊桥约0.096774/0.090081/0.090081mm低于参照绿色0.10mm。标FAB_CAM_CONFIRM_REQUIRED：厂商决定是否能够保留或需批准并窗，装配厂确认桥风险/钢网。没有授权现在修改footprint或native openings。
- 历史最小孔边间距0.31115mm仅旧只读screen，当前未重做孔对类别资格。不同via-via/pad-hole规则不能混用；完整钻孔分类由CAM核查，不能称严格CAM PASS。
- 极小原生丝印和完整mated空间/装配工具空间按实际工艺确认；不因此自动返工已接受PCB。

板厂待填FABRICATOR_PENDING；板数、服务档、实际材料/层叠、J2孔公差、阻焊桥、via环/孔间距分类、钢网/拼板/e-test接受号等待真实输入。未生成制造文件、未联系厂商、未下单。[官方能力参照]({URL})只支持一般可用工艺，不是本板放行。
''')
critical=[]
for r in bom:
 if r['Designator'].startswith('U') and not '_' in r['Designator']:
  critical.append(dict(Designator=r['Designator'],MPN=r['MPN'],Footprint=r['Footprint'],pinCount=r['pinCount'],nativeRotation=r['rotation'],instruction='Match manufacturer top-view pin1 to actual project pad1; do not use package-name suffix or rotation alone',status='ASSEMBLY_CHECK_REQUIRED'))
for r in bom:
 if r['Designator'].startswith('D_'):
  critical.append(dict(Designator=r['Designator'],MPN=r['MPN'],Footprint=r['Footprint'],pinCount=r['pinCount'],nativeRotation=r['rotation'],instruction='BAT54S is dual-series 3-pin; verify manufacturer1/2/3 and actual net, not a2-pin cathode-band shortcut',status='ASSEMBLY_CHECK_REQUIRED'))
csvout('ASSEMBLY_POLARITY_AND_PIN1.csv',critical)
write('ASSEMBLY_RELEASE_INPUTS.md',f'''# 装配输入与结构BOM
BOM_STRUCTURAL_176.csv逐个Designator，BOM_GROUPED.csv按Manufacturer+MPN+Value+actualFootprint分组（总176），BOM_MISSING_MANUFACTURER_MPN.csv列出真正空字段。冻结cold17实际字段173器件有MPN，J1/J3/J4三件缺manufacturer/MPN；不是173件已通过全规格或实物采购认证。BOM_STRUCTURAL_CHECK.json确认唯一ref、组数量相加176和同MPN值/封装无冲突。supplierPart是供应目录索引，不是厂家料号资格；Description乱码不参与authority。
J1为2位2.54PTH、J3为6位、J4为4位通用排针，现有真实封装与网络保留；装配前需实物manufacturer/MPN、针截面/高度/公母配对确认，不擅自选三替代型号。它们不是本轮已知电气PCB返工项。

J2必须覆盖generic关联名：Board header=Molex1718560008；实际footprint=MOLEX_1718560008_MFR_SD171856_R17；housing=22012087（线束外配件不计板上176数量）。J2 genericDevice和旧3D不用于买料或mated认证。完整ROW/COL只能从强制companion读取，板上仅J2+方形pad1+三角。装配作业单须附本包J2_PINOUT_AND_BODY.png、J2_ACTUAL_8PIN_HARNESS.csv、J2_CONNECTOR_AND_HARNESS_SPEC.md。

优先采用SMT回流装全部SMD，再按真实工艺焊PTH连接器。U5细间距TSSOP38、U9/U10小QFN-HR、U11/U12 WSON需装配厂钢网/温度曲线/底部连接检验方案；不把手焊全板当默认可靠。焊接/检查方式是建议合同，无实际装配或AOI/X-ray结果。是否需要X-ray由封装和可视性确定，不凭空规定此板都已检验。

ASSEMBLY_POLARITY_AND_PIN1.csv保留15颗U器件及17颗BAT54S的实际rotation和pin数，但rotation值/封装名后缀不能代厂家top-view核对。既有电气针网审查继承18；装配时需匹配physicalpin1与nativepad1：
- U5既有布局rotation180，pin1右下；U1/U2/U3/U4方向来自原生参考，不能统一按页面左上焊。
- U9/U10真实10pad、U11/U12真实6pad，不凭封装外观补第11/7个“散热焊盘”。
- BAT54S是三脚双串联二极管，逐1/2/3核对，不能靠单二极管色环；REF3025的三脚外形也不是同一针功能。
- MLCC本身无正负极性；本包未取得工作偏压有效容量，容量HOLD仍实物/性能输入，不从名义22uF推为参考供电已通过。
- J1电源输入pin1/2与所有J3/J4 sense/信号线必须按accepted实际针网验收。外部sense不能代供电；J2八线无GND/V5/V3V3。
- SMT位置/CPL和实际底/顶面、供料形式、针1标记可见性、钢网/拼板与合格检验须装配方确认；本包不生成CPL/Gerber。

当前建议工艺可用作询价输入，但manufacturer缺3件、factory/CAM、端子、CPL/生产文件、真实装配授权与实际首件检验均未闭合。采购/制造/上电依然FALSE，不把PCB设计接受当物理性能PASS。
''')
write('J2_HARNESS_BUILD_SPEC.md',f'''# J2八芯插拔线束合同（接收版，端子待真实线材）
板端1718560008、壳体22012087/22-01-2087已接受；8位单排2.54mm friction-lock。线束拔插不需要在PCB上焊八根导线。壳体ramp不等于绝对防反插；没有资格宣称reverse insertion impossible。
针序必须对板端actualpad编号：1ROW0，2ROW1，3ROW2，4ROW3，5COL0，6COL1，7COL2，8COL3。矩阵Rij跨ROWi/COLj（4行4列16点，8线）；不是16根独立两端线，也没有额外GND/电源进入J2。
EXACT_TERMINAL=PENDING_AWG。24–26AWG只是18号建议准备范围，尚非用户实际线径；已有壳体资料支持22–30AWG、绝缘外径上限1.57mm不代表每个端子全部适用。采购前取得导体AWG/绞线结构、实际绝缘外径、镀层和压接设备/方式，再与准确端子官方适用范围核对。此轮terminalcandidate0，没锁任何terminalMPN。housing配8个经资格端子数量，必要备件由未来采购量决定，不能混入176PCB器件BOM。

断电线束装配检验流程（方案，不是已执行试验）：
1. 按实际板上J2方形pad1和三角确认boardpin1；用companion固定图视角，板端pin1沿板边位置与旧generic排针图不同，不用旧图推断。
2. 拿真实header/housing按friction-lock方向实际配合；断电用万用表从boardpad1追到线端对应接触腔，标ROW0，再逐pin2..8追线。不能把housing塑料模制“1”当电气1，不能直接镜像图纸猜腔号。
3. 导线两端永久标ROW0..ROW3/COL0..COL3（颜色只能辅助），确认array端同名连续。记录实际腔号与8线net一一映射及检验人员/器材。
4. 真实mated追线与裸线束验收分开：先将裸线束与PCB、阵列两端断开，核对八条正确端到端通路且每条仅对应同名一根线，再检查任意两根不同导线的28组（8选2）隔离、无非预期导通；具体判据按实际仪器及线束合同，不能凭空给通用ohm/耐压阈值。单独裸线束与连接电阻阵列后的导通预期不同，不能要求整个已接电阻阵列所有ROW/COL无限阻抗。参考FROZEN_J2_SOURCE数据和实际阵列接法解释预期。
5. 按选定端子厂家的压接高/拉力/绝缘夹持标准确认；不凭空填某个牛顿阈值或通用0ohm阈值。与阵列连接前先单独检线束，再按已定义16点电阻/断电测量验收。
6. 线束长度、应力释放/固定、mated高度与机箱空间还未定义；旧generic3D不可认证mated干涉。不上电、不做实物实验或插拔次数试验。

强制附件:J2_PINOUT_AND_BODY.png、J2_ACTUAL_8PIN_HARNESS.csv、J2_CONNECTOR_AND_HARNESS_SPEC.md，均从 [accepted17]({OLDURL})逐字节复制。CSV的圆整API显示坐标不作为钻孔制造坐标；板上没有完整ROW/COL文字这一事实由18接受偏差，不再开CAD。
''')
checks=[
 ('A01','Accepted schematic/PCB electrical and warm/cold','ACCEPTED_REVIEW_PASS','R18 acceptedR17;176/550/514/107/36','No new physicalperformance claim'),
 ('A02','J2actualfootprint/order/bodyedge','ACCEPTED_REVIEW_PASS','1718560008/22012087, manufacturerderivedFP','Not fullmated3D'),
 ('A03','J2missingROWCOLsilk','ACCEPTED_NONBLOCKING_VARIANCE','R18 releaseconformancehold','Mandatorycompanion required; textnotprinted'),
 ('A04','J2genericDevice/old3D','NONBLOCKING_DOCUMENT_LIMIT','exactMPN+actualFPoverride','Do notprocure bygenericname orcertify3D'),
 ('P01','Selectedfabricator/quantity/price/turnaround','PREORDER_REQUIRED','FABRICATOR_PENDING','User/orderauthorization separate'),
 ('P02','Stackupmaterial/copper/thickness/finish','PREORDER_REQUIRED','defaultFR4/4L/1.6/1ozall/ENIG/green','Confirmrealstackup andinner1ozselection'),
 ('P03','Manufacturingfiles/exportpermission','PREORDER_REQUIRED','Gerber/drill/CPLnotgenerated','No autoexport/order'),
 ('C01','U5/U9/U10maskbridges','FAB_CAM_CONFIRM_REQUIRED','approximately.096774/.090081/.090081mm','Factorygreen.10reference notblanketPASS; keepnative'),
 ('C02','J2finishedhole tolerance','FAB_CAM_CONFIRM_REQUIRED','1.14+/-.05mm vsordinary+ .13/- .08','Writtenprocess acceptanceJ2eightPTH; solderheadernotpress-fit'),
 ('C03','Viaannularring/drillregistration','FAB_CAM_CONFIRM_REQUIRED','.3048/.6096/ring.1524','Near1ozreferenceabsmin.15;CAMcheck'),
 ('C04','Trackspace andother pad/innerclearances','FAB_CAM_CONFIRM_REQUIRED','6milwidthbut4milTrackTrackrule','Factorycoverfrozenrules;no4mil-to6milruleedit'),
 ('C05','Drillpair classification','FAB_CAM_CONFIRM_REQUIRED','historicaloverallmin.31115mm','Separatevia-via/pad-hole categoriesinCAM;noCADrecheck'),
 ('C06','Panel/tooling/mask/legendactualdata','FAB_CAM_CONFIRM_REQUIRED','No production CAM run','No automaticboardmodifications'),
 ('S01','J1/J3/J4manufacturer/MPN','ASSEMBLY_PREORDER_REQUIRED','3nativefieldsblank; footprints/netsfrozen','Selectmatchedactualpartbeforeorder'),
 ('S02','J2terminal/wire','ASSEMBLY_PREORDER_REQUIRED','EXACT_TERMINAL=PENDING_AWG','ActualAWG/OD/plating/crimpmethod needed'),
 ('S03','Pin1/polarity/CPL/inspection','ASSEMBLY_INPUT_REQUIRED','32criticalU/dualdiode rows','Actualmanufacturerorientationandassemblyprocedure'),
 ('S04','SMT/stencil/reflow/landacceptance','ASSEMBLY_INPUT_REQUIRED','smallQFN/WSON andTSSOPfinepitch','Noallhandsolder reliabilityassumption'),
 ('S05','Harnessmechanics/continuity','ASSEMBLY_INPUT_REQUIRED','8wiretrace plan','Noactualtest result'),
 ('B01','Firstpower andmetrology','BENCH_NOT_RELEASED','performance/MLCC/WCET/SWD/faultpending','Noactualpowerup'),
 ('N01','Metadata/UTF8/909911theory','NOT_REQUIRED_FOR_PCB_REWORK','historicalacceptedlimits','No newtoolresearch'),
 ('N02','MIMO/descriptorcertificate','NOT_REQUIRED_FOR_ENGINEERING_CLOSURE','engineeringgoalaccepted','Do notreopenendedscience'),
]
cl=[dict(id=a,item=b,category=c,evidence=d,action=e)for a,b,c,d,e in checks];csvout('MANUFACTURING_RELEASE_CHECKLIST.csv',cl)
write('MANUFACTURING_RELEASE_CHECKLIST.md','''# 放行清单
MANUFACTURING_RELEASE_CHECKLIST.csv是当前分项authority；HISTORICAL_PREFLIGHT_MATRIX_R16.csv保留原阶段输入，不覆盖18接受状态。
- 已有PASS：原理图/电气PCB/温冷/实际J2针序与2D封装。PCB_REVIEW_READY=true。
- 下单前必填：厂商、数量、实际层叠铜重/厚度/finish、生产文件和用户制造采购权限。已有默认合同可询价；不是所有参数都空着。
- CAM必须确认：细桥、J2八个tightfinishedhole、via环/孔位、既有4milspace规则、钻孔对分类、实际生产数据/拼板。
- 装配输入：J1/J3/J4准确manufacturer/MPN；真实线径OD/端子/压接；CPL/极性/钢网/回流与检查方式；线束真实连续记录。
- 不要求重开PCB的事项：J2缺ROW/COL文字已接受但companion强制；genericdevice/旧3D仅正确MPN与几何authority覆盖；历史UTF8/909911不作为工具研究。
- 物理能力保持待验：参考有效容量/100fps/WCET/300us/温区/故障/真实精度、SWD及首上电。PCB审查就绪不等于制造或bench放行。

若厂商实际拒绝某CAM条件才带具体差异集中报告，获新范围裁定前不自动改板。当前没有真实factory答复、没有Gerber、没有询价下单、没有physicalsample。
''')
g={'UTC':NOW,'ruling':'CIRCUIT-PRO-R21-J2-ECO-ACCEPT-WITH-SILK-VARIANCE-20261002-18','PCB_REVIEW_READY':True,'SCHEMATIC_ACCEPTED':True,'J2_SILK_TEXT_VARIANCE_ACCEPTED':True,'J2_NATIVE_SILK_ROWCOL_MISSING':True,'J2_ECO_CONFORMANCE_HOLD':'RELEASED_BY_R18','FAB_DEFAULT_INPUT_PREPARED':True,'FABRICATOR':'PENDING','STRUCTURAL_BOM_ROWS':176,'MPN_PRESENT_ROWS':173,'MPN_MANUFACTURER_REQUIRED':['J1','J3','J4'],'EXACT_TERMINAL':'PENDING_AWG','MANUFACTURING_RELEASE':False,'PROCUREMENT_RELEASE':False,'BENCH_RELEASE':False,'GERBER_RELEASE':False,'CAD_ALLOWED_THIS_PACKAGE':False,'nonblockingLimits':['J2_GENERIC_DEVICE_METADATA_HOLD','J2_3D_NOT_QUALIFIED','J2_SILK_TEXT_VARIANCE_WITH_MANDATORY_COMPANION'],'actualManufacturingRequired':['FACTORY_STACKUP_CONTRACT','MASK_BRIDGE_CAM_ACCEPTANCE','J2_FINISHED_HOLE_TOLERANCE_ACCEPTANCE','VIA_RING_AND_DRILL_CLASS_CAM','J1_J3_J4_PART_IDENTITIES','WIRE_TERMINAL_AND_CRIMP','PRODUCTION_FILES_AND_USER_AUTHORIZATION'],'scope':'Engineering documentprepared; real manufacturinginputs still pending. Old17 falsegates preserved historically, not rewritten.'}
js('GATES.json',g)
write('COMPLETE_FAB_INPUT_CLOSURE_RECEIPT.md',f'''# SCIENCE_ADK5556_4X4_R21_FAB_AND_ASSEMBLY_RELEASE_INPUT_CLOSURE_V1 完整回执
## 接收结论
18号正式接受J2电气/2Dfootprint/8针order/温冷DRC，并接受缺完整ROW/COL丝印为强制companion兜底的文档/装配偏差。PCB_REVIEW_READY=true；PCB设计主线结束。本包完成180min授权下的只读制造/装配输入准备，不声称实物制造输入全部闭合或允许下单。制造/采购/bench/Gerber release仍FALSE。

## 冻结输入和执行
冻结 [17包固定版本]({OLDURL})，原生SHA801149F292E86CF34AB2872F177125099D640421B48B62F3F9044EF2151DB241，继承176parts/550pads/514assigned/107nets/36NC和warm/cold真实DRC0；本包没有新CAD/cold/DRC/导出，严格禁止项全部0。旧文件哈希本包只读核对，旧17图面偏差/false门/失败不回写成18事后PASS。
普通推荐合同已具体化：FR4四层/100×90/1.6nominal/内外1oz/绿阻焊/ENIG/ordinarythroughvia；factory未选。只有一个新的官方能力页来源，连接器候选0，端子型号未锁；未新增MIMO/descriptor/API/3D研究。

## 实际资料成果
1. FABRICATION_INPUT_CONTRACT.md、DEFAULT_FAB_PARAMETERS.csv：20参数状态。内1oz需显式选；6mil线宽不能代6mil所有间距，冻结TrackTrack约4mil。
2. BOM_STRUCTURAL_176.csv、BOM_GROUPED.csv、BOM_MISSING_MANUFACTURER_MPN.csv：176唯一Designator，groupqty176，173MPN填入，J1/J3/J4缺manufacturer/MPN；字段覆盖不是173件全规格/采购认证。
3. ASSEMBLY_RELEASE_INPUTS.md与ASSEMBLY_POLARITY_AND_PIN1.csv：真实U/dualdiodeorientation记录，SMT建议、finepitch/底部连接工艺、genericJ2准确MPN覆盖，不采购generic关联名。
4. J2_HARNESS_BUILD_SPEC.md：Molex1718560008板座+22012087壳体，PCB1–8=ROW0–3/COL0–3；terminal=PENDING_AWG，24–26AWG仅建议，不假定用户线径；实际mated追线/连续检验方案未执行。
5. MANUFACTURING_RELEASE_CHECKLIST.md/CSV：PASS/下单必填/CAM/装配/nonblocking分开。没有“修丝印再开CAD”的新包。
强制三附件与17字节同：J2_PINOUT_AND_BODY.png、J2_ACTUAL_8PIN_HARNESS.csv、J2_CONNECTOR_AND_HARNESS_SPEC.md。没有复制native/PDF，固定旧版本链接可读/下载；CSV显示坐标不当CAM精度。

## 必须诚实保留的工艺差异
J2drawingfinishedhole1.14±.05，普通参照factory+ .13/- .08非等价；须J2八孔特殊公差CAM确认。不能称J2焊接header为pressfit或自动套pressfit服务。U5/U9/U10 .090–.097阻焊桥仍FAB_CAM_CONFIRM_REQUIRED；via环.1524临近多层1ozabsmin.15、旧最小孔距.31115未在本轮分类，须CAM。不存在当前实际厂家接受回执。详源F18-S1..5与OFFICIAL_CAPABILITY_REFERENCE.md，参照官方工艺URL：{URL}。
当前权威状态见GATES.json；完成文档不等于CAM/采购/制造就绪。实物有效容量、精度/100fps/300us/WCET/SWD/故障温区仍待实体工程验证，不回到工具理论门。

## 门和接续
该180min文档包完成后关闭，不循环重做。普通文件整理已授权，但未取得实物factory/Wire/MPN输入时保留具体缺项，下一步在实际资料到达后一次汇总。任何生产文件导出、采购制造或上电须用户另行明确范围授权，Pro文字不能替代。下一正常报告按用户明确更多有界工作预算要求集中提出条件只读输入接收范围，不另追加消息。

## 交付核对
预算、冻结SHA、176BOM、强制附件、状态一致性在DOCUMENT_CROSSCHECK.json与EXECUTION_BUDGET.json；一次wholepackagefreshcontext终审见FINAL_REVIEW.md。公开本项目独立GitHub新目录+manifest/ZIP+固定commit，只发送一条简短摘要，送达与回复状态分开记，配套owner/nextCheck及接续monitor。实际配对网页逐附件读取未验证，不虚报。
END-OF-COMPLETE-R21-FAB-AND-ASSEMBLY-RELEASE-INPUT-CLOSURE-RECEIPT
''')
write('README.md','''# R18 制造/装配输入合同
PCB设计与J2正式接受；此包只读文档，不允许生产/采购/上电。
- [完整回执](COMPLETE_FAB_INPUT_CLOSURE_RECEIPT.md)
- [制造合同](FABRICATION_INPUT_CONTRACT.md) / [参数CSV](DEFAULT_FAB_PARAMETERS.csv)
- [装配合同](ASSEMBLY_RELEASE_INPUTS.md) / [176BOM](BOM_STRUCTURAL_176.csv) / [合并BOM](BOM_GROUPED.csv) / [缺MPN](BOM_MISSING_MANUFACTURER_MPN.csv)
- [线束合同](J2_HARNESS_BUILD_SPEC.md) / [实际8针](J2_ACTUAL_8PIN_HARNESS.csv) / [针序图](J2_PINOUT_AND_BODY.png)
- [放行分类](MANUFACTURING_RELEASE_CHECKLIST.md) / [机器可读状态](GATES.json)
- [来源](SOURCES.json) / [预算](EXECUTION_BUDGET.json) / [终审](FINAL_REVIEW.md)

需要真实factory/CAM输入、J1/J3/J4partidentity和线材/端子输入。推荐合同不是下单和性能认证；历史文件保留原状态。
''')
print(json.dumps({'filesWritten':len(list(P.iterdir())),'BOM':176,'groups':len(grouped),'missing':['J1','J3','J4'],'criticalRows':len(critical),'defaultParameters':len(rows),'releaseChecks':len(cl)},ensure_ascii=False))
