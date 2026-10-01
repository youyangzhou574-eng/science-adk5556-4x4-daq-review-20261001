# 已接受网表的探点映射

以下是元件脚映射，不声称已有实体test pad或样机。人员须先在实体核脚/地，夹线在断电时完成；不在相邻细脚带电移动探头。

| 信号 | 已有真实网络成员中的探点 |
|---|---|
| 输入 | J1.1 V5_IN，J1.2 GND |
| 板上5V/3V3 | U9.6 V5；U10.6 V3V3；先优选对应去耦正端核实体位置 |
| REF_2V5 | U6.2，供VCM参考；不是ADC4.096V参考 |
| VCM /VEXC | R_VCM_ISO.2 /R_VEX_ISO.2，补偿后板上输出 |
| ROW0..3 | J2.1..4，各R_ISOi.2 |
| COL0..3 | J2.5..8 |
| TIA0..3 tap | R_TIA_ISOi.2、R_ADCi.1 |
| TIA_DRV0..3 | R_TIA_ISOi.1，探驱动侧区分tap |
| ADC_IN0..3 | C_ADCi.1，U5.16/.18/.21/.23 |
| ADC_REFIO /REFCAP | C_ADC_REFIO.1 U5.5；C_ADC_REFCAP.1 U5.7 |
| PGOOD/NRST | U7.6、R_RST.2、U11.6/U12.6为PGOOD同网 |
| 外部NRST | J3.5→MCU_NRST_EXT→R_J3_5 1k→PGOOD；不是旧Schmitt/G07候选 |
| 两sense | J3.1 V3V3_EXT_SWD；J4.1 V3V3_EXT_UART；各4.99k到V3V3，不作供电输入 |

所有公共地接GND；示波器保护地/探头地先核，禁止将地夹夹ROW/TIA/REF。SWD目标供电识别脚只sense，禁止调试器另一电源与板电源并供。PGOOD两监控OD并联、R_RST上拉；外部NRST只允许后续明确OD/OC正常低与HiZ，禁止推挽高/±电压强注入。
