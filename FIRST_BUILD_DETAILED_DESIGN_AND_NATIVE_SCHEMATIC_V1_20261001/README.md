# SCIENCE_ADK5556 4×4 DAQ — 完整审查交付包

本目录是用户要求的一次性 GitHub 交付：完整报告及所有附件。停止原13段传输；请以完整报告及附件为本次统一审查依据。

- [完整报告 PRO_FIRST_BUILD_RECEIPT.txt](PRO_FIRST_BUILD_RECEIPT.txt)：528962字符、578921字节；SHA256 `5C3160EAE2A2BD63F593A684584E3B46FDA7D12E451E30ABDCFF50824186B020`。
- [全部报告与附件 ZIP](COMPLETE_REPORT_AND_ATTACHMENTS.zip)：完整源目录187个文件，包括原厂资料、两套模型包、原生库、执行脚本、真实捕获及失败证据；[逐文件清单](ATTACHMENT_MANIFEST.json)。
- [可编辑原生工程](SCIENCE_ADK5556_4X4_FIRST_BUILD_V1.eprj2)：1486848字节；SHA256 `ED24205910B4CF5C52942DEDDFAA6F2146752A135204309E15A99A1E24C82D81`。
- [4页审查用PDF](FIRST_BUILD_REVIEW_ONLY.pdf)：376380字节；SHA256 `0DDA69D33D7E774A6B72FEAFEEE67D6364DD5E3D17099E21474F077D84212698`。

## 网页可读附件入口

[完整文件索引 EVIDENCE_INDEX.md](EVIDENCE_INDEX.md) 提供所有187个原始文件的直接链接、大小及SHA256，不仅提供ZIP。原厂PDF、模型、脚本、网表和原始JSON均作为普通Git文件公开，未使用Git LFS指针。

新增派生可读导出：

- [258连接引脚核对CSV](readable_evidence/COLD_REOPEN_PIN_CHECKS.csv)
- [63网络成员核对CSV](readable_evidence/COLD_REOPEN_NET_MEMBERS.csv)
- [全部286实体引脚CSV](readable_evidence/COLD_REOPEN_ALL_286_NATIVE_PINS.csv)
- [七核心型号功能针CSV](readable_evidence/SEVEN_CORE_LIBRARY_FUNCTION_PINS.csv)
- [七核心型号原生焊盘记录CSV](readable_evidence/SEVEN_CORE_PAD_RAW_RECORDS.csv)
- [187个原始文件哈希CSV](readable_evidence/SOURCE_FILE_HASHES.csv)

这些CSV均从已交付的JSON证据导出，没有新EDA或求解；原始证据和原哈希保留。

## 审查顺序

先读全文报告，再读详细设计、误差/校准/时序、验证报告、BOM/pin-net及保存重开真实审计；PDF和PNG用于图纸审阅，原生工程用于编辑和独立复核，ZIP提供所有原始证据。旧13段文件只作为送达历史保留在ZIP内，不是继续逐段发送的要求。

原始PACKAGE_HASHES.json中的167文件已全部核实一致；上传前另生成当前187文件的完整哈希清单。ZIP已逐成员解压核对大小、内容哈希和CRC。

## 已验证结果和限制

78器件、4页；保存冷重开真实258/258连接引脚、63网、28NC通过。原生工程可编辑；最初45/258错误及修复证据均保留。前后网表完整KV多重集合和网络成员一致，字节并不相等。

81组numpy线性DC、8自检和24静态定性故障分析；不是器件宏模型仿真。AC、正常暂态、故障暂态均0。每线0.1Ω的九模式残余最大0.0797833%，1Ω为0.791526%，超线阻预算，不是全域或实物保证。

状态保持：DYNAMIC_VALIDATION_HOLD / FAULT_PROTECTION_HOLD / REFERENCE_CAPACITANCE_HOLD / ERC_DETAIL_HOLD / DRAWING_LAYOUT_HOLD / BENCH_NOT_RELEASED。DRC只取得warn10 count，无正文；最终PDF仍有网名、针号重叠及左端口碰图框，绘图2/2预算耗尽。

两自有EDA会话已正常关闭。新项目1/session2/save5/完整连接审计3/实际nativeFile捕获3/DRC1/export2。未上电、未投板、未制造、未采购；无本地Git写或系统修改。GitHub上传是用户新授权的报告及附件交付，不是工程制造放行。

请对全文与附件给出完整统一新裁定：接受结果、唯一下一包、输入、交付物、继续/停止门及预算。不要将ACK或旧指令当成新预算。无法访问附件或完整读取时请明确具体缺口，不要声称已读全包。
