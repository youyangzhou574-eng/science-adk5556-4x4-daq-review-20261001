# 独立核实的案例与适用边界

S1 [ADS8684/8688 SBAS582C](https://www.ti.com/lit/ds/symlink/ads8684.pdf)，57–58页/图101：模拟输入和参考避开数字通路，专用连续地平面；REFCAP/REFGND就近连接；RC贴输入。此案例同ADC系列，直接用于U5引脚侧划分。冻结电容值不改成案例值。实际当前已有AVDD9/30、REFCAP、REFIO、DVDD多电容，须逐组围绕对应pin，不能均摊到大矩形。

S2 [TIPD167 TIDU427B](https://www.ti.com/lit/pdf/tidu427)，31–32页/图19–20：ADS8688评估板模拟和数字电路分开、输入及参考短连接。其六层板不同于本板四层，不迁移叠层；借鉴输入通道和参考相邻关系，不声称复制其性能。

S3 [TIDA-01214 TIDUD64A](https://www.ti.com/lit/pdf/tidud64)，采用ADS8688A的隔离模拟输入模块。27–28页给测试总结和设计文件入口，文档没有提供能直接证明全部元件坐标的高清placement图。这里只核实系统架构相近；不把隔离电源/变压器布局套到本板，不声称已审其完整PCB数据。

S4 [OPAx388 SBOS777D](https://www.ti.com/lit/ds/symlink/opa4388.pdf)，26页/图10-2：输入反馈就近、回路短、供电去耦靠供电脚、避免热梯度。本图是单运放layout，四运放的2+2通道必须从本板实际U1/U2各pin推导。22p局部反馈和远端4.99k/2.2nF支路不同，不将后者错误标为直接连接运放反馈pin。

S5 [TMUX1134 SCPS213B](https://www.ti.com/lit/ds/symlink/tmux1134.pdf)，引脚图与9.3–9.4：通道端、选择脚和供电脚实际交错。不能照字面将所有S放一侧D放另一侧；按真实CH0/1与CH2/3两侧，Bias源→开关→行驱动逐通道展开，控制端转向Logic。

S6 [ADI CN0175](https://www.analog.com/en/resources/reference-designs/circuits-from-the-lab/cn0175.html)，图2–4：AD7607/ADR421输入通道和去耦对称、参考邻近ADC。同类多通道设计原则可借鉴；不同ADC和参考，不能照抄封装、针号、数值、84dB性能。

以上六条独立打开官方来源，五个TI文档均本地下载SHA登记，ADI网页同样登记。网页回复的引用占位符没有被当作来源。第三方完整文件留在sources_local_only，不公开上传；公开本原创短说明/来源链接/SHA，避免整篇复制。

# 本板实际引脚与方案校正

- U5数字端1/2及36–38沿封装一端，模拟16/18/21/23沿另一端；旋转180°时analog向左、digital向右。参考5–7位于上侧近digital端，不能画成独立第三边。pin9与30各侧AVDD，34为DVDD。
- U7实际SPI11–14在右侧，旋转180°后朝U5；UART19/21与SWD24/25在下/右方向，J3/J4也相应靠可接近的右缘。
- U4的S/D沿两长边交错，双方信号链可以清晰但不存在严格的单侧S、单侧D。
- 整体布局审查仅几何和理想飞线距离，原生DRC/可布线/电气实测/完整FFC机械仍需后续阶段。
