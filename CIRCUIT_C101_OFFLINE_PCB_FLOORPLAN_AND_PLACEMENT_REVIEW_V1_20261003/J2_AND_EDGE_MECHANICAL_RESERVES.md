# 接口规划边界：不是合格厂家封装
J2唯一真实需求为薄FFC/FPC ZIF。默认2005290081 8P1mm bottomcontact/rightangle/frontflip沿左边，规划body14×7mm、焊尾8点1mm和两个空网机械占位；这些坐标是显式保守floorplan placeholder，不是native新封装、不用于出Gerber。旧171856 body不使用。左外侧10mm插线规划带及内侧操作保留区无人侵入；实际actuator sweep/线材厚度/端部朝向/实际mating/courtyard HOLD。

既有厂家资料只读复用路径 R21_J2_FFC_FPC_INTERFACE_CORRECTION_V1/sources_local_only/S2_connector_drawing.pdf 页3、DRAWING_TEXT_LOCAL_ONLY.json；本轮新增来源0。厂家整体宽A13.2±.2mm、壳体宽C11.6±.2mm、约5.3mm深度与1.9±.2mm闭合高度仅作为规划参考，frame datum精确资格未闭合，不称此占位全公差包络。

J1底边电源reserve；J3右上SWD、J4右下UART reserve。型号/侧插最终body未知，当前封装仅既有电气针位代理。外部走廊不放器件，不能把unknown机械模型当准确body。

图中接口虚线/阴影为示意，检查矩形以保存源码reserves为准，不要求三图或改坐标。
