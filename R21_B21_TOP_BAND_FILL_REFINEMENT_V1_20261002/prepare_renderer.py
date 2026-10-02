from pathlib import Path
P=Path(__file__).parent
s=(P.parent/'R21_PLACEMENT_B2_INTERLOCKING_V1'/'render_b2.py').read_text(encoding='utf8').split("m=b2['metrics'];grid=")[0]
s=s.replace("b2=json.loads((P/'PLACEMENT_B2.json')","b2=json.loads((P/'PLACEMENT_B21.json')").replace("old=json.loads((P/'PLACEMENT_B.json')","old=json.loads((P/'PLACEMENT_B2.json')").replace('ax.set_xlim(-22,85);ax.set_ylim(-4,83)','ax.set_xlim(-19,76);ax.set_ylim(-4,70)')
s+='''
reserve('finalImages','Single final B2 to B2.1 top-band-only comparison')
fig,axes=plt.subplots(1,2,figsize=(20,10),dpi=180)
draw(axes[0],old['positions'],'B2：顶部左侧空带',old['metrics']['naturalBBoxMm'])
draw(axes[1],b2['positions'],'B2.1：仅MUX小块与4个拉阻左移28mm',b2['metrics']['naturalBBoxMm'])
fig.suptitle('最后一轮顶部构图：170器件位置完全冻结，6器件平移',fontproperties=FONT,fontsize=20,y=.98)
fig.text(.5,.035,'两侧同一真实尺度；176器件/552焊盘，94关键pad距离保持，全部15,400器件对body/pad proxy不相交。\\n自然器件包络仍71×63.5mm，未改板框/原生PCB。FFC完整翻盖扫掠仍HOLD，不代表DRC、布线或制造放行。',fontproperties=FONT,fontsize=10,ha='center')
fig.subplots_adjust(left=.04,right=.98,top=.86,bottom=.19,wspace=.08)
fig.savefig(P/'PLACEMENT_B2_VS_B21.png');plt.close(fig)
print('One final comparison exported, no further images available.')
'''
(P/'render_b21.py').write_text(s,encoding='utf8')
