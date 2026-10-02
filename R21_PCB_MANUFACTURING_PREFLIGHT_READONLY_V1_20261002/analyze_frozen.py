import pathlib,json,zipfile,math,csv,collections,re,itertools
from shapely.geometry import Point,box,Polygon,LineString
from shapely import affinity
p=pathlib.Path(__file__).parent;o=p.parent/"R21_PCB_LOCAL_POUR_CLEARANCE_AND_FINAL_WARM_COLD_V1"
a=json.loads((o/"COLD_CAPTURE_AND_NATIVE.json").read_text(encoding="utf8"))["parsed"]["value"]["capture"]
net=json.loads(a["netlist"])
def rec(raw):
 out=[]
 for ln in raw.splitlines():
  if "||" not in ln:continue
  try:h,q=ln.split("||",1);out.append((json.loads(h),json.loads(q.rstrip("|"))))
  except ValueError:continue
 return out
rs=rec(a["source"])
z=zipfile.ZipFile(o/"SCIENCE_ADK5556_4X4_R21_PCB_CLOSED_REVIEW.epro2")
raw=z.read(next(n for n in z.namelist()if n.endswith(".epru"))).decode("utf8")
docs={};active=None
for h,q in rec(raw):
 if h["type"]=="DOCHEAD":active=q.get("uuid")if q.get("docType")=="FOOTPRINT"else None
 if active:docs.setdefault(active,[]).append({"header":h,"body":q})
(p/"FROZEN_FOOTPRINT_RECORDS.json").write_text(json.dumps(docs,ensure_ascii=False,indent=2),encoding="utf8")
rules=a["rules"];(p/"FROZEN_RULES.json").write_text(json.dumps(rules,ensure_ascii=False,indent=2),encoding="utf8")
parts={c["ref"]:c for c in a["parts"]};pads=[];bom=[];checks=[];holes=[];geoms={}
for c in a["parts"]:
 fp=docs[c["footprint"]["uuid"]];fpads={r["body"]["num"]:r["body"]for r in fp if r["header"]["type"]=="PAD"}
 props=net["components"][c["uniqueId"]]["props"]
 bom.append({"Designator":c["ref"],"Manufacturer":props.get("Manufacturer",""),"ManufacturerPartNumber":c["manufacturerId"]or props.get("Manufacturer Part",""),"Value":props.get("Value",props.get("Name","")),"Footprint":c["footprint"]["name"],"Quantity":1,"x_mm":c["x"]*.0254,"y_mm":c["y"]*.0254,"rotation_deg":c["rotation"],"missingMPN":not bool(c["manufacturerId"]or props.get("Manufacturer Part",""))})
 checks.append({"ref":c["ref"],"footprintUUID":c["footprint"]["uuid"],"nativePadNumbers":sorted(fpads),"actualPadNumbers":sorted(x["number"]for x in c["pads"]),"padNumbersMatch":set(fpads)=={x["number"]for x in c["pads"]},"padCount":len(fpads),"nativeDrillPads":sum(r["hole"]is not None for r in fpads.values()),"topLayer":c["layer"]==1})
 for d in c["pads"]:
  fd=fpads[d["number"]];sh=d["pad"];x,y=d["x"]*.0254,d["y"]*.0254
  if sh[0]=="POLYGON":
   path=sh[1];pts=[];k=0
   while k<len(path):
    if isinstance(path[k],str):k+=1;continue
    pts.append((path[k]*.0254,path[k+1]*.0254));k+=2
   g=Polygon(pts)
  else:
   w,ht=sh[1]*.0254,sh[2]*.0254
   if sh[0]=="ELLIPSE":g=affinity.scale(Point(0,0).buffer(1,resolution=24),w/2,ht/2)
   else:g=box(-w/2,-ht/2,w/2,ht/2)
   g=affinity.rotate(g,d["rotation"],origin=(0,0));g=affinity.translate(g,x,y)
  geoms[(c["ref"],d["number"])]=g
  hole=fd["hole"];dr=hole["width"]*.0254 if hole else None
  if dr:holes.append((c["ref"]+"."+d["number"],x,y,dr))
  exp=fd["topSolderExpansion"]*.0254 if fd["topSolderExpansion"]is not None else .0508
  pads.append({"ref":c["ref"],"pad":d["number"],"net":d["net"],"x_mm":x,"y_mm":y,"rotation_deg":d["rotation"],"shape":sh[0],"nativeHole_mm":dr,"nativeHole_raw_mil":hole["width"]if hole else None,"API_hole_retained":json.dumps(d["hole"]),"maskExpansion_mm":exp,"pitchAuthority":"native package record and actual pad centers","nativeLayer":fd["layerId"],"footprintUUID":c["footprint"]["uuid"]})
def csvwrite(name,rows):
 with(p/name).open("w",encoding="utf8",newline="")as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
csvwrite("FROZEN_176_MANUFACTURING_BOM.csv",bom);csvwrite("FROZEN_550_PAD_GEOMETRY.csv",pads)
(p/"PAD_NUMBER_COVERAGE.json").write_text(json.dumps(checks,indent=2),encoding="utf8")
lines=[dict(id=h["id"],**q)for h,q in rs if h["type"]=="LINE"];vias=[dict(id=h["id"],**q)for h,q in rs if h["type"]=="VIA"];pours=[dict(id=h["id"],**q)for h,q in rs if h["type"]=="POUR"]
B=box(0,0,3937.0079*.0254,3543.3071*.0254)
viaedge=min(min(q["centerX"]*.0254-q["viaDiameter"]*.0254/2,q["centerY"]*.0254-q["viaDiameter"]*.0254/2,B.bounds[2]-q["centerX"]*.0254-q["viaDiameter"]*.0254/2,B.bounds[3]-q["centerY"]*.0254-q["viaDiameter"]*.0254/2)for q in vias)
trackedge=min(min(q["startX"],q["endX"],q["startY"],q["endY"],3937.0079-q["startX"],3937.0079-q["endX"],3543.3071-q["startY"],3543.3071-q["endY"])-q["width"]/2 for q in lines)*.0254
padedge=min(g.distance(B.boundary)if B.contains(g)else 0 for g in geoms.values())
for q in vias:holes.append((q["id"],q["centerX"]*.0254,q["centerY"]*.0254,q["holeDiameter"]*.0254))
hp=min(({"a":x[0],"b":y[0],"clearance_mm":math.hypot(x[1]-y[1],x[2]-y[2])-(x[3]+y[3])/2}for x,y in itertools.combinations(holes,2)),key=lambda q:q["clearance_mm"])
mask=[]
for c in a["parts"]:
 for d,e in itertools.combinations(c["pads"],2):
  gd,ge=geoms[(c["ref"],d["number"])],geoms[(c["ref"],e["number"])]
  fd=next(q for q in pads if q["ref"]==c["ref"]and q["pad"]==d["number"]);fe=next(q for q in pads if q["ref"]==c["ref"]and q["pad"]==e["number"])
  gap=gd.distance(ge);mask.append({"ref":c["ref"],"padA":d["number"],"padB":e["number"],"copperGap_mm":gap,"estimatedMaskBridge_mm":gap-fd["maskExpansion_mm"]-fe["maskExpansion_mm"],"scope":"same-package local copper and existing mask expansions; rounded actual centers; not rendered Gerber or complete fab DFM"})
mask.sort(key=lambda q:q["estimatedMaskBridge_mm"]);csvwrite("SAME_PACKAGE_MASK_GAPS.csv",mask)
core=["U1","U2","U3","U4","U5","U7","U9","U10","U11","U12","D_TIA0","J1","J2","J3","J4"]
cs=[]
for ref in core:
 c=parts[ref];pd=c["pads"];dist=sorted({round(math.hypot(x["x"]-y["x"],x["y"]-y["y"])*.0254,6)for x,y in itertools.combinations(pd,2)if x["number"]!=y["number"]})
 cs.append({"ref":ref,"MPN":c["manufacturerId"],"footprint":c["footprint"]["name"],"padCount":len(pd),"rotation_deg":c["rotation"],"minimumCenterDistance_mm":dist[0],"pin1_x_mm":next(x for x in pads if x["ref"]==ref and x["pad"]=="1")["x_mm"],"pin1_y_mm":next(x for x in pads if x["ref"]==ref and x["pad"]=="1")["y_mm"],"nativeHoleWidths_mm":sorted({x["nativeHole_mm"]for x in pads if x["ref"]==ref and x["nativeHole_mm"]is not None}),"smallestSamePackageMaskBridge_mm":min(x["estimatedMaskBridge_mm"]for x in mask if x["ref"]==ref)})
(p/"CORE_PACKAGE_GEOMETRY.json").write_text(json.dumps(cs,ensure_ascii=False,indent=2),encoding="utf8")
summary={"parts":len(parts),"pads":len(pads),"padNumberCoveragePASS":all(x["padNumbersMatch"]for x in checks),"allTop":all(x["topLayer"]for x in checks),"board_mm":[3937.0079*.0254,3543.3071*.0254],"lineWidthsMil":dict(collections.Counter(q["width"]for q in lines)),"viaDimensionsMil":dict(collections.Counter(str([q["holeDiameter"],q["viaDiameter"]])for q in vias)),"viaRing_mm":min((q["viaDiameter"]-q["holeDiameter"])*.0254/2 for q in vias),"minViaCopperToBoard_mm":viaedge,"minTrackCopperToBoard_mm":trackedge,"minPadCopperToBoard_mm":padedge,"minimumHolePair":hp,"POUR":pours,"globalMaskExpansion_mm":.0508,"API_hole_discrepancy":"Header native hole widths43.308/39.37/47.244 mil vs API4.3308/3.937/4.7244; LM polygon nativeholeNone vs APIderivedhole nonzero. Native hole object is authority; no manufacturing defect concluded from API hole field.","missingMPNRefs":[q["Designator"]for q in bom if q["missingMPN"]],"manufacturingRelease":False}
(p/"GEOMETRY_SUMMARY.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf8")
print(json.dumps(summary,ensure_ascii=False));print("CORE",json.dumps(cs,ensure_ascii=False))

