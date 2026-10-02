# 装配输入与结构BOM
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
