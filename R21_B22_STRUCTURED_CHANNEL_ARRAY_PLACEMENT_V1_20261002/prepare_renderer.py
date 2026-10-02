from pathlib import Path
P=Path("E:/open/SCIENCE_ADK5556_4X4_DAQ_REPLICA/R21_B22_STRUCTURED_CHANNEL_ARRAY_PLACEMENT_V1")
S=P.parent/'R21_B21_TOP_BAND_FILL_REFINEMENT_V1'
s=(S/'render_b21.py').read_text(encoding='utf8')
s=s.replace("b2=json.loads((P/'PLACEMENT_B21.json').read_text(encoding='utf8'));old=json.loads((P/'PLACEMENT_B2.json').read_text(encoding='utf8'))","b2=json.loads((P/'PLACEMENT_B22.json').read_text(encoding='utf8'));old=json.loads((P/'PLACEMENT_B21.json').read_text(encoding='utf8'))")
s=s.replace("Single final B2 to B2.1 top-band-only comparison","Single final B2.1 to B2.2 structured-channel comparison")
s=s.replace("B2：顶部左侧空带","B2.1：调整前").replace("B2.1：仅MUX小块与4个拉阻左移28mm","B2.2：功能内等距行列／引脚侧镜像模板")
s=s.replace("最后一轮顶部构图：170器件位置完全冻结，6器件平移","B2.2 器件排列：芯片／接口骨架固定，同功能阻容形成规则组")
s=s.replace("两侧同一真实尺度；176器件/552焊盘，94关键pad距离保持，全部15,400器件对body/pad proxy不相交。\\n自然器件包络仍71×63.5mm，未改板框/原生PCB。FFC完整翻盖扫掠仍HOLD，不代表DRC、布线或制造放行。","两侧同一真实尺度；仅离线坐标草案，未改原生PCB、板框或布线。\\n四通道按实际引脚分布分组；严格距离门优先，未实现的规则组在报告中逐项列出。FFC完整翻盖、实际DRC与制造仍未放行。")
s=s.replace("PLACEMENT_B2_VS_B21.png","PLACEMENT_B21_VS_B22.png")
(P/'render_b22.py').write_text(s,encoding='utf8')
print('Renderer source prepared only, image count remains0')

