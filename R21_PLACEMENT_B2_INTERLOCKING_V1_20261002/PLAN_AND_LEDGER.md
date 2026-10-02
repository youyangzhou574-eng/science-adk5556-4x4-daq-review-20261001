# B2唯一离线咬合式方案

规格：PRO_B2_RULING_FULL.md，180min，3轮布局/2图，CAD/API/GUI0。完整读取636d471a回复后执行，不借旧23额度。

步骤：冻结现有body/pad/完整membership→先刚体骨架→普通件有限候选4旋转填缝→全不同器件body/pad proxy与关键距离、FFC2D检查→2张可读图→一次whole-package终审→固定GitHub交付和接续回复监控。

Ruling: 原文13.2mm是nominal而非公差最大，沿用已有13.4mm保守宽度及5.8mm规划包络；仍标exact actuator HOLD，新回复已明确该HOLD不阻止离线排布。代价：最终实体机械仍须后续确认，不能声称厂家扫掠资格。

Ruling: 全physical检查遍历所有不同器件对，不用旧groups.get(ref)豁免；OVAL/ELLIPSE使用保守矩形pad proxy。若proxy撞而真实形可能不撞，保留具体对与HOLD，不偷称nativeDRC。

Ruling: 无本地Git写，无worktree、提交、清理历史文件。新目录保留本阶段全部源/失败/预算/终审，用户已授权本电路公开报告GitHub发布。

Final: minor (disclosed): greedy free count actual53 corrected; no geometric effect.
Final: minor (deferred): occupancy heatmap clipped edge cells uniformly displayed; exact CSV provided, no third image.
Completed: offline placement2 passes, final images2, full source retained. No CAD.
