# 首版基线与修订
项目 SCIENCE_ADK5556_4X4_DAQ_REPLICA。依据 CIRCUIT-PRO-FIRST-BUILD-INTEGRATED-DESIGN-GATES-20261001-01。
用户事实：固定4行+4列8根电极线，单元约1–7kΩ、变化约10%；尚非逐点实测范围。设计范围0.8–8kΩ，100整帧/s，20–30°C，外线≤30cm/每线0–1nF是首版试验边界。
5V必须在ADS8684 AVDD处满足4.75–5.25V，数字3.3V。VCM=2.5V，选行=2.25V，E=0.25V。4列持续TIA，Rf=4.99kΩ，Cf=2.2nF。原论文与旧master只读参考，本包独立创建，无旧工程复制。
核心器件均采用现成嘉立创原生库且保持真实物理针号/封装：OPA4388IDR×2，OPA2388IDR，TMUX1134PWR，ADS8684IDBTR，REF3025AIDBZR，STM32G031K8T6，TPS7A2033PDBVR。
局部修订一轮：行输出10Ω改1kΩ，反馈仍从板端ROW取样；每列运放负输入前加10kΩ感测电阻，Rf/Cf仍接板端COL；90kΩ分压下臂用9只精密10kΩ串联。激励、Rf、架构和核心系列未变。新增两项电阻改变动态，必须保留验证HOLD。
ADS8684 AIN2=21/AIN2GND=20，AIN3=23/AIN3GND=22：以封装图及官方EVM图为准，保留原说明表文字矛盾。OPA2388库pin1 OUA仅库标签笔误，物理功能OUTA。TMUX1134没有EN，低SEL选B(VCM)，高SEL选A(VEXC)。REFSEL低使用ADC内部4.096V，不将REF3025输出接ADC参考。
参考去耦REFIO22µF/REFCAP1µF分开；22µF的4.096V偏压有效容量尚未厂家曲线证明≥10µF。不得把额定22µF等同有效值。
当前设计标签：DYNAMIC_VALIDATION_HOLD、FAULT_PROTECTION_HOLD、REFERENCE_CAPACITANCE_HOLD、BENCH_NOT_RELEASED。HOLD不掩盖已知错误引脚；完成真实连通性后仍不释放上电/PCB/制造。
