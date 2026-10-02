# 制造输入合同（未放行）
Authority: 16号；accepted PCB commit `e9c1b72f4d1659bb9a7a1dbe4a82e7937c5fe86a`。
本文件只定义以后询价/工艺审查所需输入，既不是订单，也不是制造指令。

| 输入 | 当前值/证据 | 状态 | 冻结责任 |
|---|---|---|---|
| 电气/布线基线 | 176器件/550pads/514assigned/107nets/36NC，15温冷DRC全0；本包不重跑 | PASS | 已接收16号 |
| 外形 | 原生矩形100.00000066×90.00000034mm，名义100×90mm | PASS | 原生geometry |
| 层数/顺序 | L1 signal/components+GND、L2 GND、L3 V5/V3V3+signal、L4 signal；物理制造叠层尚未选 | PASS（层用途） | 原生layer/4POUR |
| 板厂/服务类型 | PENDING，无选定板厂、无询价/上传板厂/订单 | PENDING_INPUT | 用户以后指定 |
| 板厚与公差 | PENDING | PENDING_INPUT | 用户/板厂 |
| 外层及内层铜厚 | PENDING；不能直接把现有6mil当任意厚铜可制造 | PENDING_INPUT | 用户/板厂 |
| core/prepreg及各介质厚度、材料/Tg | PENDING | PENDING_INPUT | 板厂实际四层stackup |
| 阻燃等级/UL认证要求 | PENDING，未从FR4名称推定具体等级 | PENDING_INPUT | 用户/板厂 |
| 外层/内层线宽线距 | 实测最窄6mil；现有Track-Track默认约.102mm、pad相关约.152mm、zone相关.254mm，10mil不是全部网络间距 | PENDING_INPUT（工艺接受） | 板厂匹配 |
| 常规通孔via | 297个，drill12mil/pad24mil，名义.3048/.6096mm，环宽.1524mm | PASS（现有几何） | 实際via |
| 通孔连接器 | 原生J1/J4孔约1.1mm、J2约1.0mm、J3约1.2mm；20PTH | PENDING_INPUT（实物匹配） | 明确连接器MPN/针截面 |
| 钻孔定义/孔公差/孔铜 | PENDING；上述CAD孔径不是未经工厂确认的最终成孔保证 | PENDING_INPUT | 板厂 |
| 阻焊颜色/扩展/公差/最小桥 | 现有默认pad扩展.0508mm；LM override约.05mm；细桥见openitems | PENDING_INPUT | 板厂CAM+用户确认 |
| via覆盖/塞孔/填孔 | via规则负扩展；工艺解释、是否允许露孔/盖孔尚未冻结 | PENDING_INPUT | 板厂 |
| 表面处理 | PENDING，不自动选择HASL/ENIG | PENDING_INPUT | 用户/板厂 |
| 最小铜到板边/铣边公差 | 既有用户铜筛查最低pad4.069mm/trace2.445mm/via2.394mm；POUR边界20mil，已填图边缘留距；尚无制造CAM | PENDING_INPUT（工艺接受） | 板厂 |
| 外形/固定孔/插接空间/板高 | 100×90实验室矩形已定，机械安装与连接器配对空间PENDING；不新加孔 | PENDING_INPUT | 用户 |
| 拼板/工艺边/定位孔/fiducial | PENDING，单板没有被本包自动加定位结构 | PENDING_INPUT | 板厂/装配厂 |
| 阶梯孔/盲埋孔/HDI/金属化槽/半孔 | 当前设计无要求或对象，常规through-via | NOT_APPLICABLE | 不新增 |
| 受控阻抗 | 当前没有受控阻抗网络要求；不引入SI/PI研究 | NOT_APPLICABLE | 若未来系统另提，单独审批 |
| 焊膏/钢网/贴装/回流/AOI/QFN检查 | PENDING，尤其RPW/DSE小无引脚封装 | PENDING_INPUT | 装配厂 |
| Gerber/drill/stackup/order | 全部本包0；不可依据review PNG下单 | PENDING_INPUT | 后续单独授权 |

JLCPCB仅作为公开普通工艺参考，未被选为供应商。依据与访问回执见 SOURCES.json、OFFICIAL_CAPABILITY_REFERENCE.md。任何生产数据生成、下单、制造、上电均未授权。

