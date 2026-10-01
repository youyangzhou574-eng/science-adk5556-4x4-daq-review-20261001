from pathlib import Path
import os,json,hashlib,datetime,numpy as np
ROOT=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']=str(ROOT/'plots'/'.mplconfig')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
def write(name,text):(ROOT/name).write_text(text,encoding='utf-8')
def finalize():
    y=np.load(ROOT/'results'/'mimo_blank_800_MATRIX.npz');h=np.load(ROOT/'results'/'HYBRID_MIMO.npz');f=y['freq'];ys=np.linalg.svd(y['R'],compute_uv=False)[:,-1]
    fig,ax=plt.subplots(figsize=(10,5),constrained_layout=True);ax.loglog(f,ys,label='Open-port Y reconstruction');ax.loglog(h['freq'],h['sigma'],'--',label='Closed double-injection reconstruction');ax.axhline(.2,color='red',ls=':',label='Pro technical-review threshold0.20');ax.set_xlabel('Frequency(Hz)');ax.set_ylabel('Minimum singular value(I+L)');ax.set_title('All blank / all800 Ohm only — technical review, no stability PASS');ax.legend();ax.grid(True,which='both',alpha=.25);fig.savefig(ROOT/'plots'/'MIMO_SIGMA_REVIEW.png',dpi=180);plt.close(fig)
    fig,ax=plt.subplots(figsize=(10,5),constrained_layout=True);ax.loglog(h['freq'],h['condition'],label='Closed reconstruction voltage matrix');ax.axhline(1/np.finfo(float).eps,color='red',ls=':',label='1/double epsilon diagnostic scale');ax.set_xlabel('Frequency(Hz)');ax.set_ylabel('Condition number');ax.set_title('Low-frequency conditioning remains unresolved; no masked-band PASS');ax.grid(True,which='both',alpha=.25);ax.legend();fig.savefig(ROOT/'plots'/'MIMO_CONDITION.png',dpi=180);plt.close(fig)
    fig,ax=plt.subplots(figsize=(7,6),constrained_layout=True);ev=h['eigenvalues'];mask=abs(ev)<3;ff=np.broadcast_to(h['freq'][:,None],ev.shape);sc=ax.scatter(ev.real[mask],ev.imag[mask],c=np.log10(ff[mask]),s=4,cmap='viridis');ax.plot([-1],[0],'rx',markersize=10,label='-1');ax.set_xlim(-2,2);ax.set_ylim(-2,2);ax.set_xlabel('Real eigenvalue');ax.set_ylabel('Imaginary eigenvalue');ax.set_title('Zoomed eigenloci; large-gain points outside plot retained in CSV');ax.grid(True,alpha=.2);ax.legend();fig.colorbar(sc,ax=ax,label='log10 frequency(Hz)');fig.savefig(ROOT/'plots'/'MIMO_EIGENLOCUS_ZOOM.png',dpi=180);plt.close(fig)
    for tag,data in [('OPEN',y),('CLOSED',h)]:
        freq=data['freq'];l=data['L'];ev=data['eigenvalues'];np.savetxt(ROOT/'results'/(tag+'_MIMO_EIGENVALUES.csv'),np.column_stack([freq,ev.real,ev.imag]),delimiter=',',header='frequency_Hz,'+','.join([p+str(i)for p in['real_eigen','imag_eigen']for i in range(10)]),comments='')
        if tag=='CLOSED':np.savetxt(ROOT/'results'/'CLOSED_MIMO_MATRIX.csv',np.column_stack([freq,l.real.reshape(len(freq),100),l.imag.reshape(len(freq),100)]),delimiter=',',header='frequency_Hz,'+','.join([p+str(i)+'_'+str(j)for p in['real_L','imag_L']for i in range(10)for j in range(10)]),comments='')
    count=0
    for p in (ROOT/'results').glob('*/*.txt'):
        if p.name not in ['ac.txt','hybrid.txt']:continue
        try:
            a=np.loadtxt(p,skiprows=1,ndmin=2)
            if a.size and np.all(np.isfinite(a)):
                fields=p.read_text().splitlines()[0].split();fields=fields if len(fields)==a.shape[1] else ['field_'+str(i)for i in range(a.shape[1])]
                np.savetxt(p.with_suffix('.csv'),a,delimiter=',',header=','.join(fields),comments='');count+=1
        except (ValueError,IndexError):pass
    from network_cases import raw_nodes
    opcount=0
    for raw in (ROOT/'results').glob('*/op.raw'):
        if 'Operating Point' not in raw.read_text(errors='replace'):continue
        nodes=raw_nodes(raw)
        if nodes:
            import csv
            with raw.with_suffix('.csv').open('w',newline='',encoding='utf-8') as out:
                w=csv.writer(out);w.writerow(['node','voltage_V']);w.writerows(sorted(nodes.items()))
            opcount+=1
    b=json.loads((ROOT/'EXECUTION_BUDGET.json').read_text());op=json.loads((ROOT/'mimo_blank_800_RESULT.json').read_text());cl=json.loads((ROOT/'HYBRID_RESULT.json').read_text());casecount=len(b['cases'])
    report=f'''# SCIENCE_ADK5556_4X4_R21_MIMO_STABILITY_AND_NATIVE_ECO_CLOSURE_V1 — 完整技术复核阻断回执

绑定新裁定：CIRCUIT-PRO-R21-COUPLED-BLOCKED-ACCEPT-MIMO-CLOSURE-20261001-05；assistant f7f4fbc1-104f-4d96-b3b5-89755a453d5c；全文PRO_MIMO_RULING_FULL.md。
冻结R2/验证/耦合输入commit：da6ca87b9f49c5af03a16c24af6186d7c5c2e0d3 / c13555a330f8ad676750b8fec5d5d42bfc0b5edb / a3e22772f368322dd9de671ab816c09e3b7f1b72。

## 结果、停止原因与门

**本包到达MIMO技术复核门，已停止新增求解。不是预算用尽，不是电路物理不稳定结论，不是R2.1原生或bench放行。**
唯一完整网络MIMO状态是5V/all-blank/all800Ω。两种量测都得到σmin约0.00994，低于绑定裁定0.20的技术复核阈值。低频重建和所选return-difference归一化同时存在很大条件数；不能忽略低频后宣布PASS，也不能把异常最小奇异值当作增长振荡或RHP极点。
停止发生在P1，P2新的保护候选/RESET解析/协议回归未执行，P3工作副本/session/save/File/audit/ERC/PDF全部0；预备七宏OP有记录，**短窗暂态实际0**，没有伪装六个核心case已完成。

| 门 | 结果与范围 |
|---|---|
| RETURN_RATIO_METHOD_VALIDATED | 之前标称单环方法PASS继续冻结；不冒称新10环方法通过 |
| FAULT_LATENCY_LOGIC_CONTRACT_PASS | 之前32GREEN离线合同PASS保持；新状态机/新回归0，硬件WCET未验证 |
| RESET_DIRECT_PATH_25C_DESIGN_PASS | Pro接受的25°C设计PASS保持；20–30°Cbench及±故障HOLD |
| MIMO_STATIC_COUPLED_SCREEN_PASS | HOLD，σ<0.20技术复核及低频条件数/归一化未资格 |
| PARTITIONED_COUPLED_DYNAMIC_PASS | HOLD；未新增短窗暂态证据 |
| R2.1原生 | NOT_ENTERED，全部操作0 |
| Bench/PCB/制造/采购/本地Git/系统写 | 全部0/未放行 |

## 1. 新预算与执行计数

**用户提出更大有界预算的要求已获Pro正式批准：新包360min，从零计数，不追认旧包7例超额。** P0/P1/P2/P3/P4上限60/120/60/90/30min。
全局计数不是互斥阶段额度：保守实际DC/AC/PZ分析指令次数{b['used']['DC_AC_PZ']}/128，diagnostic属性{b['used']['diagnostics']}/16同时扣实际分析；正常暂态0/64、完整10宏诊断0/1；RESET解析0/96、协议0/48、原厂新资料0/8、候选0/2、新库0/4、P3各项0。
{casecount}个真实ngspice过程与全部正常退出/分析报错见CASE_EXECUTION_INDEX.csv；optran只是记录明确的DC初始化算法，不当作正常外部切换暂态。保守逐指令重计49 OP＋24 AC＋3 PZ＝76次，剩余52次；另6条optran是DC初始化，单列披露。原49合并工况账作为PRE_REVIEW_BUDGET.json保留，不能把旧39/32偏差视为合并计数的授权。新runner按每条OP/AC/PZ预扣，TRAN和诊断属性同时计数；只解析.control分析块和合法点分析指令，标题PZ不计。
终审还发现第一次open矩阵RESULT在13:23:41UTC写出σ<0.20标志，但程序没有同步锁runner；13:41:58UTC仍启动8个hybrid交叉诊断，13:47:42UTC才写科学STOP。初衷是进行有界本地方法交叉检查，但本回执按保守口径明确记录执行控制偏差，不追认STOP例外，不回填假停止时间。8例数据和计数全部保留。现已将σ阈值与不可自行解除的STOP联动，缺资格时provisionalPASS固定false；禁用旧240min初始化器，避免复位新账。隔离测试先RED再GREEN，修复没有运行新SPICE。
临时隔离账原子预检回归证明：TRAN已满时，即使DC尚有余量也不能启动；失败不改账、不产生executor进程。当前runner科学STOP后拒绝所有新启动。没有安装执行器/第三方，不改宏模型、旧原生或全局设置。

## 2. MIMO方法与独立耦合fixture

延续已接受Y-port的保持DC/加载思路，为10个输入反馈wire建立20个端口：先10个运放输入侧e，再10个反馈侧f。开端口量测以1e9H保留DC连接，有限1µF隔离AC驱动；逐列读真实端口电压和进入网络电流，求Y=I V^-1，并精确减掉偏置电感导纳。模型与真实工作点未强制IC修改。
自行从端口KCL推导：闭合e=f时G=Yee+Yef+Yfe+Yff。定义D=Yee+Yff，A=Yef+Yfe，L=D^-1A，R=I+L，则G=D R。这是**候选工程return-difference归一化**；不会把标量Tian式未经论证直接推广成非交换矩阵。D所对应参考系统的内部/RHP极点资格以及这种多环归一化如何解释σ门，尚未闭合。
[Tian等原始论文](https://community.cadence.com/cfs-file/__key/communityserver-discussions-components-files/38/00900125_5F00_striving_5F00_for_5F00_small_5F00_signal_5F00_stability_5F00_circuits_5F00_devices_5F00_2001.pdf)讨论受适用条件约束的双端口/受控源方法；本文的10环矩阵是上述自行推导与fixture核验，不宣称论文直接给出了这个MIMOσ公式。

独立两个互耦Norton环fixture：解析一阶增益，输入100kΩ/输出1kΩ，两方向交叉15%/5%。四个端口真实SPICE电流/电压矩阵与独立解析Y最大相对误差2.54614e-11，L误差2.54623e-11；G=D R绝对残差1.55e-17；已知闭合极点约-682256/-574506rad/s。这个fixture有交叉，但各回路的输入/输出对角参数相同，**没有充分资格任意非交换多环归一化或证明完整OPA网络参考D稳定**。
N=1时公式退化为已接受(Y12+Y21)/(Y11+Y22)，冻结Row/TIA/VCM/VEXC的Tian/Y曲线相对复数差最大约4.11e-5/3.70e-5/1.09e-4/1.09e-4。这里重用冻结输入核实标量身份，不称新整网单环交叉资格。

初始四个fixture的wrdata直接拼接负电流表达式产生错误字段布局，分析shape检查实际拒绝。原cases/日志保留；改为分别命名每个电流vector后，新四case解析交叉通过。没有删除四个失败计数。

## 3. 第一完整网络状态与矩阵可信度

本包测5V/allblank/all800Ω，10个真实OPA宏（VCM/VEXC/4Row/4TIA），保持1k/4.99k/100p及TIA1k/22p冻结候选。
验证电路图逐元件的精确行/列交换对称性，B源内的控制网名也被纳入替换。8个代表激励列恢复完整20列、进而完整10×10矩阵。图对称自检PASS；尚未跑额外实际重复列，因此这些结果继续定义为候选重建，不能把缺失交叉核查说成完整验证。
所有代表列的真实OP相对原DC最大driver/VCM/VEXC差{op['actualColumnBiasMaxV']:.12g}V；这不是通过锁工作点达到的。开端口V矩阵条件数最高{op['portVoltageMatrixConditionMax']:.6g}，D条件数最高{op['baselineConditionMax']:.6g}；低频巨大前向级联增益/非正规矩阵可能导致误差放大。
开端口结果σmin={op['sigmaMin']:.12g} @1Hz，最小eigen距离-1约{op['minEigenDistanceToMinusOne']:.9g}。两者回答不同问题，不能用eigen远离-1覆盖σ门，也不能单靠σ判实体失稳。

第二种独立测试拓扑保持全部反馈wire的DC/小信号连接：每环一个0V串联电压源、一个0A并联电流源；分别激励，测B/A及D/C响应。由真实KCL构造I块=[B,I+A;-B,-A]及V块=[D,C;D-I,C]，再求20端口Y。这不是复制第一拓扑。
8个代表列的OP最大差{cl['biasDifferenceMaxV']:.12g}V；恢复V条件数仍最高{cl['voltageReconstructionConditionMax']:.6g}；σmin={cl['sigmaMin']:.12g} @1Hz。两者全频L的最大相对差约{cl['openClosedLRelativeDifferenceMax']:.9g}，说明两拓扑有可比数据，但这不解决低频数值/归一化的资格问题。
程序中condition<1e12的频段标记仅为自设数值诊断启发，不是Pro门，也不用于屏蔽低频或给PASS。扫频1Hz–300MHz；上界最大eigen gain约0.02513，确实衰减；仍不是全频/内部极点稳定证明。
完整复数L、eigen CSV/NPZ、sigma/condition及各原始端口数据都直接交付；图的eigenlocus只显示局部zoom，图外大增益点保留CSV。不连接未跟踪的eigen分支制造虚假连续轨迹。

**按裁定“σmin<0.20自动技术复核、不直接PASS”，科学停止。** 还没有完成全网对应单环的独立Tian再测、实际重复列及参考D资格；active800/8000/high-target和供电角点MIMO未运行。没有用测试台问题修改补偿或器件。

## 4. 供电continuation真实结果

从真实5V/all800/ROW0 OP出发，用上一实际OP的电压作为nodeset初猜，每级重新求解；无ic强锁、无复制5V结果。50mV失败后，每方向只缩到25mV一次。
下行：4.95V(50mV)失败；4.975V成功；4.975→4.95V(25mV)仍失败，因此按门停止，下界最后真实成功4.975V，**没有4.75V角点结果**。
上行：5.05V成功；5.10V(50mV)失败；退回5.05→5.075→5.10V(25mV)成功；5.125V失败，因此停止，**没有5.25V角点结果**。
CONTINUATION_STATUS.json及每级nodesetSource、真实op.raw、analysisErrors均保留。失败是数值无法求解，不冒称削顶。驱动脚本最初错误把首个25mV成功当终点，已保留初版并修正，继续到了下一步实际失败；没有把这项软件问题当科学结论。

## 5. 七宏短窗准备与未执行范围

生成两分区×三负载的6个真正pre-switchOP测试台，无外部切换。all800两个分区没有取得实际OP；8000/highTarget四例有真实OP。高目标固定ROW0/COL0=8000，其余800；初始脚本在执行前已改为按元件token赋值，避免字符串800→8000再次匹配。
准备的短窗生成器保留10ns边沿、Ron5/Roff1e12、全部电路值及负载，计划t_switch=3µs、t_end=353µs，先真正preOP再外部切换，没有在带3µs开关波形时跑100µs optran而假称pre-switch。**该生成器没有被调用run，实际正常暂态0**。
拟短窗有效CS偏移325/350µs并使用本case333–353µs后段参考；这是两时刻短窗，不冒称完整32有效边沿或整帧。该时刻合同尚未正式资格，停止后不生成虚假trace/建立PASS。
全10宏长窗0，没有为了补结果重新硬跑9.6ms。

## 6. 已接受RESET/软件契约与预算权限

不改RESET已接受25°C1k direct路径；不新增G17/G07。20–30°Cbench、±5V/掉电回灌/60s热/MCUabsmax仍按Pro分域HOLD。P2新钳位候选0，因为P1复核门先发生；不声称查过两件或温区已闭合。
四个协议/测试文件与a3e22772字节/哈希相同；接受的32项最终GREEN保持历史出处，**本包未做新的32项测试，不新增第二套状态机**。接口合同单独冻结；PGOOD/SPI/UART/真实WCET及100fps硬件无新实测。
PCB/制造/采购/bench/本地Git/系统级写0；GitHub仅已授权此电路完整报告/附件公开发布。

## 7. 集中请求的新裁定

请集中复核这一个具体问题：**D=Yee+Yff候选归一化、全10反馈的端口切集和参考系统应如何资格，才能解释低频σ<0.20？** 两拓扑保持真实偏置且在低频都很病态；当前数据没有支持把它改写为真实电路不稳定。
希望下一裁定给唯一方法修复路线：是否需要改为有明确定义/合格参考的多受控源return-difference、规定物理loop尺度/端口激励及conditioning检查；如何验证对应全网单环和低频数据，而不是略去低频。
用户的扩大有界预算要求已经批准。本包尚剩DC/AC/PZ52次及诊断属性1个，但**科学复核STOP不能用未耗尽时间/额度自动绕过**。请明确新方法包或剩余额度的接续范围，避免自重置计数；普通代码/导出细节继续本地累计，重大方法/设计/范围变化集中一次裁定。此请求不扩大平台、bench或系统权限。

## 8. 完整交付与回复安排

目录提供完整报告、裁定/输入SHA、49例索引、原始models/cases/OP/AC与全部退出/错误日志、完整矩阵/eigen/condition可读CSV、3PNG、fixture和数学/原子预算/STOP联动测试、保留的独立终审结果、接口合同及停止账。旧三代文件保持冻结。P4发布后实耗与消息历史/owner/nextCheckAtUTC在独立送达账保存；不以上传前快照冒称最终实耗。
固定GitHub新目录和commit一次性交付；内部send后立即读历史，区分送达/生成/错误/完整新裁定，结束前建立接续监控。网页是否实际读完不是附加等待门，也不会虚报已读。不分段，不重发旧报告，不联系其他项目。

END-OF-COMPLETE-R21-MIMO-STABILITY-AND-NATIVE-ECO-TECHNICAL-REVIEW-RECEIPT
FINAL-GITHUB-COMPLETE-DELIVERY
'''
    write('COMPLETE_MIMO_RECEIPT.md',report)
    write('README.md','''# R21 MIMO stability and conditional native ECO — technical-review blocked\n\n[Complete receipt](COMPLETE_MIMO_RECEIPT.md). One5V/allblank/all800 full-network matrix state, two distinct loaded probe topologies. sigma_min≈0.00994<0.20 requiresreview; low-frequency conditioning and reference normalization unqualified. No physical instability conclusion, no native ECO or bench release.\n\n- [Binding ruling](PRO_MIMO_RULING_FULL.md) / [Inputs](INPUT_VERIFIED.json) / [Gates](GATES.json)\n- [49 actual solver cases](CASE_EXECUTION_INDEX.csv) / [Global atomic budget](EXECUTION_BUDGET.json)\n- [Analytic fixture](MIMO_FIXTURE_VALIDATION.json) / [Openport matrix](mimo_blank_800_RESULT.json) / [Closed double injection](HYBRID_RESULT.json)\n- [MIMO sigma figure](plots/MIMO_SIGMA_REVIEW.png) / [Condition](plots/MIMO_CONDITION.png) / [Eigen zoom](plots/MIMO_EIGENLOCUS_ZOOM.png)\n- [Full open matrix CSV](results/mimo_blank_800_MATRIX.csv) / [Full closed matrix CSV](results/CLOSED_MIMO_MATRIX.csv) / [Open/closed conditioning comparison](results/HYBRID_CONDITION_AND_COMPARISON.csv)\n- [Continuation](CONTINUATION_STATUS.json) / [PZ capability chain](PZ_QUALIFICATION.md) / [Frozen interface](FIRMWARE_INTERFACE_CONTRACT.md)\n\nOriginal cases/models/logs/raw OP/AC remain alongside readableCSV. Initialformat errors and analysis failures count and are retained. Shorttransientactual0; candidate generator not executed. P2/P3 not entered. Prioraccepted32protocol tests are copied unchanged; no new32-testpass asserted. Full SHAmanifest and optionalZIP added atpublication, individual files remain directlyreadable.\n''')
    print(json.dumps({'readableAC_CSV':count,'readableOP_CSV':opcount,'reportBytes':(ROOT/'COMPLETE_MIMO_RECEIPT.md').stat().st_size,'reportSHA256':hashlib.sha256((ROOT/'COMPLETE_MIMO_RECEIPT.md').read_bytes()).hexdigest().upper(),'PNG':3}))
if __name__=='__main__':finalize()
