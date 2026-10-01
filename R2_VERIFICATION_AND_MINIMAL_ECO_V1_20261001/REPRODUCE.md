# 复现材料说明

本版为停止门回执，不授权自动继续模型/EDA。公开原始cases、manufacturer LIB、execution.json及stdout/stderr/原始trace，附同一官方便携archive。原case包含本机绝对.include路径，复现到新位置时仅替换模型根路径，另存派生case并记录旧/新SHA，不覆盖原证据。ngspice命令及cwd见每个execution.json；兼容-n -D ngbehavior=psa。提取archive的bin/docs/share/lib，避免示例Unicode文件名问题；程序未安装到系统。

readable CSV逐列保留原始文本值及单位名称，CURVE_SOURCE_INDEX.json关联原始SHA；PNG提供视觉摘要。coupled三次均无完整波形，只有失败日志，禁止用单TIA CSV替代耦合结果。原始模型和两个原厂来源包完整保留。原版R2工程/PDF在README固定历史commit入口，没有新原生输出。

下载diagnosis中的HTTP cookie/临时签名查询仅在公开副本去除，原始本地证据保留，PUBLIC_SOURCE_MAPPING.csv记两端SHA。原厂便携包为复现附件，正文和波形均有独立可读文件，不依赖压缩包或LFS。
