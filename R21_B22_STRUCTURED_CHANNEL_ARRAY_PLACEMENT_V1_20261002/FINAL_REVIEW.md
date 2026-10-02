# 唯一新鲜只读终审 — /root/b22_structured_final_review
可作为有明确限制的 B2.2 PARTIAL/HOLD 草案交付；不能认定全部 B2.2 要求完成，更不能进入 CAD／制造放行。无需也不应新增布局或图片。
Critical：无。
Important1：independent_audit.py原42–53缺CENTRAL_POSITIONAL_MIRROR/PIN_FORCED_BASELINE判定，默认ok=True；2+2未核pitch、ADC未核行间距。只读最终坐标实际均符合相应声明，但初始审计覆盖声明过强。应补显式分支，未知模板不得默认PASS，保留旧证据。
Important2：Pro要求BIAS左右/共同轴镜像，实际为中心配对。HF/FB/ISO的VCM侧相对U3(-.9,-4.5)、(-3,-4)、(-3,-6)，另一側取反；不能由同一反射轴逐一对应。原PASS_POSITIONAL_CENTRAL_MIRROR_ONLY容易误当要求通过，改PARTIAL_CENTRAL_PAIRING_AXIS_MIRROR_HOLD。无需重排。
Minor1：额外距离实际12条pin-pair覆盖10IC/passive组合，5条增加；U11/U12VDD各匹配两个ICpad。报告与matrix/write_receipt的All10comparisons/5of10应改12条/10组合。五条失败数值本身正确并明确披露。
新鲜只读核验：
- 七项source/copySHA均一致。
- CSV/JSON176unique相同，125位置/角变化；15IC+4J锚点全冻结。
- 552pads514assigned107nets36NC/J2八signal+两emptyMP成立。
- B2.1/B2.2bodybbox71.0000204×63.5000124相同。
- body和conservativeproxy各15400distinctpairs均无>1e-8mm2交叠，FFCplanning0。
- 94继承距离几何/CSV一致、maxincrease0；12额外距离数值吻合、5增加。
- 56模板151不重复成员+25固定；实际行列/等距/2+2/ADC4×2坐标成立，singleton已披露，非56多件阵列。
- pendingguard保留未处理的原94critical位置，豁免candidate自身，adopt后释放；只读probe未来C_ADCD占用拒绝、合法自身DVDD不误拒；不代表所有critical已受保护。
- 唯一图已查看，同尺度等比例，标题5额外待收口，与实际坐标相符。
- 2adjust/1image日志预算一致，firstfailedcode/traceback/REDGREEN保留，首次无完整partialcoords已明示。
- Power不同pitch、debug不同方向、digital未共同ICtemplate、3ADCbank未成行列均已PARTIAL/HOLD。
拒绝据此判断/放行：原生PCB一致性/DRC、实际走线长度和性能、制造courtyard/装配净距、FFCactuator/配合、用户最终选择、制造bench。175body源nativecomponentshape，1官方尺寸保守2D包络，不是完整装配认证。有限模板失败非数学不可行证明。
完成文档/审计覆盖修正可交现有坐标/唯一图和完整HOLD回执；第三次调整/第二图仍禁，不二审。

