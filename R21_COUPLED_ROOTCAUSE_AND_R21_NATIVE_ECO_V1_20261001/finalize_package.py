from pathlib import Path
import csv,json,hashlib,datetime,re,os
import numpy as np
from science import ROOT,dump,sha,utc
def readable():
    count=0
    for p in sorted((ROOT/'results').glob('*/*.txt')):
        if p.name not in ['op.txt','ac.txt','trace.txt']:continue
        try:
            a=np.loadtxt(p,skiprows=1);head=p.read_text().splitlines()[0].split();a=np.atleast_2d(a)
            if a.shape[1]!=len(head):continue
            cols=[];seen={}
            for n in head:
                seen[n]=seen.get(n,0)+1;cols.append(n if seen[n]==1 else n+'_column'+str(seen[n]))
            np.savetxt(p.with_suffix('.csv'),a,delimiter=',',header=','.join(cols),comments='',fmt='%.15g');count+=1
        except (ValueError,OSError):continue
    return count
def plots():
    os.environ['MPLCONFIGDIR']=str(ROOT/'plots'/'.mplconfig')
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size':10,'axes.grid':True,'grid.alpha':.25})
    fig,axs=plt.subplots(2,2,figsize=(12,8),constrained_layout=True)
    for col,kind in enumerate(['row','tia']):
        old=np.loadtxt(ROOT/'results'/('METHOD_'+kind+'.csv'),delimiter=',',skiprows=1);new=np.loadtxt(ROOT/'results'/('YPORT_'+kind+'.csv'),delimiter=',',skiprows=1)
        f=old[:,0]
        for z,label,style in [(old[:,1]+1j*old[:,2],'Old series voltage','--'),(new[:,1]+1j*new[:,2],'Independent Y ports','-'),(new[:,3]+1j*new[:,4],'Tian two-port',':')]:
            axs[0,col].semilogx(f,20*np.log10(abs(z)),style,label=label);axs[1,col].semilogx(f,np.unwrap(np.angle(z))*180/np.pi,style)
        axs[0,col].axhline(0,color='k',lw=.6);axs[0,col].set_title(kind.upper()+' nominal frozen candidate');axs[0,col].set_ylabel('Return ratio magnitude (dB)');axs[0,col].legend(fontsize=8)
        axs[1,col].set_xlabel('Frequency (Hz)');axs[1,col].set_ylabel('Phase (deg)')
    fig.suptitle('Loading-preserving method verification — not full-board stability');fig.savefig(ROOT/'plots'/'RETURN_RATIO_METHODS.png',dpi=180);plt.close(fig)
    fig,ax=plt.subplots(2,1,figsize=(11,7),constrained_layout=True)
    metrics=json.loads((ROOT/'TRANSIENT_RESULTS.json').read_text())
    for name in ['single_tia_repeat_trap','single_tia_repeat_tight']:
        p=ROOT/'results'/name/'trace.txt';a=np.loadtxt(p,skiprows=1);h=p.read_text().splitlines()[0].split();v=a[:,h.index('v(ain)')];t=a[:,0]*1e6;ref=float(np.median(v[t>1280]))
        ax[0].plot(t,v,label=name);ax[1].plot(t,(v-ref)*1e6,label=name)
        m=next(x for x in metrics if x['case']==name)['measurements'][0];e=np.array(m['edge_times_us']);ax[1].plot(e,(np.interp(e,t,v)-ref)*1e6,'.',markersize=4)
    ax[0].set_ylabel('AIN (V)');ax[0].legend(fontsize=8);ax[0].axvline(100,color='k',ls=':');ax[1].set_xlim(390,1300);ax[1].set_ylim(-1,1);ax[1].set_xlabel('Time (us)');ax[1].set_ylabel('Residual to late plateau (uV)');fig.suptitle('Single TIA, ideal VCM / equivalent 4x800 Ohm: 32 real non-dummy edge times');fig.savefig(ROOT/'plots'/'SINGLE_TIA_SETTLING.png',dpi=180);plt.close(fig)
    names=['part_1row_1tia_800_gear','part_4row_1tia_800_gear_180','part_1row_4tia_800_gear_180','full_monolithic_short_final'];values=[]
    for n in names:
        q=ROOT/'results'/n;p=q/'trace.txt';j=json.loads((q/'STATUS.json').read_text());values.append((np.loadtxt(p,skiprows=1)[-1,0]if p.exists()else j.get('lastProgressTime_s',0))*1e6)
    fig,ax=plt.subplots(figsize=(10,4),constrained_layout=True);ax.barh(['4 macros Gear, completed','7 macros: 4row+1TIA','7 macros: 1row+4TIA','10 macros: final short window'],values,color=['#1b9e77','#d95f02','#d95f02','#7570b3']);ax.axvline(600,color='k',ls='--',label='600us trace endpoint');ax.set_xlabel('Integrated simulation time (us)');ax.legend(fontsize=8);ax.set_title('Numerical completion evidence — orange/purple bars are forced stops');fig.savefig(ROOT/'plots'/'COUPLED_PROGRESS.png',dpi=180);plt.close(fig)
def report():
    method=json.loads((ROOT/'RETURN_RATIO_INDEPENDENT_VALIDATION.json').read_text());reset=json.loads((ROOT/'RESET_RESULTS.json').read_text());tr=json.loads((ROOT/'TRANSIENT_RESULTS.json').read_text());stat=json.loads((ROOT/'STATIC_COUPLED_RESULTS.json').read_text());b=json.loads((ROOT/'EXECUTION_BUDGET.json').read_text())
    rows=['| 类别 | Tian fc (MHz) | Tian PM (°) | 独立Y端口 fc (MHz) | 独立Y端口 PM (°) |','|---|---:|---:|---:|---:|']
    for x in method:
        if x['class']=='fixture':continue
        a,c=x['Tian'][0],x['Y_ports'][0];rows.append(f"|{x['class']}|{a['fc_Hz']/1e6:.6f}|{a['PM_deg']:.6f}|{c['fc_Hz']/1e6:.6f}|{c['PM_deg']:.6f}|")
    txt=f'''# SCIENCE_ADK5556_4X4_R21_COUPLED_ROOTCAUSE_AND_R21_NATIVE_ECO_V1 完整阻断回执

裁定：CIRCUIT-PRO-R21-BLOCKED-ACCEPT-COUPLED-CLOSURE-20261001-04；全文见PRO_COUPLED_RULING_FULL.md。
冻结输入：R2 commit da6ca87b9f49c5af03a16c24af6186d7c5c2e0d3；R2.1验证 commit c13555a330f8ad676750b8fec5d5d42bfc0b5edb。
用户第二阶段已允许恢复沟通与普通技术连续推进。没有重复原交付或旧PART；没有新增原生工程。

## 结果与进入门

| 门 | 本包结果 | 范围 |
|---|---|---|
| RETURN_RATIO_METHOD_VALIDATED | PASS：冻结候选的返回比方法交叉 | 双注入与独立端口导纳；并非整板物理稳定 |
| PARTITIONED_COUPLED_DYNAMIC_PASS | HOLD | 关键7宏模型未完整获得300us后有效窗口 |
| FULL_STATIC_COUPLED_NO_INSTABILITY_EVIDENCE | HOLD | 9个要求的标称静态状态均有有限DC/AC；电源角点与PZ未闭合，有限频率AC不能证明无RHP极点 |
| RESET_DIRECT_PATH_PASS | HOLD；25°C正常OD断言/释放解析有裕量 | 高温BAT54S漏电没有保证上界；±故障钳位、回灌、热与瞬态不放行 |
| FAULT_LATENCY_LOGIC_CONTRACT_PASS | 逻辑契约PASS | 明确依赖≤1ms接收tick、≤0.5ms合格传输/时间基转换；硬件WCET未验证 |

P3进入门未过，工作副本/session/save/File capture/audit/ERC/PDF全部0。旧R2原生工程未打开、未修改。
保持DYNAMIC_VALIDATION_HOLD、FAULT_PROTECTION_HOLD、REFERENCE_CAPACITANCE_HOLD、ERC_DETAIL_HOLD、DRAWING_LAYOUT_HOLD、METADATA_DETAIL_HOLD、BENCH_NOT_RELEASED及COUPLED_MODEL_CONVERGENCE_HOLD。
放弃G17→G07候选的历史RESET_THRESHOLD_ENVELOPE_HOLD仍按裁定退出主线。当前活动缺口是RESET_DIRECT_PATH_HOLD，不将历史退出误称新复位已通过。

## 1. 确认并修正耦合测试台偏置错误

冻结原生R2实际分压：RD_TOP=10kΩ，底臂九个10kΩ串联，共90kΩ，正确输出0.9×VCM=2.25V。
旧make_coupled.py写成上臂90k、下臂10k，产生0.25V。旧实际工作点VCM2.48829V、VEXC命令0.248814V、VEXC0.245138V，支持此根因。
先对旧脚本执行独立偏置契约，RED退出1；只在新目录修正为上10k/下90k，GREEN退出0。
旧三次耦合失败及原文件全部保留；不能继续把它们描述为目标2.25V下的耦合数值失败，也不能据此判物理不稳定。
修正后的新宏模型工作点在有效标称工况达到VCM约2.500000V、VEXC约2.250000V。本文没有改变电路E/Rf/主器件系列。
证据：evidence/BIAS_REGRESSION_RED_GREEN.json；test_bias_contract.py；cases/中每个真实netlist；results/的实际OP与日志。

## 2. 返回比方法核实与修复

原串联电压比 -V(fb)/V(minus) 与保持加载的双注入法明显不同：原行/共同缓冲PM约105°而修正约99°；TIA原约121°而修正约101°。原方法的高阻近似在主交越附近受到输入加载/双向传输影响，不能继续使用旧PM作为正式门值。
采用[Tian等原始论文](https://community.cadence.com/cfs-file/__key/communityserver-discussions-components-files/38/00900125_5F00_striving_5F00_for_5F00_small_5F00_signal_5F00_stability_5F00_circuits_5F00_devices_5F00_2001.pdf)的双端口定义。
VTEST由minus到fb，ITEST由地注入minus；if=-I(VTEST)，ve=V(minus)。电压/电流两个独立AC运行给出B,D及A,C。
本实现从两个端口KCL自行展开，T=[2(AD-BC)-A+D]/[1-2(AD-BC)+A-D]。
独立方法在AC断开/DC保留的两个端口施加两组激励，按实际端口电压和电流求Y矩阵，消除有限耦合电容与偏置电感的影响，T=(Y12+Y21)/(Y11+Y22)。这是不同测试拓扑、不同测量量和独立求逆实现的交叉；不改变厂商模型。
已知一阶解析fixture确认符号与加载修正，双注入相对误差最大约7.98e-7，独立Y端口约1.33e-7。

{chr(10).join(rows)}

1Hz–100MHz范围内，各类两种方法均只发现一个下降交越；fc差远低于10%，PM差远低于5°。所有已发现交越均解释，不以PM>100°推导绝对稳定。
失败证据保留：最初超大AC隔离电容引起数值相消，且transient-OP未保留正确DC；TIA纯DC也曾落入非物理偏置。最终采用有限端口电压矩阵修正及来自真实OP的nodeset初始猜测，不用强制IC、不改原厂模型。一次nodeset变量名重复包v()的脚本错误也保留在diag_yport4日志，并在diag_yport5纠正。
OP一致性检查与ADC采样建立是不同量：原先自行施加的整向量100uV规则曾拒绝约115uV的driver偏差。该失败JSON保留；最终对偏置线性化采用1mV一致性检查。原裁定fc10%/PM5°与ADC100uV阈值均未改变；输入OP差最大约108uV，独立返回比曲线仍吻合。详见RETURN_RATIO_INDEPENDENT_VALIDATION.json，不冒称两个OP逐节点严格相等。

## 3. 完整静态耦合与暂态

实际87个SPICE进程记录见CASE_EXECUTION_INDEX.csv；必须同时看分析错误和输出，不能将ngspice正常退出码0等同分析成功。
完整静态AC用满24次，包括失败与重新种子/节点排序对照。11次得到有效DC/AC，覆盖全部9个要求的标称组合：all-blank/ROW0/ROW1 × 全800/全8000/高目标低邻居。没有在这些有效标称OP发现输出削顶。
两次图同构ROW0/ROW1节点/实例重命名用于数值排序诊断，元数据按实际网表重新核对；它们不改变元件数值、拓扑或物理工作状态。
4.75V/5.25V完整网络工况未取得有效DC/AC，不把数值失败叫物理削顶，也不把标称结果扩展成全供电角点保证。
4个PZ尝试均无可用极点结果：有输入信号短接路径错误和OP求解失败。失败原因尚未充分定位，不冒称原厂模型确定不支持PZ。部分pz.raw实际是Operating Point plot而非极点，明确不计作极点证据。静态AC有限频率响应没有证明无右半平面极点，因此门保持HOLD。

正常暂态实际20次（含1次同时扣特殊完整模型诊断），共20个暂态过程；每例初始wall上限≤180s，最终10宏模型诊断取60s，未延长到8min。所有超时/15s积分停滞停止均是自有子进程，FORCED_STOP_NOT_NORMAL_EXIT与日志保留，不伪装正常结束。
关键800Ω分区：4row+1TIA Gear180s只到375.633us；1row+4TIA Gear180s只到287.162us；没有完整600us轨迹，不能验证切换100us后300us有效窗口及全部边沿。其他高目标/8000Ω、trap与KLU对照同样未给出关键完整轨迹。
KLU出现的“out of memory/needed element”属于实际求解器错误日志，未将其解释为宿主RAM耗尽；无新执行器安装或全局配置变化。
4宏模型VCM/VEXC+1row+1TIA的Gear诊断完成600us，8个短窗AIN0有效边沿最大残余约3.04e-8V，连续切换后300–500us最大约4.59e-8V。其余边界为理想行/列端口；不算完整帧、不算7/10宏模型证据，Gear不单独证明物理稳定。
单TIA复算使用真正32个非dummy CS时刻，覆盖1.2ms活动状态，理想VCM与等效4×800Ω负载。默认trap与reltol1e-5/vntol1e-8/abstol1e-12对照均完成1.3ms，最大边沿残余分别约2.24e-8V与2.16e-8V。仅复核此前已接受的局部筛查，不扩为整板。
图和可读CSV见plots/与各results/子目录；原始空格TXT与netlist同时保留。

## 4. 直接NRST解析与保证值范围

候选仍为J3.5→1k±1%→PGOOD/NRST，保留10k上拉、MCU内部上拉、BAT54S和并联TPS3890开漏RESET，不加入G17→G07链。这里没有实施原生。
外部契约是active-low OD/OC，释放Hi-Z，VOL≤0.4V；不能据此保证任意调试器或任意5V推挽源兼容。复位有效低脉宽须在NRST节点满足器件要求；线缆/节点RC尚未实测。
[STM32G031K8原厂数据](https://www.st.com/resource/en/datasheet/stm32g031k8.pdf)，DS12992 Rev4：低/高门限0.3/0.7×VDDIO1；NRST上拉25–55kΩ，内部reset可能关闭该上拉，故释放计算也覆盖内部上拉关闭。输入泄漏70nA，另将产品pad基础10uA保守分配到NRST。该部分引用保证参数，不将典型迟滞当阈值保证。
冻结[BAT54S资料](https://assets.nexperia.com/documents/data-sheet/BAT54S.pdf)只给25°C下2uA反向漏电保证，高温图为典型值；不能用典型曲线构造保证上界。保留PGOOD所接[SN74LVC1G17](https://www.ti.com/lit/ds/symlink/sn74lvc1g17.pdf)输入5uA界，以及两颗[TPS3890](https://www.ti.com/lit/ds/symlink/tps3890.pdf)各250nA开漏漏电。合计保守泄漏预算17.57uA。
60个解析工况=32个OD断言+16个Hi-Z释放+8个±5V说明性限流+4个并联开漏状态。不是宏模型故障模拟或实物试验。
25°C正常OD最坏NRST={reset['assert_max_NRST_V']:.9f}V；跨供电保守比较低阈值0.9195V，裕量{reset['conservative_unpaired_assert_margin_V']:.9f}V。释放最小裕量{reset['release_min_margin_V']:.9f}V；TPS最坏所需sink约0.490mA，低于2mA保证测试点。
±5V表仅是给定说明性钳位电压的串阻电流/功耗计算，未证明所有引脚绝对电压、未供电回灌、动态注入或60s热安全。温度保证与故障保护未闭合，故不宣布RESET_DIRECT_PATH_PASS，更不宣布FAULT_PROTECTION_PASS。
原厂PDF直接下载分别遭403/567；网页读取STM32正式PDF成功，表号/版本/URL保存；既有冻结BAT/TPS/G17文件用于复核。没有安装requests等缺失库，没有绕过认证或改系统。

## 5. 帧内progress watchdog逻辑契约

protocol.py/test_protocol.py是冻结R2.1原21项核心回归，未修改；progress_protocol.py是合成接收器与进度/失效的组合契约，test_progress.py补11项，总32项回归通过。RED基线11项中8项失败；终审另发现健康状态下旧epoch reset/错误configure会抛异常却保留资格，扩充现有test_07先RED复现，再仅修新wrapper立即clear，最后32项GREEN。冻结基类与原21项未改。所有日志保存。测试项内的多状态/非有限值覆盖如实记录，不当成新的硬件试验次数。
heartbeat携带epoch、current frame_id、完成state_index0..7、最后有效状态采样完成时间、累计32×(state+1)样本数。必须观察一帧全部八状态后才允许该完整帧参与两帧连续资格；跳状态、重放、未来/非有限时间、无状态前进而篡改采样时间均失效。
缺heartbeat4.5ms或进度2.5ms无前进立即清DATA_VALID；同状态原封不动heartbeat不续进度期限。clear保留receive-clock及进度/完整帧防重放水位；新epoch保持接收时钟单调。PGOOD低与标签/范围错误在模型调用时立即失效，恢复必须两个真正新完整帧。
“≤10ms”是有条件的逻辑设计契约：接收tick间隔≤1ms，队列/转换后capture到receive≤0.5ms，发送进度依据已完成有效采样而非伪造主循环计数。用保守1ms报告/排队余量，冻结进度失效≤5ms、丢heartbeat≤7ms，均<10ms；8状态注入冻结的离线测试通过。
真实MCU/WCET/UART/SPI/时钟同步/硬件禁激励延迟未执行、未验证。10.25ms只作数据新鲜度，不再承担安全失效时延证明。逻辑契约PASS不解除硬件或bench门。

## 6. 通信漏跟自查与修复

确证失效点：旧等待automation删除后，R2发送后虽有两次读回、最后06:47:25仍active，却06:48:22结束本轮，缺少接续automation。直到用户08:04:39追问，08:05:50才恢复read；回复检查间隔78min25s。不是科学许可不足，也不能把“发送成功”当作“收到裁定”。
新的交付生命周期区分SEND_ACCEPTED、HISTORY_CONFIRMED、REPLY_GENERATING、SYSTEM_ERROR、FULL_RULING_RECEIVED、DECISION_CONSUMED。发送与正文hash/commit/历史ID记账；立即fresh read确认；在结束本轮前建立明确owner、nextCheckAtUTC和接续监控。第一项新报错本地可见；重复相同报错不轰炸、不重发已送内容。
本次恢复先只读对账，全文保存已有新裁定后才删除旧r2-1等待automation并执行此唯一包。没有重发旧报告、旧PART或恢复催问。此次新GitHub交付只发一条简短摘要、索引与固定commit。网页是否实际读完未验证，且不是附加等待门。
下一次重大裁定仍先全文读取保存；普通实现与进度在本地累计；未获新预算不越过本包STOP，不另开网页对话或更换模型绕过。

## 7. 下一轮集中申请——明确由用户提出

**用户新增要求：下次正常报告同时申请更多工作预算（执行时间、计算/试验次数、自主范围），减少反复请示；本条不是模型平台额度扩展。** 此次将申请与本完整回执一起提交，未获批不执行。
建议仅一个下一包，继续冻结架构与候选：总360min，P0方法/求解诊断60min、P1关键分区及全静态闭合120min、P2复位保证/逻辑补缺60min、条件原生ECO90min、完整发布及回复安排30min。
拟申请DC/AC/PZ合计≤128个工况，正常短窗≤64，数值方法/排序/容差诊断属性≤16且同时计入其DC/AC/PZ或暂态次数（不是额外分析额度），reset解析≤96，协议测试≤48，原厂资料≤8；无bench/物理试验，无第三方安装，无新执行器，普通暂态180s及停滞立即停、完整长窗最多1次≤8min约束保留。原生仍只在完整进入门通过后，副本1/session≤2/save≤8/capture-audit≤4/ERC≤2/PDF≤2。
预算用途：修正PZ端口/验证资格或确认其能力边界；定位7宏模型在正确偏置下的数值刚性；优先验证关键分区有效窗口及供电角点，避免大量完整帧盲跑；为温度漏电保证缺口取得原厂保证或裁定明确有效温度域。
拟自主范围：普通测试台一致性、数值排序、限时重试、可读结果与协议回归在包内累计；只在真实增长振荡、削顶、方法冲突、需要改变E/Rf/OPA/ADC/fps、预算/范围变化或必需验收时集中再请裁定。不得用此建议扩PCB/制造/采购/本地Git/系统/bench权限。
需要网页此次集中裁定：接受哪些方法/局部筛查；关键7宏模型仍不足时优先的唯一数值/验证路线；RESET温度保证域与±故障门如何界定；批准/修改上述唯一更大有界包。没有自行生成第三套补偿或新原生工程。

## 8. 预算与交付索引

**预算执行偏差：P0实际DC/AC/PZ分析39/32，超额7。** 原账把7次含DC/AC的诊断当成额外互斥额度，这是执行分类错误，不是新增授权；原标签账及全部失败证据保留在BUDGET_CLASSIFICATION_AUDIT.json。诊断属性7/8必须同时扣分析次数。已停止所有新科学运行，原数据保留供裁定；不声称预算全PASS，不要求追认就视作自动放行。runner已改为按实际分析与诊断属性双扣、所有额度预检通过后才记账/启动；隔离临时账的1项基础设施RED/GREEN验证没有调用求解器。P1完整静态AC24/24，正常暂态实际20/32，PZ4/12，完整10宏模型短窗同时扣特殊诊断1/1（60s）；P2解析60/64，回归测试32/32，复位相关原厂资料4/6，库0；P3所有操作0。
主动阶段的实际时间边界/累计记录见EXECUTION_BUDGET.json。P4上限15min，发布与匿名读回、send历史确认、接续监控的最终实耗在独立送达账保存；不将上传前快照冒称完整发布后的实耗。
所有新科学结果在独立目录；原冻结模型SHA与执行器SHA见INPUT_VERIFIED.json；原生R2输入未修改；没有在E:\\open做Git写操作。
README.md、CASE_EXECUTION_INDEX.csv、RETURN_RATIO_INDEPENDENT_VALIDATION.json、STATIC_COUPLED_RESULTS.json、TRANSIENT_RESULTS.json、RESET_RESULTS.json及results/RESET_60_CORNERS.csv提供总索引。原始cases/models/results/logs、可读CSV、3PNG图和全文都直接提供，不仅是ZIP/LFS指针。附件SHA清单发布前冻结。

END-OF-COMPLETE-R21-COUPLED-ROOTCAUSE-AND-NATIVE-ECO-BLOCKED-RECEIPT
FINAL-GITHUB-COMPLETE-DELIVERY
'''
    (ROOT/'COMPLETE_COUPLED_RECEIPT.md').write_text(txt,encoding='utf-8')
    (ROOT/'README.md').write_text('''# R2.1 coupled root-cause and conditional native ECO — BLOCKED receipt

完整正文：[COMPLETE_COUPLED_RECEIPT.md](COMPLETE_COUPLED_RECEIPT.md)。本包没有新原生工程；单环路方法已修复，关键7宏模型动态及全静态极点/电源角点、复位保证域仍HOLD。bench/制造未放行。

- [裁定全文](PRO_COUPLED_RULING_FULL.md) / [冻结输入SHA](INPUT_VERIFIED.json)
- [87例执行/错误/限时账](CASE_EXECUTION_INDEX.csv) / [当前预算快照](EXECUTION_BUDGET.json)
- [返回比方法交叉](RETURN_RATIO_INDEPENDENT_VALIDATION.json) / [静态DC/AC](STATIC_COUPLED_RESULTS.json)
- [实际暂态与边沿范围](TRANSIENT_RESULTS.json) / [60个复位解析角点](results/RESET_60_CORNERS.csv)
- [progress组合契约](progress_protocol.py) / [32项回归](test_protocol.py) + [test_progress.py](test_progress.py)
- [返回比图](plots/RETURN_RATIO_METHODS.png) / [单TIA32边沿图](plots/SINGLE_TIA_SETTLING.png) / [耦合积分进度](plots/COUPLED_PROGRESS.png)

cases/为真正运行的netlist与配置；results/每例有STATUS/DISPATCH/stdout/stderr及可用原始OP/AC/trace和可读CSV。错误/缺数据不构成PASS。evidence/保留RED/GREEN、偏置错误、失败方法与初始判据。sources/仅本项目引用的既有原厂资料，源链接/参数见全文；没有把下载失败说成成功。

原V1/R2/R2.1验证目录和原文件保持冻结。下一轮更大有界预算申请明确来自用户，尚待集中新裁定。
''',encoding='utf-8')
    gates={'RETURN_RATIO_METHOD_VALIDATED':'SCOPED_PASS','PARTITIONED_COUPLED_DYNAMIC_PASS':'HOLD','FULL_STATIC_COUPLED_NO_INSTABILITY_EVIDENCE':'HOLD','RESET_DIRECT_PATH_PASS':'HOLD_25C_NORMAL_BOUNDS_ONLY','FAULT_LATENCY_LOGIC_CONTRACT_PASS':'PASS_WITH_EXPLICIT_TIMING_OBLIGATIONS','P3':'NOT_ENTERED','BENCH':'NOT_RELEASED','RESOURCE_EXECUTION':'P0_COUNT_OVERRUN_7_REQUIRES_REVIEW'}
    dump(ROOT/'GATES.json',gates)
if __name__=='__main__':
    count=readable();plots();report();print(json.dumps({'readableCSV':count,'reportSHA256':sha(ROOT/'COMPLETE_COUPLED_RECEIPT.md'),'reportBytes':(ROOT/'COMPLETE_COUPLED_RECEIPT.md').stat().st_size,'PNG':3}))
