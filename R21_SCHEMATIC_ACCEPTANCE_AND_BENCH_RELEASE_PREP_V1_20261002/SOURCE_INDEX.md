# 既有证据来源

1. 11号完整裁定PRO_ACCEPTANCE_RULING_FULL.md：工程接受、240min、所有native/simulation/bench0、下一次Phase1集中release。
2. 固定基线commit fbb7c0ed5f322f078583fadbdb353efe835e4c01：actual107成员/176BOM/514针/cold/companion/addendum。ACCEPTED_BASELINE_SHA.json记录原文件SHA，引用不复制原生。
3. 08包DC_ENGINEERING_40_GROUPS.csv /DC_ENGINEERING_SUMMARY.json：旧40组理想DC、仅等效输入；本包EXISTING_IDEAL_DC_REFERENCE.json引用3组，不新算。温区、线阻、宏动态、器件实际饱和未由此证明。
4. 既有FIRST_BUILD sources/ADS8684.pdf.txt Section8.3.9、pinout：REFSEL低/内部4.096V、REFIO/REFCAP；并非REF3025的2.5V。本包只读厂家已存文本，不新下载。
5. 旧R2_VERIFICATION RESET_AND_TIMING_CONTRACT.md八状态/48clk/25us段，仅时间合同；旧复位候选已不适用当前J3.5实际1k直接PGOOD。当前reset接线只以已接受actualnet为准。

Pro已说明复看材料；这里只记录其声明，不冒称网页端逐个附件字节全读。新包只读证据，不开EDA/仿真/测试，不改变旧SHA。
