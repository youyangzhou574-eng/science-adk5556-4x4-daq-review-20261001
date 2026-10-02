# Historical metadata overrides

Actual case.cir and RUN.json take precedence over copied ASSUMPTIONS.json. No new scientific run is made here.

- row800_blank_to_enable was copied from row OP metadata: it really includes EN off at5.01us and on25.01us; blankIncluded is true, unlike its historical copied field.
- matrix800_selected_external_nodeset_op includes only external nodesets; they are not measured internal states or a model edit.
- matrix800_family_model_op changes all four TIA instances to unedited generic OPAx388; its historical copied OPA4388-description field is stale. OP aborted, no qualification.
- tia800_op_ac uses the original OPA4388 macro, input series voltage injection; ideal three unselected rows. It has OP and AC, not PZ.
- tia800_current_pz has OP plus aborted current-port PZ. poles.txt contains OP-vector output, not poles.
- tia_step_800_1000_7000_8000 uses a behavioral resistor driven by a voltage-only value control; source steps are not actual mechanically switched resistors, cable and ADC are equivalent models. OP and TRAN both counted.
- No case includes a REF3025 macro, full TMUX1109 leakage/charge/noise model, LP5912 macro, or actual MCU/firmware.
- run_one_screen.py is historical bounded execution code only; incomplete stall/cumulative-phase enforcement is disclosed, not a reusable qualified runner. Budget STOP is sticky and no subsequent SPICE launch is permitted.


## Final-review OP validity override
阶跃case的显式OP虽然生成文件，但 out=3.6923474469V、ain=3.8062722860V；100Ω串阻和1MΩ输入在DC应给 ain=out/1.0001≈3.691978249V，差约114.294mV，因此该OP不满足支路一致性，不能称有效DC解。次数照算，原证据保留。后续TRAN重新初始化，首点和末段单独解释，不因此重跑，也不把OP文件存在当PASS。
