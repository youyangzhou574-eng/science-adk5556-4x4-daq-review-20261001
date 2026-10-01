import pathlib,json,csv,collections
p=pathlib.Path(__file__).resolve().parent
plan=json.loads((p/'PLANNED_NATIVE_DESIGN.json').read_text(encoding='utf-8'))
lib=json.loads((p/'ALL_LIBRARY_PARSED.json').read_text(encoding='utf-8'))
def doc(n,t):(p/n).write_text(t.strip()+'\n',encoding='utf-8')
doc('BASELINE_AND_CHANGELOG.md','''# 首版基线与修订
项目 SCIENCE_ADK5556_4X4_DAQ_REPLICA。依据 CIRCUIT-PRO-FIRST-BUILD-INTEGRATED-DESIGN-GATES-20261001-01。
用户事实：固定4行+4列8根电极线，单元约1–7kΩ、变化约10%；尚非逐点实测范围。设计范围0.8–8kΩ，100整帧/s，20–30°C，外线≤30cm/每线0–1nF是首版试验边界。
5V必须在ADS8684 AVDD处满足4.75–5.25V，数字3.3V。VCM=2.5V，选行=2.25V，E=0.25V。4列持续TIA，Rf=4.99kΩ，Cf=2.2nF。原论文与旧master只读参考，本包独立创建，无旧工程复制。
核心器件均采用现成嘉立创原生库且保持真实物理针号/封装：OPA4388IDR×2，OPA2388IDR，TMUX1134PWR，ADS8684IDBTR，REF3025AIDBZR，STM32G031K8T6，TPS7A2033PDBVR。
局部修订一轮：行输出10Ω改1kΩ，反馈仍从板端ROW取样；每列运放负输入前加10kΩ感测电阻，Rf/Cf仍接板端COL；90kΩ分压下臂用9只精密10kΩ串联。激励、Rf、架构和核心系列未变。新增两项电阻改变动态，必须保留验证HOLD。
ADS8684 AIN2=21/AIN2GND=20，AIN3=23/AIN3GND=22：以封装图及官方EVM图为准，保留原说明表文字矛盾。OPA2388库pin1 OUA仅库标签笔误，物理功能OUTA。TMUX1134没有EN，低SEL选B(VCM)，高SEL选A(VEXC)。REFSEL低使用ADC内部4.096V，不将REF3025输出接ADC参考。
参考去耦REFIO22µF/REFCAP1µF分开；22µF的4.096V偏压有效容量尚未厂家曲线证明≥10µF。不得把额定22µF等同有效值。
当前设计标签：DYNAMIC_VALIDATION_HOLD、FAULT_PROTECTION_HOLD、REFERENCE_CAPACITANCE_HOLD、BENCH_NOT_RELEASED。HOLD不掩盖已知错误引脚；完成真实连通性后仍不释放上电/PCB/制造。
''')
doc('DETAILED_CIRCUIT_AND_PROTECTION.md','''# 详细电路及保护
## 正常工作
J1输入稳压5V/GND；U8产生3.3V，EN接5V，NC悬空。U6产生REF_2V5，U3A单位增益产生VCM。VCM经10k/90k分压，U3B缓冲产生VEXC=2.25V。分压滤波100nF，启动必须等待参考及缓冲稳定，不能套用正常300µs建立时间。
四个ROW_SEL各100k下拉；U4的SxB=VCM、SxA=VEXC，Dx送各行跟随器正输入。U1各输出经1k至板端ROW，10k从板端ROW送负输入，1nF从输出送负输入。全低为电气空白，单高为对应选行。不得两行同时选中并把数据解释为单点。
U2四个TIA正输入VCM；板端COL经10k接负输入，输出经4.99k||2.2nF反馈至板端COL。传感器电流主要流经Rf/Cf，不流经10k感测电阻；输入偏置/保护电流会在该电阻产生压降，动态增加极点，尚未验证。
J2 pin1–4=ROW0–3，pin5–8=COL0–3。外部16电阻位于传感阵列，不在板上伪造16个传感器元件。外线压降在板外，板端反馈不消除它。
各TIA输出经100Ω至ADS8684 AINxP，10nF从ADC输入到GND。所有AINxGND、AGND、DGND归GND，35DNC严格NC；DAISY/REFSEL低，内部4.096V参考，REFIO22µF、REFCAP1µF。输入范围固件设置0–5.12V。
STM32 SPI1使用PA5/6/7，PA4软件CS，PB0复位ADC，PA0–3行选择；PA9/10 UART，PA13/14 SWD。PA14复位默认BOOT0功能/option bytes需按ST配置确认，禁止依赖浮动引脚进入启动模式。使用内部时钟，无未验证晶振。VDD、VDDA同一3.3V管脚4，VSS/VSSA pin5。SWD/UART接口仅3.3V逻辑。
## 正常静态余量
选行最大吸收4×0.25/800=1.25mA。1k±1%输出隔离，最坏输出约2.25−1.25mA×1010=0.9875V，理想DC有输出余量；实际输出摆幅/温度和共同封装限制另验证。TIA差值范围0.1559375–1.559375V，理想输出2.6559375–4.059375V。
## 故障定义和HOLD
一次单故障：任一ROW/COL对GND或5.25V硬短路、ROW–COL短路/单元短路、单元或电极线开路、MCU复位HiZ、3.3V先失/5V先失/慢启动。源阻抗不以虚构电阻减轻故障。
1k行电阻最坏分支电流上界5.25/990=5.303mA，耗散≤27.84mW；这是电阻静态边界，不证明运放多通道60s热安全。OPA单通道对地短路资料不能扩展为同封装多路/电源短路保证。
10k感测电阻限制输入钳位电流粗界5.25/9990=0.526mA；不证明掉电内部保护、供电轨反灌和全板无损。Rf故障电流粗界5.25/4985.01=1.053mA，耗散≤5.53mW。Cf短路瞬态不可由DC电阻界覆盖。
MCU复位/3.3V先失时下拉使MUX命令返回VCM，但没有硬件故障断开或电源良好联锁。5V失电时外部强制5V仍可能回灌；LDO反向电流、ADC DVDD与AVDD排序、输入绝对最大和多路热安全未闭合。故障硬件覆盖不足明确FAULT_PROTECTION_HOLD，不宣称60s无损，不允许上电。
固件规划：缺数据/饱和/零或负差值/非法通道/电源状态无效立即丢弃，最迟下一10ms帧标记故障；恢复先校验供电、参考、ADC寄存器并连续2完整有效帧。仅固件规划无固件实测，无电源监控硬件，故障检测本身仍HOLD。外部强制5V可能损伤传感材料，本板保护不保证材料安全。
## 验收待办
正常AC/瞬态需厂家模型及实测覆盖行/4TIA/VCM/VEXC与耦合阵列、全部交越；PM nominal≥60°/corners≥45°且GM≥10dB。60s单故障温升/绝对最大、掉电回灌、短路移除恢复均需闭合后另申请bench门。无PCB/制造/采购。
''')
doc('ERROR_CALIBRATION_AND_TIMING.md','''# 误差、校准和时序
每点邻近电气空白D=activeADC−blankADC，以两个已测标准电阻1k/6.8k建立D=a/R+b，Rhat=a/(D−b)，禁止两点R线性插值。标准不确定度目标≤0.05%；25°C校准、20–30°C复查，其他真实电阻0.8/1.5/3.3/4.7/7/8k与邻点改变；目标校准后≤1%读数、1000连续帧标准差≤0.2%，非压力精度、非1000帧平均后的假通过。
分配conductance误差：增益0.15%、零点/偏置/漏电0.10%、线阻/保护/邻点0.20%、动态0.15%、ADC0.30%，合计0.90%；反算R界0.009/(1−0.009)=0.9082%。这些是预算，不是验证结果。有限线阻造成邻点依赖不能仅用逐点校准消除。首版线阻上限由本包敏感性结果约束，不能把1Ω例子默认当通过范围。
0–5.12V的16bit LSB=78.125µV。两次读数最坏INL差4LSB，量化差1LSB，总390.625µV；在R=8k、S=155.9375mV时conductance约0.250501%，尚在0.30%分配内，其余参考温漂/采集误差需另计。噪声、相关性及4次平均的收益未证明，不保证重复标准差。
每个正常切换后ADC输入剩余≤100µV，blank/active合并≤200µV，最小信号约0.1283%；300µs是待验证目标，不能因理想RC时间常数推断运放稳定。
时序规划每行2500µs：blank300µs；blank采集800µs；active300µs；active采集800µs；控制/额外dummy300µs。总10000µs。每个800µs窗口16个50µs采样slot，4通道各4次。SPI4MHz×32clocks=8µs，ADC转换在CS下降沿采样，当前通道由前帧命令选择（ADS8684 RevC p38–39），SDO是该当前转换结果，不能按本帧SDI通道编号贴标签。
实际规划在每个300µs建立区末端发送MAN_CH0完整32clock帧，弃其当前结果，下一窗口首slot转CH0，命令CH1；随后CH1/2/3循环。切换后首dummy采样必须弃掉并留足300µs至首有效CS边沿。首次进入MAN模式、复位、寄存器操作和范围更改的额外帧独立startup，不占稳态有效数据；读回ADC通道/范围/状态，正确对齐是固件验收项，未执行真实SPI。
基线与active采样差值方差Var(D)=Var(A)+Var(B)−2Cov(A,B)，不能假定不相关。ADC/线阻DC分析不验证SPI硬件、PM/GM、300µs建立或噪声。
''')
rows=[]
for q in plan['parts']:
 d=lib[q['device']]['device'];pins={a['number']:a for a in lib[q['device']]['pins']}
 for n,net in q['nets'].items():
  rows.append(dict(ref=q['ref'],value=q['value'] or q['device'],manufacturer_part=d.get('manufacturerId') or 'NATIVE_GENERIC_HEADER_TRACEABILITY_HOLD',supplier_id=d.get('supplierId'),device_uuid=d['uuid'],symbol_uuid=d['symbolUuid'],footprint_uuid=d['footprintUuid'],footprint_name=d['footprintName'],physical_pin=n,symbol_function=pins[n]['name'],net=net or 'NC',page=plan['page_names'][q['page']],identity='CORE_MANUFACTURER_PINMAP_VERIFIED' if q['ref'].startswith('U') else 'NATIVE_SYMBOL_PAD_NUMERIC_CORRESPONDENCE',remaining='post-reopen audit pending; dynamic/fault/assembly qualifications hold'))
with(p/'EXACT_BOM_AND_PINMAP.csv').open('w',encoding='utf-8-sig',newline='')as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(json.dumps({'P2':'DESIGN_DEFINED_WITH_EXPLICIT_HOLDS','components':len(plan['parts']),'pinmap_rows':len(rows),'revision_rounds':1}))
