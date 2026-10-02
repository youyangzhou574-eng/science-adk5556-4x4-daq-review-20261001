# J2 可插拔8线接口规格（审查版）

板端 **Molex1718560008**，单排8位、2.54mm、竖直PTH、摩擦锁；线端 **22012087 /22-01-2087 /2695-8R** 压接壳体。线端接头插到板端，不把8根线直接焊到PCB。每个待测电阻Rij只接ROWi与COLj，16个电阻形成4行4列；J2没有GND或供电针。

从PCB真实方形1脚起：1ROW0、2ROW1、3ROW2、4ROW3、5COL0、6COL1、7COL2、8COL3。必须逐芯连通确认实际对接关系，不能假定线壳模制数字与板座1脚相同。它是摩擦锁接口，不承诺完全防反插。

准确压接端子MPN尚未锁定：实际AWG、绝缘外径、镀层和压接工具未知。厂家公共图给出22–30AWG/max insulation1.57mm及2759/6459/41572/4809/8088系列，不能把系列范围当作每个端子MPN资格。没有承诺兼容用户原有未知型号线缆；当前采用已批准的新成套标准。

## 原生工程实际身份与装配覆盖

J2原理图/PCBName与ManufacturerPart为1718560008，Manufacturer为MOLEX，旧通用供应编号C124381已清空。仅J2使用项目封装87b2e6ab0bf2243f，名MOLEX_1718560008_MFR_SD171856_R17，真实File里尺寸通过；保留通用8针电气symbol与generic device UUID，不冒称厂家库器件已入库。装配选料须使用准确MPN与本项目封装，不按generic device/catalog名采购。

原生自定义MatingHousing/CrimpTerminal等属性键创建但实际值为空，API返回true不是字段已写证明。配套壳体/端子/针序以本文和实际8针CSV为合同。旧generic排针3D关联仍存在，**不能用于新Molex机械验证**；没有制造/全3D或用户现有线缆兼容放行。项目正文不让这些元数据缺项卡住电气主线。

来源与尺寸见CONNECTOR_SOURCE_QUALIFICATION.md。当前Molex页Limited Information Available；不把旧裁定的Active说法作为实证。资料镜像旧版图明确列出8位，不称当前最新版或供货保证。


## 17号丝印要求的未闭合项

实际原生丝印可见J2与1脚三角，但**没有ROW0–ROW3/COL0–COL3或1/ROW0文字**；GUI padnet显示不属于制板丝印。17号要求未完全满足。准确针序图/CSV为mandatory companion，不能声称该文字已印在板上。J2电气/尺寸/温冷DRC通过，独立J2制造接口conformance保持HOLD，请Pro接受配套图作为当前审查合同或统一批准一次最小原生丝印补字。当前硬save/audit/export已满，不自行追加CAD，也不调查工具。
