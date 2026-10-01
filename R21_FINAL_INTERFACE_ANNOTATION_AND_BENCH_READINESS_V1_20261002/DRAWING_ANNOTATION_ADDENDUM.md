# R2.1图纸备注校正表

六页仍继承R2标题和几处旧说明；09的两次尝试未改变备注；10仅一次官方Text.modify(value)分组尝试加save返回true，实际source/PDF仍未变。没有继续研究API或重试。LEGACY_ANNOTATION_HOLD。实际器件/网络以冷重开File、514针CSV/BOM为准。PDF必须连同此补充使用，不作制造/上电依据。

| 页 | R2.1正确说明 |
|---|---|
| 1 | VCM/VEXC各1k隔离、4.99k反馈、100p；U3.2=VCM_FB、U3.6=VEXC_FB。1–7k正常/0.8–8k保护带。 |
| 2 | ROW1k/4.99k/100p；旧ideal300us筛查不代表实体动态PASS。 |
| 3 | 四新22p：TIA_DRV_i↔COL_SENSE_i；10k感测/1ktap/Rf4.99k/Cf2.2nF保持；四C_ADC实际10nF X7R。 |
| 4 | REFIO/REFCAP独立HF/bulk；偏压有效容量/启动/噪声待bench。 |
| 5 | J3.5 NRST实际0603WAF1001T5E/1k；SWD/UART等仍4.99k。“all4.99k”旧泛化句不适用NRST。OD/OC、VOL<=0.4V、释放HiZ。 |
| 6 | 保护/supervisor继承；热/故障/全温区未验证。 |

8状态BLANK0/ROW0..BLANK3/ROW3，9.6ms+0.4ms，288传输/32dummy/256有效。epoch/replay/progress watchdog/两完整好帧恢复继承离线合同；真实100fps/WCET/精度/300us均BENCH_PENDING。

## 本次10的接口修正与PDF缺字

J3.1/R_J3_1.1实际为V3V3_EXT_SWD；J4.1/R_J4_1.1实际为V3V3_EXT_UART；两电阻pin2仍V3V3，各4.99k，外侧不共网。四新端口在最终PDF页5只显示空箭头，网名没有打印。INTERFACE_NET_LABEL_DRAWING_HOLD保留，不能称独立PDF完整终版。必须同时读取INTERFACE_TOPOLOGY_COMPANION.md/PNG/CSV及最终实际514针CSV。原生/File连接通过不等于图面文字修复。

J3.1/J4.1只作电压sense，不作供电输入；保留4.99k SWD信号串阻，后续明确获准的台架从约100kHz开始。正常1–7k、0.8–8k保护带；约10%变化验证基点不得使终点超正常域。所有300us、100fps、WCET、容量与故障指标均待实体证据。
