from pathlib import Path
import os,json,csv,hashlib,numpy as np
R=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']=str(R/'plots/.mplconfig')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from network_cases import raw_nodes

case=[];acCount=opCount=0
b=json.loads((R/'EXECUTION_BUDGET.json').read_text())
for c in b['cases']:
 p=R/'results'/c['name'];s=json.loads((p/'STATUS.json').read_text());row={'case':c['name'],'kind':c['kind'],'OP':c['commands'].count('op'),'AC':c['commands'].count('ac'),'OPTRAN_init':c['commands'].count('optran'),'TRAN':c['commands'].count('tran'),'processStatus':s['status'],'analysisStatus':s['analysisStatus'],'wallSeconds':s['wallSeconds']};case.append(row)
 if s['analysisStatus']=='ANALYSIS_ERROR':continue
 if(p/'data.txt').exists():
  a=np.loadtxt(p/'data.txt',skiprows=1);fields=(p/'data.txt').read_text().splitlines()[0].split();assert len(fields)==a.shape[1];np.savetxt(p/'data.csv',a,delimiter=',',header=','.join(fields),comments='');acCount+=1
 if(p/'op.raw').exists():
  nodes=raw_nodes(p/'op.raw');assert all(np.isfinite(v)for v in nodes.values())
  with(p/'op.csv').open('w',newline='')as f:w=csv.writer(f);w.writerow(['node','voltage_V']);w.writerows(sorted(nodes.items()))
  opCount+=1
with(R/'CASE_EXECUTION_INDEX.csv').open('w',newline='')as f:w=csv.DictWriter(f,fieldnames=list(case[0]));w.writeheader();w.writerows(case)
arrays=np.load(R/'results/NEW_GC.npz');freq=arrays['freq']
for key in ['openGc','closedGc']:
 a=arrays[key];np.savetxt(R/'results'/(key+'_MATRIX.csv'),np.column_stack([freq,a.real.reshape(len(freq),100),a.imag.reshape(len(freq),100)]),delimiter=',',header='frequency_Hz,'+','.join([part+str(i)+'_'+str(j)for part in['real_','imag_']for i in range(10)for j in range(10)]),comments='')
fig,ax=plt.subplots(figsize=(10,5),constrained_layout=True)
for key in ['openGc','closedGc']:ax.loglog(freq,np.linalg.cond(arrays[key]),label=key)
ax.axhline(1/np.finfo(float).eps,color='red',ls=':',label='1 / double epsilon (diagnostic)');ax.grid(True,which='both',alpha=.25);ax.set_xlabel('Frequency (Hz)');ax.set_ylabel('Condition number of Gc');ax.set_title('All20 columns measured: low-frequency numerical qualification HOLD');ax.legend();fig.savefig(R/'plots/GC_CONDITION_ALL_FREQUENCIES.png',dpi=180);plt.close(fig)
fig,axes=plt.subplots(2,2,figsize=(11,7),constrained_layout=True)
for target,ax in zip([0,1,2,6],axes.flat):
 a=np.loadtxt(R/'results'/f'FULL_TIAN_SCHUR_{target}.csv',delimiter=',',skiprows=1);f=a[:,0];d=a[:,1]+1j*a[:,2];s=a[:,3]+1j*a[:,4];ax.semilogx(f,20*np.log10(abs(d)),label='Direct loaded2port'if target==6 else'Direct series/shunt');ax.semilogx(f,20*np.log10(abs(s)),'--',label='Full matrix Schur');ax.axhline(0,color='gray',lw=.7);ax.set_title(['VCM','VEXC','ROW0','TIA0 (direct Tian HOLD)'][[0,1,2,6].index(target)]);ax.set_xlabel('Frequency (Hz)');ax.set_ylabel('Return ratio (dB)');ax.grid(True,alpha=.2);ax.legend(fontsize=8)
fig.savefig(R/'plots/SCALAR_CROSSCHECK_SCOPES.png',dpi=180);plt.close(fig)
proxy=np.genfromtxt(R/'results/DETERMINANT_FINITE_AXIS_PROXY.csv',delimiter=',',names=True,dtype=None,encoding=None);fig,ax=plt.subplots(figsize=(10,5),constrained_layout=True)
for label in ['openGc','closedGc']:
 a=proxy[(proxy['topology']==label)&(proxy['scaleIndex']==0)];ax.semilogx(a['Hz'],np.unwrap(np.angle(a['detPhaseReal']+1j*a['detPhaseImag'])),label=label)
ax.set_xlabel('Frequency (Hz)');ax.set_ylabel('det(Gc) / det(G0) phase (rad)');ax.set_title('Finite imaginary-axis diagnostic only; no certified RHP contour');ax.grid(True,alpha=.2);ax.legend();fig.savefig(R/'plots/FINITE_AXIS_PROXY_NOT_CERTIFICATE.png',dpi=180);plt.close(fig)
report='''# SCIENCE_ADK5556_4X4_R21_INVARIANT_MIMO_AND_NATIVE_ECO_FINALIZATION_V1 — 完整方法资格阻断回执

绑定06号：CIRCUIT-PRO-R21-MIMO-TECHNICAL-REVIEW-ACCEPT-INVARIANT-CLOSURE-20261001-06；assistant7e05b904-60de-4d53-a3d9-f3ec26c24be7；全文PRO_INVARIANT_RULING_FULL.md。旧四代commit冻结da6ca87b9f49c5af03a16c24af6186d7c5c2e0d3 / c13555a330f8ad676750b8fec5d5d42bfc0b5edb / a3e22772f368322dd9de671ab816c09e3b7f1b72 / d152e092101188e6dc57f620f81d52f2e243fb01。

**结果是方法资格HOLD，不是实体失稳，也不是原生或bench放行。** 旧D=Yee+Yff及sigma0.20硬门已正式退出；旧sigma=.00994保留其原范围。不因旧剩余52额度自行解锁；本06号包单独360min/160分析/24诊断重新授权。

## 本包实做与预算

实际52个ngspice进程；逐.control预扣52OP+52AC=104/160。包括4个进程正常退出但分析失败，不能把exit0称分析成功。48例有真实OP/AC数据。诊断9/24：4个真实求解诊断（2次固定DC optran初值、2次TIA不同加载端口），5次离线数值重放（初始Gc、两次旧矩阵重放含JSON导出失败重算、一次临时代理计算及一次可重现代理导出）。初版诊断账6，完整封装对账后补列前两项+可重现重执行1到9；旧账含UTC/历史保留，不称原始计数无误。

正常切换/资格暂态0/48；另2条optran 100us是固定外部状态的DC初始化诊断，不称完全没有任何内部暂态算法。完整10宏长诊断0/1；新reset/protocol/sources/candidate/library0；P2/P3全部0，旧原生不打开不改。普通主线AC资格不是求解器诊断变体，104条分析全计；没有把失败移出额度。源件/执行器SHA冻结；未安装执行器或第三方。

science.py保留实际指令原子预扣及sticky科学STOP，旧init禁用。新包不继承旧sigma.20停止逻辑。到达本包方法资格门后停止所有新SPICE；之后只有可读证据整理/离线代理存证及计数对账，没有新求解。

## 数学方法及三个已知真值fixture

统一10个反相求和点e/f；只有宏模型反相输入引脚移至e，外部4.99k/100p与Rsense/Rf/Cf/22p仍在f网络，输出1k隔离未切。对每对用vc=(ve+vf)/2、vd=ve-vf、ic=ie+if、id=(ie-if)/2，直接实现功率共轭变换。闭合约束vd=0、ic=0，Gc=Ycc=四原Y块之和；这是完整端口特征对象，但不自动提供参考或内部极点证书。

实现QZ/homogeneous generalized eigenvalue、不直接inv(G0)@Gc；LU/logdet、backward residual、condGc/G0及pencilSensitivityProxy。该proxy只是left/right耦合敏感性诊断，不冒称完整规范化generalized eigen condition估计。实际物理尺度Sv=Si=I事先冻结；10^-3..10^3固定混合尺度仅资格测试，不依频率或状态调指标。

三个独立state-space真值：2×2不对称非正规稳定（-2±j）、2×2闭环RHP（-1±sqrt8，其中一个RHP）、3×3不对称上三角稳定（-1/-3/-7）。A与diag(A)不交换。参考对角局部极点已知全负；完整闭合右半平面轮廓（下降imaginary轴并沿RHP大圆弧返回）QZ/LU计算在三组固定尺度下绕数0/1/0，与独立state-space真值一致。解析fixture资格PASS，不转成原厂宏网络PASS。

基础功率/closure/稳定和RHP/固定尺度测试先RED后GREEN；最终4项含证据来源防误报回归GREEN。首次资格导出JSON complex错误未丢数据，修序列化后再次离线重放并计账；不是物理失败。

## 实际重复列失败及强制全列回退

初8代表列的真实ROW0/ROW1电压与电流重复差8.8303%/8.7994%，超0.5%；TIA0/1约1e-14相符。没有用图对称证据覆盖真实失败。按06号直接放弃重建，补测open缺12列、closed缺8列，现在两拓扑各20列全部真实实测。ACTUAL_REPEATED_COLUMNS_AFTER_FULL_FALLBACK.json保留的是初始对称诊断，不表示最终20列仍用恢复值。

所有实际AC覆盖0.01Hz–300MHz，未删0.01/0.1/1/10Hz。两新Y完整实测矩阵、原始电流/电压/OP/退出日志均保留。两个拓扑的Gc在低频复数矩阵相对范数差约2.91e-6（约0.000291%），高频约1.12e-11；比第一版混合重建更一致，但不能独立证明物理稳定。

## 全网单环Schur交叉范围

另9反馈闭合的真正全网串联电压/并联电流双注入：VCM约7.97185MHz/93.9170°，VEXC约6.04404MHz/90.0589°，ROW0约5.52666MHz/98.6568°。三者与完整20端口的Schur消元fc/PM误差远小于10%/5°，接受为有限主交越交叉；低频Schur矩阵病态警告保留，不将小backward residual当作全频前向精度证明。

TIA0串联/并联两例OP/AC失败；一次定义明确的100us optran初始化两例也失败，4个失败全部计账。没有随机节点排序大搜索。另一保持DC的电感/有限电容加载双端口两例成功，得到约6.66567MHz/101.3152°，与完整矩阵Schur交叉一致。**这仅是LOADED_2PORT_VS_SCHUR_ONLY，不写成串联/并联TIA资格通过。** 独立终审发现target6旧JSON只有PASS:true容易误读，唯一修复轮加入方法/case来源/directSeriesShuntQualified:false及范围状态，先RED后GREEN；总FULL_NETWORK_PORT_CUT门仍PARTIAL。

## 低频尺度资格与Nyquist证书缺口

Gc在0.01Hz两拓扑cond约6.66e18/6.55e18，1Hz约1.62e17。QZ backward residual虽小，广义eigen集合对固定功率共轭尺度的相对差在0.01Hz约0.33、1Hz约1.01；高频则接近一致。这是双精度前向谱/方法资格问题，**没有观察到一个已资格的稳定/不稳定分类因尺度改变**，不能虚称电路失稳。

LU determinant的有限imaginary-axis代理绕数三组尺度/两拓扑均数值≈0，最大相邻相位步约0.12rad。determinant_proxy.py、DETERMINANT_PROXY_SUMMARY.json与CSV提供完整可重现定义：测得正频率到0.01、用共轭负频率、以显式线段连接低频gap与高频端点。**这些连接不是测得或解析证明的真实RHP轮廓/无穷远弧。** 参考G0=diag(Gc)的RHP零/内部极点资格也未完成；代理0不能变成MIMO_GENERALIZED_NYQUIST_PASS。

没有删低频，没有调频率相关物理尺度抬sigma，也没有对假定稳定G0发PASS。当前LOW_FREQUENCY_NUMERICAL_HOLD及REFERENCE_SYSTEM_QUALIFICATION_HOLD保留。

## N=1对象必须分域的数学事实

当N=1，指定G0=diag(Gc)=Gc，耦合R恒等1，R-I=0，不可能自身保留非零Tian fc/PM。简单解析L=100/(s+1)的局部闭环稳定，而Tian仍有有限fc；Gc=2(1+L)，耦合比仍1。若局部L=-2/(s+1)，Gc的闭合零在+1rad/s，但同样R=1；此时G0不稳定，应拒绝参考资格，不能因ratio=1称稳定。

这不是证明整个方法无效：耦合R可以描述**先已资格稳定局部参考之后**的环间变化。但它与物理单环返回比是不同对象。N1_OBJECT_CONTRACT_PROOF.json明确这一点。本地计划解释N=1/Tian资格针对二端口/Schur返回比，耦合不变量针对环间作用；此分域需本次集中新裁定接受，仍不补足G0证书。

## STOP与未执行范围

停止是INVARIANT_MIMO_METHOD_QUALIFICATION_HOLD：固定尺度下低频广义轨迹未资格、参考G0及真实RHP轮廓证书缺失，并且直接串联/并联TIA尚未资格。不是sigma.20（已取消），不是预算耗尽，不是实体增长振荡/削顶。独立终审认定证据足以支持方法资格HOLD；没有把数值谱变化称真正稳定分类变化。

P1其他负载/供电及六七宏353us切换因方法进入门未过而0；P2新的温区器件/protocol0，维持已接受25°C scoped RESET和旧32GREEN软件合同。P3全部0，旧ERC/图面/故障/温区/bench及供电HOLD保持。没有第三轮补偿/换OPA或ADC/改E/Rf/fps。

## 集中申请唯一后续路线及更大有界预算

请明确：接受N=1两个对象分域后，如何对diag(Gc)提供独立、物理稳定局部参考/RHP零与内部极点证据；如何处理未资格低频QZ前向谱敏感性，以及真实DC gap/RHP弧，才能避免把有限det代理0误读为稳定证书。TIA加载二端口/Schur可以接受到什么切口资格范围，仍缺串联/并联路径是否必须继续修复。不要用假稳定参考或删低频打开原生门。

**扩大执行预算是用户明确提出的要求，仅随这一次正常完整报告集中申请。** 建议唯一下一方法与条件原生包480min：参考/数值资格90、完整MIMO120、七宏动态100、RESET/接口40、条件原生100、交付30；实际OP/AC/PZ≤192、数值诊断≤32、正常暂态≤64、完整10宏附加长诊断1≤8min、RESET96/协议48/原厂资料8/候选2，原生副本1/session2/save8/captureaudit4/ERC2/PDF2保持。额度用于有边界的参考验证、独立交叉/数值资格与后续条件ECO，不扩平台额度，不安装新工具/模型或扩大PCB/制造/bench/本地Git/系统权限。普通实现与有限retry本地累计，重大方法/硬门/范围变化仍集中裁定。本包剩余56分析/15诊断不是续跑许可，旧包关闭，未批不复位STOP。

## 交付与通信生命周期

全文、固定裁定/输入/原模型、全部52case及退出失败/真实端口OP/AC、96逐case可读CSV、完整新矩阵/低频/QZ/尺度/代理/交叉/fixture CSV与3PNG、源算法/独立终审/RED-GREEN/计数修正一起独立新目录公开上传。ZIP只是额外汇总，原文件逐一直接上传，manifest对应SHA。

一次性短摘要+固定commit提交配对对话；立即fresh read确认完整user正文，区分生成/报错/完整裁定，不盲目重发旧缓存；同回合建立有效后继监控、owner/nextCheckAtUTC。网页实际读取不是额外等待门，不虚报已读。P4最终实际墙钟/消息和monitor状态保存在独立送达账，不篡改已发布预算快照。全部旧文件冻结、无他项目数据/实际凭据。

END-OF-COMPLETE-R21-INVARIANT-MIMO-METHOD-QUALIFICATION-BLOCKED-RECEIPT
FINAL-GITHUB-COMPLETE-DELIVERY
'''
(R/'COMPLETE_INVARIANT_RECEIPT.md').write_text(report,encoding='utf-8')
(R/'README.md').write_text('''# R21 invariant MIMO — method qualification HOLD

[Complete Chinese receipt](COMPLETE_INVARIANT_RECEIPT.md) · [Ruling](PRO_INVARIANT_RULING_FULL.md) · [Budget](EXECUTION_BUDGET.json) · [Gates](GATES.json)

52 actual SPICE processes /104 OP+AC analyses;9 numerical diagnostics incl5 offline; normal switchingtransient0, two optran DCinitialization cases, native0. Method/HOLD; no physical instability or stable verdict.

- [All cases and failed analyses](CASE_EXECUTION_INDEX.csv), original cases/results/models alongside96 percase readableCSV.
- [Three analytical fixtures](FIXTURE_QUALIFICATION.json), [N1 object scope proof](N1_OBJECT_CONTRACT_PROOF.json).
- [Initial repeatedcolumn fail](ACTUAL_REPEATED_COLUMNS.json), [Full actual-column fallback scope](EXTENDED_MEASUREMENT_PLAN.json).
- [Open Gc CSV](results/openGc_MATRIX.csv), [Closed Gc CSV](results/closedGc_MATRIX.csv), [Lowfreq/QZ/fixedscales](LOW_FREQUENCY_QZ_AND_SCALING.json).
- [Fullnetwork scalarcrosscheck scoped sources](FULL_NETWORK_SCHUR_TIAN_CROSSCHECK.json): TIA loaded2port PASS does not certify failed direct series/shunt Tian.
- [Finite-axis determinant proxy](DETERMINANT_PROXY_SUMMARY.json), [all proxy curves CSV](results/DETERMINANT_FINITE_AXIS_PROXY.csv): zero proxy is not a certified fullRHP contour.
- [Condition plot](plots/GC_CONDITION_ALL_FREQUENCIES.png), [Scalar scope plot](plots/SCALAR_CROSSCHECK_SCOPES.png), [Proxy phase plot](plots/FINITE_AXIS_PROXY_NOT_CERTIFICATE.png).

Reference G0/internal poles/true RHP contour and low-frequency forward spectrum unqualified; no native or bench release. Source SHAmanifest and ZIP added at publication; individual evidence files remain readable.
''',encoding='utf-8')
print(json.dumps({'AC_CSV':acCount,'OP_CSV':opCount,'actualProcesses':len(case),'reportBytes':(R/'COMPLETE_INVARIANT_RECEIPT.md').stat().st_size,'reportSHA256':hashlib.sha256((R/'COMPLETE_INVARIANT_RECEIPT.md').read_bytes()).hexdigest().upper()}))
