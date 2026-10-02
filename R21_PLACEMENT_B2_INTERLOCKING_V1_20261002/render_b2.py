from placement_geometry import *
import numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as PatchPolygon,Rectangle,Ellipse,FancyBboxPatch
from matplotlib.transforms import Affine2D
from matplotlib.font_manager import FontProperties
FONT=FontProperties(fname=r'C:\Windows\Fonts\msyh.ttc')
COLORS={'AFE':'#306b53','BIAS':'#655488','ADC':'#316fa1','DIGITAL':'#675d99','POWER':'#9a6536','EXTERNAL':'#3a8181'}
NAMES={'AFE':'模拟前端','BIAS':'激励/偏置','ADC':'ADC','DIGITAL':'数字控制','POWER':'电源','EXTERNAL':'外部/调试'}
b2=json.loads((P/'PLACEMENT_B2.json').read_text(encoding='utf8'));old=json.loads((P/'PLACEMENT_B.json').read_text(encoding='utf8'))
def draw(ax,positions,title,bbox):
    for r,g in G.items():
        pos=positions[r];poly=body(r,pos)
        for part in getattr(poly,'geoms',[poly]):ax.add_patch(PatchPolygon(list(part.exterior.coords),facecolor=COLORS[regions[r]],edgecolor='#20332c',linewidth=.35,alpha=.85,zorder=3))
        for p in g['pads']:
            x,y=newpad(r,p,pos);sh=p['shape'];a=p['rotation']+pos[2]-g['rotation']
            if sh[0]=='POLYGON':
                v=[v for v in sh[1]if isinstance(v,(int,float))];points=[newpad(r,dict(xMm=v[i]*.0254,yMm=v[i+1]*.0254),pos)for i in range(0,len(v),2)]
                patch=PatchPolygon(points,facecolor='#c6b072',edgecolor='#8a753a',linewidth=.2,zorder=2)
            else:
                w,h=sh[1]*.0254,sh[2]*.0254
                if sh[0]=='ELLIPSE':patch=Ellipse((x,y),w,h,angle=a,facecolor='#c6b072',edgecolor='#8a753a',linewidth=.2,zorder=2)
                elif sh[0]=='OVAL':
                    patch=FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle=f'round,pad=0,rounding_size={min(w,h)/2}',facecolor='#c6b072',edgecolor='#8a753a',linewidth=.2,zorder=2);patch.set_transform(Affine2D().rotate_deg_around(x,y,a)+ax.transData)
                else:patch=Rectangle((x-w/2,y-h/2),w,h,angle=a,rotation_point='center',facecolor='#c6b072',edgecolor='#8a753a',linewidth=.2,zorder=2)
            ax.add_patch(patch)
        if r.startswith(('U','J'))and'_'not in r:ax.text(pos[0],pos[1],r,fontsize=6.5,color='white',weight='bold',ha='center',va='center',zorder=4)
    j=positions['J2'];mouth=j[0]-5.5
    ax.add_patch(Rectangle((mouth-10,j[1]-8.7),10,17.4,fill=False,hatch='///',edgecolor='#439ca4',linewidth=.6))
    ax.annotate('FFC 插入',xy=(mouth,j[1]),xytext=(mouth-11,j[1]),fontproperties=FONT,fontsize=8,arrowprops={'arrowstyle':'->','color':'#439ca4'},ha='right',va='center',color='#338b94')
    pin=next(p for p in G['J2']['pads']if p['number']=='1');ax.plot(*newpad('J2',pin,j),'o',color='#c43131',markersize=3,zorder=5)
    ax.add_patch(Rectangle((bbox[0],bbox[1]),bbox[2]-bbox[0],bbox[3]-bbox[1],fill=False,linestyle='-.',edgecolor='#365b48',linewidth=.9))
    ax.set_title(title,fontproperties=FONT,fontsize=15,pad=12);ax.set_xlabel('x / mm');ax.set_ylabel('y / mm');ax.set_aspect('equal');ax.grid(alpha=.08);ax.set_xlim(-22,85);ax.set_ylim(-4,83)
    handles=[Rectangle((0,0),1,1,facecolor=COLORS[n],label=NAMES[n])for n in COLORS];ax.legend(handles=handles,prop=FONT,ncol=3,loc='upper center',bbox_to_anchor=(.5,-.1),frameon=False)
m=b2['metrics'];grid=np.load(P/f'OCCUPANCY_B2_PASS_{m["pass"]}.npy')
reserve('finalImages','Final B2 no-copper placement with conservative occupancy map')
fig,(ax,occ)=plt.subplots(1,2,figsize=(16,10),dpi=180,gridspec_kw={'width_ratios':[2.6,1]})
draw(ax,b2['positions'],'B2：小刚体锁定，功能区自由咬合\n自然器件包络 71.0 × 63.5 mm',m['naturalBBoxMm']);ax.set_xlim(-19,75);ax.set_ylim(-4,69)
bb=m['naturalBBoxMm'];occ.imshow(grid,origin='lower',extent=[bb[0],bb[2],bb[1],bb[3]],cmap='Greys',vmin=0,vmax=1,interpolation='nearest');occ.set_aspect('equal');occ.set_title('1mm body相交占用栅格\n黑色有body，白色无body',fontproperties=FONT,fontsize=11);occ.set_xlabel('x / mm');occ.set_ylabel('y / mm')
rect=m['largestEmptyRectMm'];occ.add_patch(Rectangle((rect[0],rect[1]),rect[2]-rect[0],rect[3]-rect[1],fill=False,edgecolor='#c93434',linewidth=1));occ.text(.5,-.15,f'完整空格最大矩形：{m["largestEmptyFullCellRectangleAreaMm2"]} mm²\n保守栅格指标，非DRC/布线余量',transform=occ.transAxes,fontproperties=FONT,fontsize=9,ha='center')
fig.suptitle('B2咬合式器件布局 · 实际PCB未改动',fontproperties=FONT,fontsize=21,y=.97)
fig.text(.5,.045,'176器件 / 552焊盘；94组关键pad距离保持；body及保守pad proxy全部不同器件对无相交。\nFFC为官方尺寸规划包络，完整翻盖扫掠HOLD；虚线是自然包络，不是板框。未布线、未原生DRC、未制造放行。',fontproperties=FONT,fontsize=10,ha='center')
fig.subplots_adjust(left=.04,right=.98,top=.87,bottom=.2,wspace=.08);fig.savefig(P/'PLACEMENT_B2_NO_COPPER.png');plt.close(fig)
reserve('finalImages','Final old B vs same B2 comparison')
fig,axes=plt.subplots(1,2,figsize=(20,10),dpi=180)
draw(axes[0],old['positions'],'旧 B：81.0 × 77.9 mm',old['metrics']['naturalBodyBoundingBoxMm']);draw(axes[1],b2['positions'],'新 B2：71.0 × 63.5 mm',bb)
fig.suptitle('旧 B → 新 B2：关键小模块不拆，普通器件填缝',fontproperties=FONT,fontsize=21,y=.98)
fig.text(.5,.035,'同一176器件、同一真实尺度、同一坐标缩放；仅离线布局。旧B指标有终审缺项，不能把旧零当完整验证。\nB2 body/保守pad proxy全组合检查；器件身份/值/封装/针序/网络不改。选定后才能进入原生搬件与布线。',fontproperties=FONT,fontsize=10,ha='center')
fig.subplots_adjust(left=.05,right=.98,top=.86,bottom=.18,wspace=.08);fig.savefig(P/'PLACEMENT_OLD_B_VS_B2.png');plt.close(fig)
print('Two final images exported; no native/CAD/API/GUI.')
