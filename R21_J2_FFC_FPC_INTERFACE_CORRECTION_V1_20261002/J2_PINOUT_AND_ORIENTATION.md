# J2行列和方向

未旋转封装顶部观察，以后端焊尾从左到右定义项目Pin1–8；厂商图纸没有编号标记，不冒称厂商模塑Pin1。板上旋转90°、信号行x6.5mm，Pin1 y35.5mm为ROW0，往上依次到Pin8 y42.5mm COL3。MP1/MP2是固定焊片空网。

FFC从PCB左边水平插入，导体面朝PCB；翻盖闭合后锁住薄排线。插入侧观察左右会反转，按实际导体通路验证远端编号。Rij接ROWi/COLj，绝不可将排线某芯当电源/GND。

温态封装原生字符串实际只有J2、1、ROW、COL、FFC INSERT。初始工作源含CONTACT PCB，final source已缺失；CONTACT_SIDE_NATIVE_SILK_HOLD。静态方向图补充说明，不能替代Pro20要求的原生文字。Pin1三角原生POLY和项目编号参考，最终独立原生仍待核验。
