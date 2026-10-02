from pathlib import Path
import json,math,hashlib,datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle,Polygon
P=Path(__file__).parent
read=lambda n:json.loads((P/n).read_text('utf8'))
w=read('FINAL_WARM_PCB.json');a=read('FINAL_EVIDENCE_AUDIT.json');j=next(x for x in w['parts']if x['ref']=='J2')
def rows(s):
 z=[]
 for l in s.splitlines():
  if '||'in l:
   h,b=l.split('||',1);z.append((json.loads(h),json.loads(b.rstrip('|'))))
 return z
rw=rows(w['source']);rf=rows((P/'J2_FINAL_WARM_FOOTPRINT_SOURCE.txt').read_text('utf8'))
sx,sy=j['x']*.0254,j['y']*.0254
def draw(ax,local=False):
 ax.add_patch(Rectangle((0,0),100,90,fc='#174b36',ec='#26364b',lw=2,zorder=0))
 for h,b in rw:
  if h['type']=='LINE':
   ax.plot([b['startX']*.0254,b['endX']*.0254],[b['startY']*.0254,b['endY']*.0254],color={1:'#f07579',2:'#61a8f5',16:'#d6b663'}.get(b['layerId'],'#bba467'),lw=max(.35,b.get('width',6)*.0254*1.5),alpha=.85,zorder=1)
 for c in w['parts']:
  for p in c['pads']:
   x,y=p['x']*.0254,p['y']*.0254;pad=p['pad']
   if pad[0]=='POLYGON':
    v=[q for q in pad[1] if isinstance(q,(float,int))];ax.add_patch(Polygon([(v[i]*.0254,v[i+1]*.0254)for i in range(0,len(v)-1,2)],fc='#c0cbd0',ec='#253746',lw=.2,zorder=3));continue
   ww,hh=pad[1]*.0254,pad[2]*.0254
   rot=p['rotation'];rect=Rectangle((x-ww/2,y-hh/2),ww,hh,angle=rot,rotation_point='center',fc='#e5c077' if c['ref']=='J2'else'#c0cbd0',ec='#253746',lw=.2,zorder=3);ax.add_patch(rect)
   if p['hole']:ax.add_patch(Circle((x,y),.25,fc='#102d22',zorder=4))
  if not local:ax.text(c['x']*.0254,c['y']*.0254,c['ref'],fontsize=3,color='#e1eae7',ha='center',va='center')
 for h,b in rw:
  if h['type']=='VIA':ax.add_patch(Circle((b['centerX']*.0254,b['centerY']*.0254),b['viaDiameter']*.0254/2,ec='#1a2d44',fc='#d1b772',lw=.25,zorder=2))
 # Project's native assembly artwork, not a qualified manufacturer body datum.
 ax.add_patch(Rectangle((sx-4.8,sy-6.6),5.3,13.2,fill=False,ec='#ffffff',lw=1.5,zorder=4))
 if local:
  for h,b in rf:
   if h['type']=='STRING':
    # Native placement rotated with J2; note stroke font glyph geometry is not reproduced.
    xx=sx-b['y']*.0254;yy=sy+b['x']*.0254
    ax.text(xx,yy,b['text'],rotation=90,fontsize=8,color='white',ha='left',va='bottom',zorder=5)
  for p in j['pads']:
   ax.text(13.7,p['y']*.0254,f"{p['number']}  {p['net'] or 'mechanical / no net'}",fontsize=9,va='center',color='white',zorder=5)
  ax.annotate('FFC ribbon enters toward connector\nconductors face PCB (contract; native text missing)',xy=(1.4,39),xytext=(-7.5,48.7),arrowprops={'arrowstyle':'->','color':'#66c8f1'},fontsize=9,color='#163b58',bbox={'facecolor':'white','alpha':.9,'edgecolor':'none'})
  ax.set_xlim(-8,28);ax.set_ylim(28,53)
 else:ax.set_xlim(-1,101);ax.set_ylim(-1,91)
 ax.set_aspect('equal');ax.set_xlabel('PCB x (mm)');ax.set_ylabel('PCB y (mm; native positive upward)')
fig,ax=plt.subplots(figsize=(12,10),dpi=200);draw(ax);ax.set_title('Actual final warm PCB: J2 converted to 8P 1mm FFC/FPC ZIF\nWhite frame = native artwork; body datum and cold closure HOLD, not fabrication release',fontsize=13);fig.tight_layout();fig.savefig(P/'PCB_FINAL_WARM_REVIEW.png');plt.close(fig)
fig,ax=plt.subplots(figsize=(13,8),dpi=180);draw(ax,True);ax.set_title('J2 actual warm pad-net and local fanout\nWhite frame = native artwork, body datum unqualified; CONTACT native silk / cold HOLD',fontsize=13);fig.tight_layout();fig.savefig(P/'J2_FFC_ACTUAL_WARM_DETAIL.png');plt.close(fig)
mech={'source':'warm actual pad coordinate + project native assembly artwork; manufacturer body datum relative to pad row NOT_QUALIFIED','signalRowXmm':sx,'illustrativeNativeArtworkXrangeMm':[sx-4.8,sx+.5],'illustrativeNativeArtworkYrangeMm':[sy-6.6,sy+6.6],'oldIncorrectConservativeEnvelope':'original x1.2..6.5 frame omitted native artwork right0.5mm; original images retained BEFORE_REVIEW only','manufacturerBodyDatum':'HOLD','neighborMechanicalClearance':'HOLD','closedHeightMm':'1.9±0.2 official nominal','openActuatorApproxHeightMm':3.95,'cableEntersFrom':'left PCB edge horizontally by project contract','boardBoundsMm':[0,100,0,90],'bodyEnvelopeQualified':False,'enclosureUnknown':True,'actualMatedMechanicalValidation':False,'CONTACTSideNativeText':'missing final source, contract only','flipSweepFull3D':'NOT_QUALIFIED'}
(P/'J2_MECHANICAL_2D_CHECK.json').write_text(json.dumps(mech,indent=2),'utf8')
docs={
'J2_FFC_FPC_CONNECTOR_SPEC.md':'''# 当前J2板座合同（审查，不是制造放行）

用户确认FFC/FPC薄软排线翻盖插槽类型；1.00mm及无现成线材并非用户已回答。Pro20批准默认Molex **2005290081**，8P、1mm、FrontFlip/ZIF、bottom-contact、直角SMT。原1718560008+22012087 KK254离散线束接口已superseded，旧包不回写。

实际温态新封装8个信号SMT焊盘0.40×1.00mm/1mm pitch，加2个2.00×1.30mm固定焊片。MP1/MP2保留真实空网，不随意接GND。信号1–4 ROW0–3，5–8 COL0–3。原生器件Name/MPN为2005290081；封装/通用器件库旧KK/HDR名称仍残留，不能把它们当厂家器件匹配证书。PCB otherProperty旧3D字段清空，但封装源D3_ATTRIBUTE仍在，不可使用其3D外形证明兼容。

只限厂家图纸派生几何及温态审查。底接触和翻盖空间实际线材/外壳未验证，独立冷态和正式原生File未完成。
''',
'J2_FFC_CABLE_SPEC.md':'''# 当前软排线默认标准

Pro20默认Molex Premo-Flex **154670229**：8芯、1.00±0.05mm pitch、102±3mm长、TypeA两端同面、端部加强后厚0.30±0.05mm；厂家图纸注明可配200529系列。接触暴露3.5±0.5mm，对应板座推荐3.5±0.3mm存在边界差异，制造时需厂商确认，不能声称全公差机械兼容已证。

已有用户排线规格未知，若给真实pitch/厚度/接触面则优先匹配，不把默认1mm说成人工确认。底接触要求板端导体朝PCB；TypeA同面不能证明远端接插件编号。配线装前两端断开，验证8条正确通路和任意两线28组隔离，不注入电源/短路故障。本包实际测线/采购/装配0。
''',
'J2_PINOUT_AND_ORIENTATION.md':'''# J2行列和方向

未旋转封装顶部观察，以后端焊尾从左到右定义项目Pin1–8；厂商图纸没有编号标记，不冒称厂商模塑Pin1。板上旋转90°、信号行x6.5mm，Pin1 y35.5mm为ROW0，往上依次到Pin8 y42.5mm COL3。MP1/MP2是固定焊片空网。

FFC从PCB左边水平插入，导体面朝PCB；翻盖闭合后锁住薄排线。插入侧观察左右会反转，按实际导体通路验证远端编号。Rij接ROWi/COLj，绝不可将排线某芯当电源/GND。

温态封装原生字符串实际只有J2、1、ROW、COL、FFC INSERT。初始工作源含CONTACT PCB，final source已缺失；CONTACT_SIDE_NATIVE_SILK_HOLD。静态方向图补充说明，不能替代Pro20要求的原生文字。Pin1三角原生POLY和项目编号参考，最终独立原生仍待核验。
''',
'FABRICATION_INPUT_CONTRACT.md':'''# 制造输入合同（未放行）

沿用正常1–7kΩ/0.8–8k保护带、4×4/8线、5V+3V3、VCM2.5/VEXC2.25/E0.25/Rf4.99k/Cf2.2nF/100fps目标，主电路175器件、100×90mm板框和规则不改。本包仅J2 SMT接口局部ECO。FR4/4层/1.6mm/内外1oz/green/ENIG只是既有建议，真实厂家和CAM合同仍缺。

旧KK254的J2八个1.14mm特殊PTH孔要求对新SMT接口superseded；不扩展为其他孔已合格。新增8个局部via hole12mil/diam24mil，厂家环宽/孔位及全板细阻焊桥仍需实际CAM接受。U5/U9/U10约0.090–0.097mm mask桥问题继承，不因温态DRC0自动放行。

原生File导出未产生，保存项目仅本地保留且冷态不合格。没有Gerber、生产文件、采购、制造、bench、上电授权。不可拿此包直接下单。
''',
'MANUFACTURING_OPEN_ITEMS.md':'''# 实际未闭合输入

- 独立冷重开与四类DRC、全量pad-net、真实无账户数据epro2导出：本包失败/未得到结果，禁止声称已PASS。
- 原生CONTACT SIDE文字、残留KK封装名称和D3字段，需要J2-only有限收尾；不研究setter/API。
- 用户现有FFC pitch/厚度/同异面接触规格未知；1mm成套是Pro20默认，供应和实物配插未测。
- 厂商确认154670229暴露长度全公差与200529座匹配，真实工厂/叠层/CAM阻焊/孔位与装配。
- 旧J1/J3/J4准确manufacturerMPN未定，本包不扩大为采购替换。
- 主电路实体精度、速度/WCET/100fps、容量/供电故障、样机人员仪器缺项继续HOLD。

旧KK合同历史保留，新FFC默认方向合同为当前用户需求；新板暂PCB_REVIEW_READY=false。无实体操作。
''',
'CLOSURE_FAILURE_AND_NEXT_SCOPE.md':'''# 检查失败和唯一收尾路线

温态完整检查和DRC0真实有效。第一次warm NetlistError1只因J2的FFC Cable属性未同步；GUI导入变更清单仅此一项，应用后warm value=[]。不是电路短路或行列错接。

cold session启动时温态GUI仍未完全关闭；两次冷DRC报画布主题未订阅，最后cold full报获取所有器件失败，尚未到实际File导出。两次预扣DRC与一次capture/export全部留账，不把失败追回成成功，也不能断言软件bug。后来两自有session官方closed且两GUI正常退出、fresh窗口列表空。独立cold门未资格。

在不修API工具、改铜或重做科学包的前提，建议唯一180min收尾包：J2接触面文字/旧3D标记的既有正常编辑40min，先真正关闭全部自有窗口再新GUI重新打开当前工作工程、正常DRC及保存导出60min，核验与公开交付80min。source0/candidate0/copy0/session2/save2/capture3/DRC2/export1/pour0；LINE/VIA/规则/值/主铜变化0。这是本次正常报告按用户明确更多有界时间/次数/自主范围要求提出的申请，未批不执行；不是平台额度提升，不单独追加审批消息。

本地eprj2是SQLite，检测到非空users.password及账户字段，值从未输出；原文件不修改、不公开。未来仅标准epro2导出后再凭据扫描，避免发布账户库。当前公开own source/TXT/CSV/PNG和完整失败回执，原项目文件留本地hash审计。
'''}
for n,t in docs.items():(P/n).write_text(t,'utf8')
urls={'S1':'https://www.molex.com/en-us/products/part-detail/2005290081','S2':'https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/200/200529/2005290061_sd.pdf','S3':'https://www.molex.com/en-us/products/part-detail/154670229','S4':'https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/154/15467/154670229_sd.pdf'}
sources=[]
for code,url in urls.items():
 f=next((P/'sources_local_only').glob(code+'_*'+('.pdf'if code in ['S2','S4']else'.html')))
 sources.append({'source':code,'url':url,'localFile':f.name,'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest().upper(),'publicBulk':False,'publicOwnSummary':'P0_SOURCE_QUALIFICATION.md'})
(P/'OFFICIAL_SOURCE_INDEX.json').write_text(json.dumps(sources,indent=2),'utf8')
a['footprintLibraryGetterName']='Old KK name remains in native ATTR/getter; warm actual 10-pad manufacturer-derived geometry, no catalog or cold identity qualification.'
(P/'FINAL_EVIDENCE_AUDIT.json').write_text(json.dumps(a,indent=2),'utf8')
print(json.dumps({'rendered':2,'contracts':6,'bodyDatumQualified':False,'sources':4,'coldUnqualified':True}))
