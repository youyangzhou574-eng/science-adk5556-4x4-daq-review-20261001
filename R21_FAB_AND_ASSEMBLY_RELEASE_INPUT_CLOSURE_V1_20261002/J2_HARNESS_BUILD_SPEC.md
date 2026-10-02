# J2八芯插拔线束合同（接收版，端子待真实线材）
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

强制附件:J2_PINOUT_AND_BODY.png、J2_ACTUAL_8PIN_HARNESS.csv、J2_CONNECTOR_AND_HARNESS_SPEC.md，均从 [accepted17](https://github.com/youyangzhou574-eng/science-adk5556-4x4-daq-review-20261001/tree/bcafa5c6b834c20539774cd335d34586442453be/R21_EXTERNAL_ARRAY_PLUGGABLE_INTERFACE_AND_FAB_INPUT_CONTRACT_V1_20261002)逐字节复制。CSV的圆整API显示坐标不作为钻孔制造坐标；板上没有完整ROW/COL文字这一事实由18接受偏差，不再开CAD。
