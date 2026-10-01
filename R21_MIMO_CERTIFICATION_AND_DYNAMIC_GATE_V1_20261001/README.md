# Circuit R21 MIMO certification reference HOLD

完整结论：[COMPLETE_CERTIFICATION_RECEIPT.md](COMPLETE_CERTIFICATION_RECEIPT.md)。本次没有新SPICE/动态/原生，只离线资格证据。

- [新裁定全文](PRO_CERTIFICATION_RULING_FULL.md)，[输入与SHA](INPUT_VERIFIED.json)，[执行账](EXECUTION_BUDGET.json)，[门](GATES.json)。
- [块参考两拓扑/三尺度](BLOCK_REFERENCE_CANDIDATES.json)，results/含六个完整839点矩阵谱CSV和四个全谱匹配CSV。
- [已知block状态空间真值](KNOWN_BLOCK_REALIZATION_FIXTURES.json)，[参考零点反例](REFERENCE_ZERO_COUNTEREXAMPLE.json)，[隐藏内部模态反例](HIDDEN_INTERNAL_MODE_COUNTEREXAMPLE.json)。反例是数学域，不指称实际器件内部失稳。
- [精确频点覆盖](EXACT_FREQUENCY_COVERAGE.json)，两首次失败日志位于evidence/，完整冻结输入inputs/NEW_GC.npz。
- test_certificate.py/certificate_contract.py/diagnose_blocks.py可审计；不自行重新运行diagnostic以绕过sticky STOP或计数。

不得以代理0圈、单环有限PM或端口拟合pole宣称实际内部稳定；不能将loaded TIA通过变成direct通过。所有科学STOP/bench/旧HOLD保留。
