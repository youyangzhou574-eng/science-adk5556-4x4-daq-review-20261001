# R2.1 实际模型验证与最小ECO候选：阻断回执

包：SCIENCE_ADK5556_4X4_R2_VERIFICATION_AND_MINIMAL_ECO_V1。

**本包取得了真实执行器与单环路/单TIA原厂模型结果，完成了八状态和接收端连续性测试；整板耦合暂态未闭合，复位完整保证仍有资料缺口，因此没有生成R2.1原生工程，不解除上电/制造禁门。**

## 裁定、冻结输入与范围

新裁定全文见PRO_R21_GATE_FULL.md，标记CIRCUIT-PRO-R2-REVIEW-AND-VERIFICATION-GATES-20261001-03，配对assistant消息1d942a5b-d99d-4dda-b739-0cd5196c20ec。收到后按用户连续普通技术授权直接执行，不索取模型/人工提交许可。

冻结R2 commit [da6ca87b9f49c5af03a16c24af6186d7c5c2e0d3](https://github.com/youyangzhou574-eng/science-adk5556-4x4-daq-review-20261001/tree/da6ca87b9f49c5af03a16c24af6186d7c5c2e0d3/FIRST_BUILD_ELECTRICAL_CLOSURE_AND_SCHEMATIC_R2_V1_20261001)。R2原生入包重新核验2052096bytes、SHA256 02729786CCDCABA10979A9BB36AAD86500D492E665905A62BA8DF789346B83AE，见P0_INPUT_VERIFIED.json。

固定4×4/8线、800–8000Ω、E=0.25V、Rf4990Ω、100完整帧/s、≤1%误差和≤0.2%帧间标准差目标没有降低。V1/R2未改；PCB、制造、采购、实物上电、本地Git写入、系统配置更改全部0。

## 实际执行器资格

官方ngspice47 Win64便携包，项目内解压调用，无安装器、提权、全局PATH或用户配置修改。官方入口先403，NetIX官方镜像成功下载同一包；13814879bytes，SHA256 59225971bd68cdd1199443649aa4615a9e6d684933f205ab49006a3942518f5a，与SourceForge公布值一致。

执行器自报ngspice-47、2026-08-11构建。ngspice_con.exe SHA256 22d5cae2bd32b2e39157a8d27bf457122f68285b72a9ebefdf41551b628233ab。Windows tar读取部分Unicode示例文件名报错（exit1）；已选择提取bin/docs/share/lib，实际exe与必需库通过RC/运放测试，未冒称全包提取exit0。

原OPA4388宏模型17385bytes、SHA256 958ff133418bd47522015057497858263e73b9e6d75860ef9c0b6fdabed5cd0d保留。无兼容模式运行失败，提示VSWITCH类型及TEMP参数；唯一兼容轮为文档规定的命令行`-n -D ngbehavior=psa`。没有改模型、更没有删除限流/钳位/动态环节。新增TI OPAx388原厂包及原LIB也保留，明确用于单/双核OPA388/OPA2388共同节点，资格响应已执行。

RC一阶1µs时间常数算例1619点，指定检查点对解析误差0.1842mV（门限1mV）；OPA4388跟随器2191点，10mV阶跃稳态误差1.62µV。输出有限、正常跟随、供电5V和五脚次序均核对，不只看退出码。P0在30min内完成，四个资格运行中包括一次原语法失败；后加OPAx388资格仍在P0起点30min窗口内。

## 两轮局部补偿与实际模型结果

基线小集合：带1k隔离、1nF共同负载的缓冲，返回比标称相位裕度约11.006°，不满足60°。原TIA返回比出现上下多交越及不可靠DC偏置，已标UNQUALIFIED_MULTICROSSING，没有把269°等简单数值当稳定保证。

第一轮候选：TIA输出→反相感测端100pF高频反馈；VCM/VEXC隔离后反馈增加4.99k感测返回、输出→感测100pF。行原有4.99k/100pF保留。第二轮候选只将TIA高频反馈从100pF改22pF；不改Rf4990/Cf2.2nF/输出1k/列感测10k/ADC100Ω与10nF。

`optran`2ms工作点准备按ngspice手册执行，原默认偏置结果和日志保留，不覆盖成成功。AC使用1Hz–100MHz、100点/十倍频；报告所有单位增益交越和负实轴交越。部分没有负实轴交越，只表示所扫频带未找到，不能声称全频无限GM或把GM≥10dB当完整角点PASS。

详尽返回比数据见results/LOOP_METRICS.json。单环路方法是高输入阻抗处串联电压注入，L=−V(fb)/V(minus)，其他源AC0；尚未做独立注入方法交叉验证。即使数值超过60°，仍不能替代耦合多环路证明。四行/四TIA是对称等效小集合，未声称十个实体环路及全部角点已穷尽。

单TIA第一轮：可用首个有效边沿残余约103.34µV，超过100µV；第二轮22pF、完整1200µs活动状态的32个有效采样边沿，最大模型残余约0.03µV（受输出文本精度限制），通过这个**单TIA、理想VCM、4×800Ω等效负载**的边沿筛查。稳态目标取后段原始波形，不是理想值或另一次校准。没有把模型小数位数写成实物分辨率。

## 整板耦合阻断

测试台包含4行+4TIA原OPA4388模型、VCM/VEXC OPAx388原厂模型、所有输出1k隔离、补偿支路、16×800Ω、ROW/COL各1nF、ADC100Ω/10nF/1MΩ及八状态。TMUX以5Ω/1e12Ω开关近似，参考源/电源理想化，外部BAT/真实参考启动与电源热故障未覆盖，不能称全板所有物理行为模型。

两次2ms工作点准备分别触及48s运行封顶，没有完整波形。第三次使用默认DC初始化，工作点完成但暂态在约12.8–13.5µs处以极小步长推进；运行约11.95min仍远未达9.6ms。核对PID54804、绝对exe路径和启动时间后结束仅本包自建进程，日志完整保存。该次是FORCED_STOP_NOT_NORMAL_EXIT，不能写正常退出或“没有仿真”。内部10min观察闹钟超过约1.95min，如实披露，未冒称该内部时限严格通过；官方P2≤90min没有耗尽。

本轮尚不能区分耦合物理不稳定、模型行为分段导致的收敛困难和初始化问题。不能用Gear数值阻尼、删除模型环节或新执行器偷偷把缺口标PASS。两轮补偿预算已用完，耦合标称建立结果仍不可判定，触发停止推进；P3禁门保持。

## 软件、协议与复位

八状态实际事件表288传输/32dummy/256有效样本；每行使用相邻blank，差分代码已执行。21测试通过：连续两帧、10s间隔、跳号、重复、uint32回绕、旧epoch、旧采集、迟到、缺样、错标签、无新数据失效、持续心跳但数据过期、过期后两帧恢复、事件计数、独立原厂位序字面向量、差分计算。最终审查另发现失效清理丢失防重放水位；新增5项回归测试先实际失败，再将同epoch已收帧号/采集时间水位与连续资格分离，并加入跨失效/复位保留的有限单调接收时钟。过期旧帧重放、重复帧重播、倒退时钟、非有限时钟和新epoch时钟倒退均被拒绝，最终21/21通过。RED日志、修复后日志及FINAL_REVIEW.md保留。

选择SPI mode1 falling-edge捕获上一稳定SDO位，16th edge推出B15、17th edge采B15；与表13/14及TI原厂说明对应。离线字面向量独立于编码器。硬件SPI/示波器/ADC mux建立、WCET与噪声仍HOLD。

9600µs采集+400µs余量，额外开销候选354µs、余46µs；DMA服务要放在25µs转换周期已有空档内。不是实测固件100fps证据。

帧采集间隔9.75–10.25ms，接收延迟≤0.5ms，严格连续帧号及epoch；独立tick，心跳4.5ms超时，采集年龄10.25ms撤销资格。正常恢复要两帧。≤10ms实体故障延迟候选分配9.75ms尚未验证；持续心跳但完整帧缺失的数据年龄失效路径本身可超过10ms，明确FAULT_LATENCY_CONTRACT_HOLD。

复位候选不把原4.99k/10k分压原样搬到MR：采用独立Schmitt请求及板内开漏驱动PGOOD的等效方案，保留电源监控器。32解析角点得到请求低最大0.555017V、断开高最小2.82765V、板内下拉负荷上界0.53764mA、NRST最低低门限0.9195V。原架构1.098532V分压冲突被候选连接消除，尚未落实原生。Schmitt全区间门限包络、开漏释放漏电分配和连续负故障热行为没有闭合，完整复位保证为HOLD。详见RESET_AND_TIMING_CONTRACT.md及RESET_CORNERS.json。

## 容量、故障、误差与未执行项

准确型号Murata接口未返回曲线，44µF保留系数0.29709/0.59418只是需求；无盲目加倍。拓扑故障路径及轨吸收耗散已整理，但未跑故障宏模型/60s热试验，不伪装成保护PASS。

统一电导误差索引见UNIFIED_ERROR_BUDGET.csv：冻结固定校准线阻/接触有限域结果、固定INL从电阻误差换成电导界、两个状态各100µV残余的差分界、偏置/激励/参考/增益漂移及噪声另列。缺少完整耦合及保证温度/容量/噪声条件，不给出全域≤1%或≤0.2%通过。

P3全0：没有新原生/R2.1BOM、连接差异的实际实现或冷重开、没有新ERC/PDF。冻结R2 warn1168仍无正文；四个C_ADC Value/制造商编码和旧图面问题不因本次软件/单环路PASS自动解除。

## 实耗、收尾与一次性交付

实耗上限账见EXECUTION_BUDGET.json与CASE_EXECUTION_INDEX.csv：便携包1、资格4、兼容1、设计修订2、AC11、显式宏模型DC8、解析复位DC32（DC合计40≤64）、正常暂态10（含资格、原失败及三个耦合未完成）、新增原厂模型包1、两种复位解析应力；原生库/会话/保存/File/审计/ERC/PDF0。源码/日志/原始数据与失败证据均保留。

本包单环路真实输出已建立，但整板动态门没有通过；停止本轮原生推进，等待统一处理耦合收敛/验证方法、复位门限和≤10ms完整缺帧路径的新裁定。不要重启R2/V1或分段正文。GitHub使用同一专用公开仓库的新目录及固定commit、可读MD/CSV/PNG/TXT与模型/原始数据附件。网页端实际读完不冒称已验证。

最终复查和软件修复不新增模型/设计修订/原生次数。预算字段已明确limit，上限不冒称实耗；正式P2进入至科学收尾约8.39min，停止进程后的分析归档包含其中。发布文件的来源/SHA和敏感下载头脱敏映射见MANIFEST.csv、PUBLIC_SOURCE_MAPPING.csv、PUBLIC_PREPARATION.json。

全部既有DYNAMIC_VALIDATION_HOLD、FAULT_PROTECTION_HOLD、REFERENCE_CAPACITANCE_HOLD、ERC_DETAIL_HOLD、DRAWING_LAYOUT_HOLD、BENCH_NOT_RELEASED保留。本包额外RESET_THRESHOLD_ENVELOPE_HOLD、FAULT_LATENCY_CONTRACT_HOLD、COUPLED_MODEL_CONVERGENCE_HOLD明确记录。

END-OF-COMPLETE-R21-VERIFICATION-AND-MINIMAL-ECO-BLOCKED-RECEIPT
