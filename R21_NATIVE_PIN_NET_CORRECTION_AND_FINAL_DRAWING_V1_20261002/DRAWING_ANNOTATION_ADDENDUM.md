# R2.1图纸备注校正表

六页仍继承R2标题和几处旧说明；两次Text.modify(content)返回saved true但实际source/PDF未变。LEGACY_ANNOTATION_HOLD。实际器件/网络以冷重开File、514针CSV/BOM为准。PDF必须连同此补充使用，不作制造/上电依据。

| 页 | R2.1正确说明 |
|---|---|
| 1 | VCM/VEXC各1k隔离、4.99k反馈、100p；U3.2=VCM_FB、U3.6=VEXC_FB。1–7k正常/0.8–8k保护带。 |
| 2 | ROW1k/4.99k/100p；旧ideal300us筛查不代表实体动态PASS。 |
| 3 | 四新22p：TIA_DRV_i↔COL_SENSE_i；10k感测/1ktap/Rf4.99k/Cf2.2nF保持；四C_ADC实际10nF X7R。 |
| 4 | REFIO/REFCAP独立HF/bulk；偏压有效容量/启动/噪声待bench。 |
| 5 | J3.5 NRST实际0603WAF1001T5E/1k；SWD/UART等仍4.99k。“all4.99k”旧泛化句不适用NRST。OD/OC、VOL<=0.4V、释放HiZ。 |
| 6 | 保护/supervisor继承；热/故障/全温区未验证。 |

8状态BLANK0/ROW0..BLANK3/ROW3，9.6ms+0.4ms，288传输/32dummy/256有效。epoch/replay/progress watchdog/两完整好帧恢复继承离线合同；真实100fps/WCET/精度/300us均BENCH_PENDING。
