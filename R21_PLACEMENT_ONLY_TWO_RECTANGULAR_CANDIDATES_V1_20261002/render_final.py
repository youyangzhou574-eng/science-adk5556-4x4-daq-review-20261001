from pathlib import Path
import json,math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as PatchPolygon, Rectangle, Ellipse, FancyBboxPatch
from matplotlib.transforms import Affine2D
from matplotlib.font_manager import FontProperties
from placement_common import P,G,body
from reserve import reserve
FONT=FontProperties(fname=r'C:\Windows\Fonts\msyh.ttc')
COLORS={'AFE':'#306b53','BIAS':'#655488','ADC':'#316fa1','DIGITAL':'#675d99','POWER':'#9a6536','EXTERNAL':'#3a8181'}
NAMES={'AFE':'传感/模拟前端','BIAS':'激励/偏置','ADC':'ADC','DIGITAL':'数字控制','POWER':'电源','EXTERNAL':'外部/调试'}
data={a:json.loads((P/('PLACEMENT_'+a+'.json')).read_text(encoding='utf8'))for a in'AB'}
def newxy(r,x,y):
    g=G[r];px,py,a=data[current]['positions'][r];theta=math.radians(a-g['rotation'])
    u,v=x-g['xMm'],y-g['yMm']
    return px+u*math.cos(theta)-v*math.sin(theta),py+u*math.sin(theta)+v*math.cos(theta)
def draw(ax,a):
    global current;current=a
    d=data[a];m=d['metrics'];bb=m['naturalBodyBoundingBoxMm'];board=m['recommendedBoardEnvelopeMm']
    ax.add_patch(Rectangle((board[0],board[1]),board[2]-board[0],board[3]-board[1],facecolor='#f5f7f5',edgecolor='#9aaca0',linewidth=1,linestyle='--',zorder=0))
    for r,g in G.items():
        pos=d['positions'][r];poly=body(r,pos);color=COLORS[d['regionMembership'][r]]
        for part in getattr(poly,'geoms',[poly]):
            ax.add_patch(PatchPolygon(list(part.exterior.coords),facecolor=color,edgecolor='#202a2a',linewidth=.5,zorder=3,alpha=.82))
        for p in g['pads']:
            x,y=newxy(r,p['xMm'],p['yMm']);sh=p['shape'];angle=p['rotation']+pos[2]-g['rotation']
            if sh[0]=='POLYGON':
                v=[v for v in sh[1] if isinstance(v,(float,int))]
                points=[newxy(r,v[i]*.0254,v[i+1]*.0254)for i in range(0,len(v),2)]
                patch=PatchPolygon(points,facecolor='#c0ad6e',edgecolor='#7d713e',linewidth=.25,zorder=2)
            else:
                w,h=sh[1]*.0254,sh[2]*.0254
                if sh[0]=='ELLIPSE':patch=Ellipse((x,y),w,h,angle=angle,facecolor='#c0ad6e',edgecolor='#7d713e',linewidth=.25,zorder=2)
                elif sh[0]=='OVAL':
                    patch=FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle=f'round,pad=0,rounding_size={min(w,h)/2}',facecolor='#c0ad6e',edgecolor='#7d713e',linewidth=.25,zorder=2)
                    patch.set_transform(Affine2D().rotate_deg_around(x,y,angle)+ax.transData)
                else:patch=Rectangle((x-w/2,y-h/2),w,h,angle=angle,rotation_point='center',facecolor='#c0ad6e',edgecolor='#7d713e',linewidth=.25,zorder=2)
            ax.add_patch(patch)
        if (r.startswith(('U','J'))and'_'not in r):
            ax.text(pos[0],pos[1],r,fontsize=7,weight='bold',color='white',ha='center',va='center',zorder=4)
        if r=='J2':
            p=next(p for p in g['pads']if p['number']=='1');x,y=newxy(r,p['xMm'],p['yMm'])
            ax.plot(x,y,'o',color='#c62828',markersize=3,zorder=5)
    # Distinguish actual physical pads from conservative manufacturer-body
    # planning bound. Hatched operating area is free air/access, not PCB material.
    j=d['positions']['J2'];mouth=j[0]-5.5
    ax.add_patch(Rectangle((mouth-10,j[1]-8.7),10,17.4,fill=False,edgecolor='#3a8d93',linestyle=':',hatch='///',linewidth=.8,zorder=1))
    ax.annotate('FFC 插入 →',xy=(mouth+.2,j[1]),xytext=(mouth-8,j[1]),fontproperties=FONT,fontsize=8,arrowprops={'arrowstyle':'->','color':'#247f87'},color='#247f87',va='center',ha='right')
    ax.text(mouth-9,j[1]+11,'8P / 1mm\n官方尺寸保守包络',fontproperties=FONT,fontsize=7,color='#247f87',ha='center')
    ax.add_patch(Rectangle((bb[0],bb[1]),bb[2]-bb[0],bb[3]-bb[1],fill=False,edgecolor='#263e35',linewidth=1.2,linestyle='-.'))
    ax.set_xlim(mouth-27,board[2]+4);ax.set_ylim(board[1]-3,board[3]+5);ax.set_aspect('equal')
    ax.set_xlabel('x / mm');ax.set_ylabel('y / mm')
    ax.set_title(('A：功能/操作优先'if a=='A'else'B：矩形规整/视觉平衡')+f'\n器件自然包络 {m["naturalWidthMm"]:.1f} × {m["naturalHeightMm"]:.1f} mm',fontproperties=FONT,fontsize=14,pad=14)
    ax.grid(alpha=.12,linewidth=.4)
    handles=[Rectangle((0,0),1,1,facecolor=COLORS[n],label=NAMES[n])for n in COLORS]
    ax.legend(handles=handles,prop=FONT,ncol=3,fontsize=8,loc='upper center',bbox_to_anchor=(.5,-.10),frameon=False)
    # Right-edge connectors retained as vertical rows; access from above
    # is schematic only because exact mating housing remains unspecified.
    for jref in ('J3','J4'):
        x,y,_=d['positions'][jref]
        ax.annotate('SWD'if jref=='J3'else'UART',xy=(x,y),xytext=(x+3.7,y),fontsize=7,color='#2e7277',ha='left',va='center')

for a in'AB':
    reserve('finalImageExports',1,'Final no-copper candidate '+a)
    fig,ax=plt.subplots(figsize=(10,9),dpi=180)
    draw(ax,a)
    fig.suptitle('纯器件布局候选 · 实际PCB未修改',fontproperties=FONT,fontsize=17,y=.99)
    fig.text(.5,.025,'实体外形来源：原生 component-shape；FFC为官方尺寸保守包络。虚线是建议轮廓，不是最终板框。\n本图不含走线/过孔/覆铜；机械装配、实际布线与原生DRC仍待后续。',fontproperties=FONT,fontsize=8,ha='center')
    fig.subplots_adjust(top=.86,bottom=.17,left=.09,right=.95)
    fig.savefig(P/('PLACEMENT_'+a+'_NO_COPPER.png'));plt.close(fig)
reserve('finalImageExports',1,'Final A/B comparison of the same two approved candidates')
fig,axes=plt.subplots(1,2,figsize=(20,10),dpi=170)
for ax,a in zip(axes,'AB'):draw(ax,a)
fig.suptitle('先选器件布局，再定最终板框，最后布线',fontproperties=FONT,fontsize=21,y=.99)
fig.text(.5,.03,'两套均含176器件真实尺度、552焊盘；74组关键pin–passive距离保持。\n不包含trace/via/pour；图纸只供布局选择，未执行CAD、原生DRC或制造放行。',fontproperties=FONT,fontsize=11,ha='center')
fig.subplots_adjust(top=.86,bottom=.18,wspace=.12,left=.05,right=.97)
fig.savefig(P/'PLACEMENT_AB_COMPARISON.png');plt.close(fig)
print('Final three user-review placement images exported; CAD=0')
