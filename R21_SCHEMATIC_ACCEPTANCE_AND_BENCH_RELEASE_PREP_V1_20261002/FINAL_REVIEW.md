# 单次fresh-context终审及文档收敛

Reviewer /root/bench_preparation_final_review，全程只读，无Git/EDA/仿真/联网/新协议/新实验/子agent。Critical0、Important2、Minor0。真实NOT_RELEASED准备包可在两项文档收敛后交付，不需要回修电路或工具。

Important1：TIMING_CAPTURE_PLAN.md:3把4×9×25us写1200us，漏写等待；原冻结合同实际300+900=1200，8状态9600+400。COMPLETE_BENCH_PREP_RECEIPT.md同样需要明确加法。Important2：基线文件只有epro2固定URL，强制companion/addendum/实际CSV未有可取得链接，README/receipt声称已有全部链接不符。补固定commit目录及逐文件链接即可；不要复制原生。

独立核对13/13基线SHA/bytes当前不变；被占用WORK.eprj2用共享只读流核SHA，未干预进程。CSV全部57×25、46×11与TABLE_INPUTS一致；所有工况未执行、空载16R为空非0Ω。32实际探点网络与accepted107CSV一致，46节点探点均实际成员；J3.5实际1k到PGOOD，不混旧候选。旧08三引用及源SHA正确；4.096仅内部参考启用。校准点非独立验证、每单元<=1%和sampleSD<=0.2%、guardband正确；数字硬门和实体输入null/PENDING_RELEASE。两PNG实际查看，可读，无需xlsx。

Declined：样机存在/正确装配、仪器能力、限流/硬停止安全数字、实际启动热故障精度时序、后续网络/send；这些不能由本包证明，也不构成返回EDA或工具研究的门。

Root仅一次文档修复pass：澄清300+900、补13固定基线文件URL；修复静态检查FINAL_REVIEW_DOCUMENT_FIX_CHECK.json，无新科学测试或第二轮review。
