# 实际针序与方向

见J2_ACTUAL_8PIN_HARNESS.csv及J2_PINOUT_AND_BODY.png。图按PCB顶面、EDA正y向上绘制：方形1脚在本图下端（x约5mm/y约30.11mm），三角丝印在1脚右侧。上端为8/COL3，不能按照片“从上到下”自动当作1..8。

板座body20.17×6.35mm，pinspan17.78mm。projectcourtyard选21.88×7.37mm（包括20.88mm线壳长向+两端0.5mm，以及板端外侧0.5mm余量）；这是本项目设计选择，非厂家推荐courtyard。manufacturerassembly外形离板左边最小约1.90mm，projectcourtyard约1.40mm，未移J2或改板框。孔径1.14±0.05mm来自厂家推荐；1.70mm铜盘为本板选择，名义环0.28mm，最大孔1.19mm时环0.255mm。

摩擦锁侧面沿PCB左侧（local+y经90°旋转后-x）。应沿板法向竖直插拔；机壳/扎带/弯曲半径未知，完整mated3D与真实操作空间仍PENDING。图中示意不作为完全机械认证。厂家特别注明header circuit1可能不与housing circuit1相同；装配线束须以实际接触连续性匹配，不只看壳体数字。


## 17号丝印要求的未闭合项

实际原生丝印可见J2与1脚三角，但**没有ROW0–ROW3/COL0–COL3或1/ROW0文字**；GUI padnet显示不属于制板丝印。17号要求未完全满足。准确针序图/CSV为mandatory companion，不能声称该文字已印在板上。J2电气/尺寸/温冷DRC通过，独立J2制造接口conformance保持HOLD，请Pro接受配套图作为当前审查合同或统一批准一次最小原生丝印补字。当前硬save/audit/export已满，不自行追加CAD，也不调查工具。
