# 装配与可探测性清单
冻结PCB不修改，所有结论限既有几何和既有针网数据。PRO16已接受电气基线；本包没有新DRC/捕获/export。
`ASSEMBLY_AND_PROBE_REVIEW.png`是原生body/pad投影的只读图，不含完整阻焊、丝印、铜/钢网/3D，不可制造。红点是component marking，不等于已验证制造丝印。绿圈编号对应13行 `EXISTING_TEST_ACCESS_CANDIDATES.csv`。

| 对象 | 针号/间距与方向证据 | 当前接受/制造待项 |
|---|---|---|
| U1/U2 OPA4388IDR | native14pins，1.27mm pitch；pin1上侧左端，rotation0；继承已接受manufacturer pinmap | PASS number/pitch；SOIC可外露焊接，无独立exposedpad；实物pin1方向/丝印/装配检查PENDING |
| U3 OPA2388IDR | native8pins，1.27mm；pin1上侧左端，rotation0；既有pinmap | PASS number/pitch；实物/装配同上 |
| U4 TMUX1134PWR | native20pins，名义.65mm；pin1左上，rotation0；既有pinmap | PASS number/pitch；不重新查第7份datasheet |
| U5 ADS8684IDBTR | native38pins，名义.5mm；rotation180，pin1右下；官方DBT0038A图已看 | PASS pins/方向对应；current .3×1.3mm左右land是1.5mm官方example的不同版本，不声称example严格同；钢网/land接受PENDING |
| U7 STM32G031K8T6 | native32pins，.8001mm actual centers、7×7mm body；ST DS12992 rev4 .8mm LQFP32，无中心exposedpad；rotation0 | PASS count/pitch；原生pad约.447×1.684mm不同于ST example .45×1.2mm，land/stencil审批PENDING，不据此单独判针错 |
| U9/U10 LM73100RPWR | 原生10pads，无额外中心pad；5/6两个长powerland、1/4/7/10 corner polygons；厂家RPW0010A p50已看；pin1左下，与rotation0布局一致 | PASS number/可辨方向；.45/.475混合间距，禁止把全部焊盘一律按.45mm；小2mm QFN-HR需回流/钢网/AOI或适当检验，手焊不默认可靠 |
| U11/U12 TPS389001DSET | 6pins，.5mm pitch，1.5mm DSE；实际pin1左下，与官方topview对应；无第7中心pad | PASS pin set；官方land区分1–3 SMD和4–6 NSMD，当前默认正mask扩展并非严格复制该example，assembler/fab acceptance PENDING |
| BAT54S,215（D_TIA等） | 原生1/2同侧、3另一侧；1/2间距1.89992mm，接GND/V5/对应输出；Nexperia SOT23 p5已看 | PASS pin pattern；系列封装方向不能与REF3025三脚外观混淆，装配极性核对必做 |
| J1–J4 | native2/8/6/4 pins均2.54mm；rotation90；pin1方pad在上方；原生drill1.1/1.0/1.2/1.1mm | PASS number/pitch/drill geometry；generic header无Manufacturer/MPN，必须指定实物配对pin截面、外壳和插接方向后才可采购装配 |

全176器件native pad-number集合与550实际pad列表一致，见PAD_NUMBER_COVERAGE.json。该检查证明号码覆盖，不代替厂商内部焊盘定义/符号功能复审。当前结构BOM172个有MPN，4个J1–J4仍为空；不引用Description乱码。
175个可解析native layer48 nominal body无2D重叠，最近U9_IN_CAP↔U9_OV_B2约.300002mm；U6无支持的该POLY48 body对象，未得到全176 courtyard/3D保证。每个器件极限尺寸、工具吸嘴/烙铁空间、插头高度仍由装配流程确认。
U5/U9/U10阻焊桥约.096774/.090081/.090081mm，不能宣称满足所有板厂颜色/铜厚；见制造openitems。没有生成Gerber或运行factory DFM。

探点优先较大被动件/连接器pad，不默认直接戳.25mm QFN。13候选含V5_IN/V5/V3V3/REF_2V5/VCM/VEXC/PGOOD/ROW0/TIA_DRV0/TIA0/ADC_IN0/MCU_NRST_EXT/GND。PGOOD选R_RST.2，外侧NRST选J3.5，二者不是同一裸网。TIA0与TIA_DRV0分开。不能把REF_2V5、VCM、VEXC混为一个节点。
probe型号/固定夹、接地参考、人员、仪器和实际样机仍未知。点位存在不等于允许上电、安全探测或时序验证。先断电固定探头；日后上电必须获新的具体实体release，当前bench/powerup=0。不要求现在增加testpoint。

