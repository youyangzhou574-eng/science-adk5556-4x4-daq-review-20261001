# Unique final-review disposition

唯一fresh-context审查FINAL_REVIEW.md：Critical0、Important1、Minor1。两图实际查看，101/363/5050、16bank、172边、5串阻链、28代表边、7源/副本SHA独立核过；没有二审。

Important I1接受：ROW_PIN_SIDE_ADJACENCY。实际J2占位pin1..4 ROW在世界x6/y25.5..28.5（下半），COLpin5..8在y29.5..32.5（上半）。U4=(14,37.5)、U1=(21.5,37)上方，U2=(20,25.5)下方。与Pro要求ROW宏贴ROW侧存在明确合同差异。ROW驱动支路代理11.386..11.938mm、sense15.254..16.730mm；两支路差3.868..4.792mm。这不是有数值硬门的电气FAIL，也不是厂家物理pin方向已经资格。

Final: Ruling: 保留完整101、全5050保守几何与bank身份PASS以及供工程审查的图，限缩“无条件宏布局收口”，添加J2_PIN_SIDE_ROW_ADJACENCY_HOLD、ALL_MACRO_LAYOUT_INTENTS_ACCEPTED=false、NATIVE_PLACEMENT_ELIGIBLE=false。真实接口方向/邻近取舍需Pro明确书面裁定；不能借剩placement或STOP后quota立即转J2、改针序、搬ROW、重画。若下一范围需要实际修正，使用新的具体工程授权。

一pass只改文档/门：保留PRE_REVIEW_GATES/PRE_REVIEW_FULL_OFFLINE_AUDIT，标明新HOLD与精确pin方向；不修改坐标、PNG、原始输入、budget事件。verify_review_disposition.py先RED缺HOLD，再GREEN7项含禁止native提升、旧全101/363/5050和输入SHA。这个修复关闭的是“遗漏HOLD/完成声明过度”问题，I1实际方向取舍仍OPEN；不称布局修正已发生。

Minor M1 deferred：detail裁剪外小标签泄漏；CSV和全图精确位置可用，两图额度满，不第三图。不是几何FAIL，不独立出版图。

Declined-to-judge rulings：nativeDRC/真实铜回流/可布通性未执行；FFC/J1/J3/J4厂家mating机械未资格；Ceff/ESL/动态100fps/精度温区保护bench保持HOLD；用户满意未确认；52mm备选未执行不称最优。远端发布验证由独立送达账完成，不借本审查声称。以上不引出工具研究或新布局。

Final: fixed Important report/gate overclaim — verification RED→GREEN7/7。Actual ROW direction/adjacency question OPEN, requires unified engineering disposition. No coordinates/images/science rerun.
