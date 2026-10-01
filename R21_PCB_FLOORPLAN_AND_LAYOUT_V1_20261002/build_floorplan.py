import pathlib,json,math,re,csv
P=pathlib.Path(__file__).resolve().parent
cap=json.loads((P/'PCB_PAD_AUDIT_01.json').read_text('utf8'))['parsed']['value'];actual={a['ref']:a for a in cap['parts']};plan={a['ref']:a for a in json.loads((P/'PCB_COMPONENT_PLAN.json').read_text('utf8'))}
def local_box(c):
 xs=[];ys=[]
 for p in c['pads']:
  sh=p['pad'];ang=math.radians(p['rotation'])
  if sh[0]=='POLYGON':
   coords=[v for v in sh[1]if isinstance(v,(int,float))];xx=coords[::2];yy=coords[1::2]
   xs+=xx;ys+=yy
  else:
   w,h=sh[1:3];hx=(abs(math.cos(ang))*w+abs(math.sin(ang))*h)/2;hy=(abs(math.sin(ang))*w+abs(math.cos(ang))*h)/2
   xs +=[p['x']-hx,p['x']+hx];ys +=[p['y']-hy,p['y']+hy]
 return [(min(xs)-c['x'])*.0254,(min(ys)-c['y'])*.0254,(max(xs)-c['x'])*.0254,(max(ys)-c['y'])*.0254]
boxes={r:local_box(a) for r,a in actual.items()}
def box(r,x,y,rot):
 b=boxes[r];rad=math.radians(rot);points=[(u*math.cos(rad)-v*math.sin(rad),u*math.sin(rad)+v*math.cos(rad))for u in [b[0],b[2]]for v in [b[1],b[3]]]
 margin=.35
 return (x+min(p[0]for p in points)-margin,y+min(p[1]for p in points)-margin,x+max(p[0]for p in points)+margin,y+max(p[1]for p in points)+margin)
placed={};occupied={};notes={}
def fits(b):
 if b[0]<1.5 or b[1]<1.5 or b[2]>98.5 or b[3]>88.5:return False
 return all(b[2]<o[0] or b[0]>o[2] or b[3]<o[1] or b[1]>o[3]for o in occupied.values())
def place(r,x,y,rot=0,role='',search=False):
 if r in placed:raise RuntimeError('duplicate '+r)
 original=(x,y,rot)
 candidates=[(x,y,rot)]
 if search:
  # Local collision avoidance within a manually selected functional cluster, not EDA auto-placement.
  offsets=[(dx*.5,dy*.5)for dx in range(-22,23)for dy in range(-22,23)]
  offsets.sort(key=lambda z:z[0]**2+z[1]**2)
  candidates +=[(x+dx,y+dy,ro)for dx,dy in offsets for ro in (rot,(rot+90)%360)]
 for xx,yy,ro in candidates:
  b=box(r,xx,yy,ro)
  if fits(b):
   placed[r]={'ref':r,'x_mm':xx,'y_mm':yy,'rotation':ro,'x':xx/.0254,'y':yy/.0254};occupied[r]=b;notes[r]={'role':role,'requested_mm':original[:2],'actual_mm':[xx,yy],'displacement_mm':math.hypot(xx-x,yy-y),'envelope_mm':b};return
 raise RuntimeError('No room in chosen cluster '+r)
cores={'J2':(5,39,90),'J1':(7,81,90),'J3':(94,18,90),'J4':(94,73,90),'U1':(27,21,0),'U2':(28,53,0),'U3':(52,20,0),'U4':(44,35,0),'U5':(52,53,180),'U6':(59,13,0),'U7':(82,53,0),'U8':(45,81,0),'U9':(21,81,0),'U10':(58,81,0),'U11':(74,78,0),'U12':(84,78,0),'U13':(71,36,0),'U14':(61,36,0),'U15':(73,68,0)}
for r,(x,y,rot)in cores.items():place(r,x,y,rot,'Manual signal-chain/power/interface floorplan')
for core,group in [('U1','ROW'),('U2','TIA')]:
 cx,cy,_=cores[core]
 for i,(sgx,sgy)in enumerate([(-1,-1),(1,-1),(1,1),(-1,1)]):
  if group=='ROW':names=[(f'C_ROW_HF{i}',3.175,5),(f'R_ISO{i}',4.8,7.8),(f'R_ROW_FB{i}',1.4,7.8),(f'D_ROW{i}',7.4,5)]
  else:names=[(f'C_TIA_HF{i}',3.175,5),(f'R_TIA_ISO{i}',4.8,7.8),(f'R_COL_SENSE{i}',1.4,7.8),(f'RF{i}',4.8,10.5),(f'CF{i}',1.4,10.5),(f'D_TIA{i}',7.4,5)]
  for r,dx,dy in names:place(r,cx+sgx*dx,cy+sgy*dy,0,'Local '+group+' feedback/compensation channel '+str(i),True)
# Reference and ADC capacitors are assigned to physical pin neighborhoods, not merely common nets.
anchors={
 'C_ROW_OP':(27,15.2,0),'C_TIA_OP':(28,47.2,0),'C_MUX':(44,31,0),'C_BUF':(49,24.5,0),'C_REF':(59,16,0),'C_MCU1':(82,47.8,0),'C_MCU_BULK':(86,47,0),'C_U13':(71,31.5,0),'C_U14':(61,31.5,0),'C_U15':(73,71,0),
 'C_VCM_HF':(50.73,15,0),'R_VCM_ISO':(47.5,13,0),'R_VCM_FB':(50.5,11,0),'D_VCM':(45,15,0),
 'C_VEX_HF':(52,25,0),'R_VEX_ISO':(48,28,0),'R_VEX_FB':(52,29,0),'D_VEX':(46,25,0),
 'C_ADC0':(49,61,0),'R_ADC0':(45.5,64,0),'C_ADC1':(45.5,61,0),'R_ADC1':(42,61,0),'C_ADC2':(45.5,45,0),'R_ADC2':(42,45,0),'C_ADC3':(49,45,0),'R_ADC3':(45.5,42,0),
 'C_ADC_REFIO':(57.5,58,0),'C_REFIO_B':(62,58,0),'C_ADC_REFCAP':(54.5,61,0),'C_REFCAP_BULKA':(57.5,64,0),'C_REFCAP_BULKB':(62,64,0),
 'C_AVDD9_HF':(52.5,58.5,90),'C_AVDD30_HF':(52.5,47,90),'C_DVDD34A':(57.5,47,0),'C_DVDD34B':(61,47,0),
 'C_AVDD9A':(54,66.5,0),'C_AVDD9B':(57.5,69,0),'C_AVDD30A':(54,42,0),'C_AVDD30B':(57.5,40,0),'C_ADCA1':(61,42,0),'C_ADCA2':(61,69,0),'C_ADCD':(61,50,0),
 'C_LDO_IN':(42,81,90),'C_LDO_OUT':(48,81,90),'C_PWR':(13,81,0),'U9_IN_CAP':(17,84,0),'U9_OUT_CAP':(25,84,0),'U10_IN_CAP':(55,84,0),'U10_OUT_CAP':(62,84,0),
 'R_RST':(79,70,0),'C_RST':(82,70,0),'R_CS_PU':(74,51,0),'R_ADC_RESET_PD':(67,50,0),'C_DIV':(56,29,0)}
for r,(x,y,rot)in anchors.items():place(r,x,y,rot,'Curated local supply/reference/ADC/control placement',True)
for r in sorted(plan):
 if r in placed:continue
 if r.startswith('RD_'):anchor=(58,23)
 elif r.startswith('U9_'):anchor=(21,76)
 elif r.startswith('U10_'):anchor=(58,76)
 elif r.startswith('U11_'):anchor=(74,81)
 elif r.startswith('U12_'):anchor=(84,81)
 elif '_J3_'in r:anchor=(87,18)
 elif '_J4_'in r:anchor=(87,73)
 elif r.startswith('R_SEL_PD'):anchor=(44,38)
 elif r in ['R_HW_PD','R_ENABLE_PD']:anchor=(76,36)
 else:raise RuntimeError('No functional cluster '+r)
 place(r,*anchor,0,'Functional cluster: '+str(anchor),True)
assert len(placed)==176
out={'board_mm':[100,90],'mechanical':'Provisional lab rectangle; no enclosure or holes implied','layers':{'1':'L1 components and critical analog','15':'L2 continuous GND no other-net routing','16':'L3 power/slow digital','2':'L4 remaining signals'},'placements':list(placed.values()),'notes':notes,'geometricCheck':'No overlapping conservative PAD envelopes +0.35mm per component; true silk/courtyard/DRC checked later.'}
(P/'FLOORPLAN.json').write_text(json.dumps(out,indent=2),'utf8')
with(P/'PLACEMENT_PLAN.csv').open('w',newline='',encoding='utf8')as f:w=csv.DictWriter(f,fieldnames=list(next(iter(placed.values()))));w.writeheader();w.writerows(placed.values())
code='const p='+json.dumps(out['placements'],separators=(',',':'))+';\n'
code+='''const pr=await eda.dmt_Project.getCurrentProjectInfo();if(pr.uuid!=="e58f223d256cd14d13a6fb04a0e150585301864f01c50827f9241f5945cf2801")throw Error('Wrong copy');await eda.dmt_EditorControl.openDocument('268e6597399ebcce');const all=await eda.pcb_PrimitiveComponent.getAll();if(all.length!==176)throw Error('Count');const byRef=new Map(all.map(c=>[c.getState_Designator(),c]));const moved=[];for(const row of p){const c=byRef.get(row.ref);if(!c)throw Error(row.ref);await eda.pcb_PrimitiveComponent.modify(c,{x:row.x,y:row.y,rotation:row.rotation});moved.push(row.ref);}const w=100/.0254,h=90/.0254;
for(const [x1,y1,x2,y2]of [[0,0,w,0],[w,0,w,h],[w,h,0,h],[0,h,0,0]])if(!await eda.pcb_PrimitiveLine.create('',11,x1,y1,x2,y2,4,false))throw Error('Outline');
return {moved,saved:await eda.pcb_Document.save()};'''
(P/'place_floorplan.js').write_text(code,'utf8')
print(json.dumps({'components':len(placed),'size':out['board_mm'],'largestAdjustment_mm':max(n['displacement_mm']for n in notes.values())}))
