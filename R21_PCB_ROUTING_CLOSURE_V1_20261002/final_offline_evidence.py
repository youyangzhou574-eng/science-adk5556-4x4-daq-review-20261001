import pathlib,json,zipfile,csv,collections,hashlib,math,datetime
from shapely.geometry import Polygon,Point,LineString
from shapely.ops import unary_union
P=pathlib.Path(__file__).parent
native=P/'SCIENCE_ADK5556_4X4_R21_PCB_ROUTED_REVIEW.epro2'
with zipfile.ZipFile(native)as z:text=z.read('SCIENCE_ADK5556_4X4_R21_ROUTING_CLOSURE_WORK.epru').decode('utf8')
source=[];records=[];inpcb=False
for ln in text.splitlines():
 if '||'not in ln:continue
 a,b=ln.split('||',1)
 try:h=json.loads(a);j=json.loads(b.rstrip('|'))
 except ValueError:continue
 if h['type']=='DOCHEAD':inpcb=j.get('docType')=='PCB'and j.get('uuid')=='268e6597399ebcce'
 if inpcb:source.append(ln);records.append((h,j))
assert records
(P/'FINAL_PCB_DOCUMENT_FROM_NATIVE_FILE.txt').write_text('\n'.join(source)+'\n','utf8')
start=json.loads((P/'START_CAPTURE.json').read_text('utf8'))['parsed']['value'];warm=json.loads((P/'WARM_CAPTURE.json').read_text('utf8'))['parsed']['value']
sk={c['ref']:c for c in start['parts']};wk={c['ref']:c for c in warm['parts']};assert set(sk)==set(wk)
rows=[];identity=[]
for ref,c in wk.items():
 a=sk[ref];ap={p['number']:p for p in a['pads']};bp={p['number']:p for p in c['pads']};assert set(ap)==set(bp)
 for num,p in bp.items():rows.append({'ref':ref,'pad':num,'net':p['net'],'beforeNet':ap[num]['net'],'PASS':p['net']==ap[num]['net'],'xMil':p['x'],'yMil':p['y']})
 # UI/library metadata carries old names; compare full actual identity fields.
 identity.append({'ref':ref,'PASS':all(a[k]==c[k]for k in('name','footprint','device','uniqueId','manufacturerId','props')),'movedOrRotated':any(a[k]!=c[k]for k in('x','y','rotation'))})
assert all(r['PASS']for r in rows+identity)
def csvout(name,rows):
 with(P/name).open('w',encoding='utf8',newline='')as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
csvout('ALL_550_PAD_NET_IDENTITY.csv',rows);csvout('ALL_176_COMPONENT_IDENTITY.csv',identity)
lines=[dict(id=h['id'],**b)for h,b in records if h['type']=='LINE'];vias=[dict(id=h['id'],**b)for h,b in records if h['type']=='VIA'];pours=[dict(id=h['id'],**b)for h,b in records if h['type']=='POUR'];filled=[(h,b)for h,b in records if h['type']=='POURED']
csvout('ACTUAL_ROUTED_SEGMENTS.csv',[{k:q.get(k)for k in('id','netName','layerId','startX','startY','endX','endY','width')}for q in lines]);csvout('ACTUAL_VIAS.csv',[{k:q.get(k)for k in('id','netName','centerX','centerY','holeDiameter','viaDiameter')}for q in vias])
def points(path):
 x,y=path[:2];out=[(x*10,y*10)];i=2;mode='L'
 while i<len(path):
  if isinstance(path[i],str):mode=path[i];i+=1;continue
  if mode=='ARC':
   ang,nx,ny=path[i:i+3];i+=3;theta=math.radians(ang);dx,dy=nx-x,ny-y
   if abs(math.sin(theta/2))>1e-10:
    cx=(x+nx)/2-dy/(2*math.tan(theta/2));cy=(y+ny)/2+dx/(2*math.tan(theta/2));sx,sy=x-cx,y-cy
    for k in range(1,max(4,int(abs(ang)/8))+1):
     t=theta*k/max(4,int(abs(ang)/8));out.append(((cx+sx*math.cos(t)-sy*math.sin(t))*10,(cy+sx*math.sin(t)+sy*math.cos(t))*10))
   else:out.append((nx*10,ny*10))
   x,y=nx,ny;mode='L'
  else:
   x,y=path[i:i+2];i+=2;out.append((x*10,y*10))
 return out
polys=[];fillmeta=[]
arcSteps=[]
for h,b in filled:
 arcSteps=[]
 pid=json.loads(h['id'])[1];boundary=next(q for q in pours if q['id']==pid);chunks=[]
 for fill in b['pourFill']:
  if not fill.get('fill'):continue
  paths=fill['path'];paths=paths if isinstance(paths[0],list)else[paths]
  if not paths:continue
  for path in paths:
   for i,q in enumerate(path):
    if q=='ARC':arcSteps.append(abs(path[i+1])/max(4,int(abs(path[i+1])/8)))
  rings=[points(path)for path in paths]
  poly=Polygon(rings[0],rings[1:])
  if not poly.is_valid:poly=poly.buffer(0)
  chunks.append(poly)
 geom=unary_union(chunks);polys.append((boundary,geom))
 comps=len(geom.geoms)if geom.geom_type=='MultiPolygon'else 1
 fillmeta.append({'net':boundary['netName'],'layer':boundary['layerId'],'filledCopperComponents':comps,'areaMM2':geom.area*.0254**2,'arcApproximationMaxDegrees':max(arcSteps),'scope':'offline native filled geometry, not final electrical DRC or manufacturing certificate'})
csvout('ACTUAL_FILL_GEOMETRY_REVIEW.csv',fillmeta)
summary={'parts':len(wk),'pads':len(rows),'assigned':sum(bool(r['net'])for r in rows),'nets':len({r['net']for r in rows if r['net']}),'NC':sum(not r['net']for r in rows),'padNetIdentity':'PASS warm actual550 vs start','componentCoreIdentity':'PASS176','lines':len(lines),'vias':len(vias),'pourBoundaries':len(pours),'actualFilledPours':len(filled),'layerLineCounts':dict(collections.Counter(q['layerId']for q in lines)),'fillGeometry':fillmeta,'nativeSHA256':hashlib.sha256(native.read_bytes()).hexdigest().upper(),'finalElectricalDRC':'NOT_COMPLETED','lastSuccessfulDRC':'TARGETED_DRC:8 ConnectionError before final15 bridges','coldActualPadAudit':'FAILED_NULL_PINS','coldNativeDRC':'FAILED_NO_CANVAS_SUBSCRIPTION','PCB_REVIEW_READY':False,'MANUFACTURING_NOT_RELEASED':True,'noFurtherNativeMutation':True}
(P/'FINAL_EVIDENCE_SUMMARY.json').write_text(json.dumps(summary,indent=2),'utf8')
print(json.dumps(summary))
