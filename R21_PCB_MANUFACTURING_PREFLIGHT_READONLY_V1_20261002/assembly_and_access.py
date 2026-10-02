import pathlib,json,math,csv,itertools
from shapely.geometry import Polygon,Point,box
from shapely import affinity
import matplotlib;matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Patch
p=pathlib.Path(__file__).parent;o=p.parent/"R21_PCB_LOCAL_POUR_CLEARANCE_AND_FINAL_WARM_COLD_V1"
a=json.loads((o/"COLD_CAPTURE_AND_NATIVE.json").read_text(encoding="utf8"))["parsed"]["value"]["capture"]
ds=json.loads((p/"FROZEN_FOOTPRINT_RECORDS.json").read_text());parts={c["ref"]:c for c in a["parts"]}
def world(c,g):
 g=affinity.rotate(g,c["rotation"],origin=(0,0));return affinity.translate(g,c["x"]*.0254,c["y"]*.0254)
def pathpoly(path):
 if any(isinstance(v,str)and v!="L"for v in path):return None
 v=[q for q in path if not isinstance(q,str)]
 return Polygon([(v[i]*.0254,v[i+1]*.0254)for i in range(0,len(v),2)])
bodies={};marks={};nativeg={};masks={};nativepads=[]
for c in a["parts"]:
 fp=ds[c["footprint"]["uuid"]]
 for r in fp:
  q=r["body"];k=r["header"]["type"]
  if k=="POLY"and q.get("layerId")==48:
   g=pathpoly(q["path"])
   if g is not None:bodies[c["ref"]]=world(c,g)
  if k=="FILL"and q.get("layerId")==49:
   pp=q["path"][0]
   if pp[0]=="CIRCLE":g=world(c,Point(pp[1]*.0254,pp[2]*.0254));marks[c["ref"]]=(g.x,g.y)
  if k=="PAD":
   sh=q["defaultPad"]
   if sh["padType"]=="POLYGON":g=pathpoly(sh["path"])
   else:
    w,h=sh["width"]*.0254,sh["height"]*.0254
    if sh["padType"]=="ELLIPSE":g=affinity.scale(Point(0,0).buffer(1,resolution=24),w/2,h/2)
    else:g=box(-w/2,-h/2,w/2,h/2)
    g=affinity.rotate(g,q["padAngle"],origin=(0,0));g=affinity.translate(g,q["centerX"]*.0254,q["centerY"]*.0254)
   g=world(c,g);key=(c["ref"],q["num"]);nativeg[key]=g
   masks[key]=q["topSolderExpansion"]*.0254 if q["topSolderExpansion"]is not None else .0508
   pp=next(x for x in c["pads"]if x["number"]==q["num"])
   nativepads.append({"ref":c["ref"],"pad":q["num"],"net":pp["net"],"x_mm":g.centroid.x,"y_mm":g.centroid.y,"nativeCopperShape":sh["padType"],"nativeDrill_mm":q["hole"]["width"]*.0254 if q["hole"]else None,"nativeMaskExpansion_mm":masks[key],"nativeLayer":q["layerId"]})
mg=[]
for c in a["parts"]:
 ks=[k for k in nativeg if k[0]==c["ref"]]
 for x,y in itertools.combinations(ks,2):mg.append({"ref":x[0],"padA":x[1],"padB":y[1],"nativeCopperGap_mm":nativeg[x].distance(nativeg[y]),"nativeMaskBridgeEstimate_mm":nativeg[x].distance(nativeg[y])-masks[x]-masks[y],"method":"existing native pad polygon/rect with padAngle and component rotation; ellipse24seg; no Gerber"})
mg.sort(key=lambda q:q["nativeMaskBridgeEstimate_mm"])
def csvwrite(n,rows):
 with(p/n).open("w",encoding="utf8",newline="")as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
csvwrite("NATIVE_SAME_PACKAGE_MASK_GAPS.csv",mg);csvwrite("NATIVE_550_PAD_GEOMETRY.csv",nativepads)
bc=[]
for (x,g),(y,h)in itertools.combinations(bodies.items(),2):
 d=g.distance(h)
 if d<.75:bc.append({"refA":x,"refB":y,"nominalBodyGap_mm":d,"overlapArea_mm2":g.intersection(h).area,"scope":"native component-body outline layer48; not courtyard/full3D/assembly tool keepout"})
bc.sort(key=lambda q:q["nominalBodyGap_mm"]);csvwrite("NOMINAL_BODY_NEAR_PAIRS.csv",bc)
access=[]
targets={"V5_IN":["J1"],"V5":["U9_OUT_CAP","C_ADCA1"],"V3V3":["U10_OUT_CAP","C_MCU1_1"],"REF_2V5":["C_REF","U6"],"VCM":["R_VCM_ISO","R_TIA_SENSE0"],"VEXC":["R_VEXC_ISO","U3"],"PGOOD":["R_RST","R_J3_5"],"ROW0":["J2"],"TIA_DRV0":["RF0","C_TIA0_COMP"],"TIA0":["R_ADC0","R_TIA_ISO0"],"ADC_IN0":["C_ADC0","R_ADC0"],"MCU_NRST_EXT":["J3"],"GND":["J1","J3"]}
for target,prefer in targets.items():
 opts=[x for x in nativepads if x["net"]==target]
 def score(x):
  ref=x["ref"];g=nativeg[(ref,x["pad"])];minsize=min(g.bounds[2]-g.bounds[0],g.bounds[3]-g.bounds[1])
  return (ref not in prefer,not ref.startswith(("J","R","C")), -minsize)
 opts.sort(key=score)
 if opts:
  d=dict(opts[0]);g=nativeg[(d["ref"],d["pad"])];d.update(target=target,padWidthX_mm=g.bounds[2]-g.bounds[0],padWidthY_mm=g.bounds[3]-g.bounds[1],assessment="PASS existing accessible surface pad candidate; actual probe/clips/operator and powered safety PENDING_INPUT")
  access.append(d)
 else:access.append({"target":target,"assessment":"PENDING_INPUT alias/net not present; do not invent test point"})
csvwrite("EXISTING_TEST_ACCESS_CANDIDATES.csv",[{k:r.get(k,"")for k in ["target","ref","pad","net","x_mm","y_mm","padWidthX_mm","padWidthY_mm","nativeDrill_mm","assessment"]}for r in access])
fig,ax=plt.subplots(figsize=(13,11))
for ref,g in bodies.items():
 ax.add_patch(Patch(list(g.exterior.coords),facecolor="#ddd"if ref not in ["U1","U2","U3","U4","U5","U7","U9","U10","U11","U12","J1","J2","J3","J4"]else"#ceddef",edgecolor="#777",lw=.4))
 if ref.startswith("J")or(ref.startswith("U")and ref[1:].isdigit()):ax.text(g.centroid.x,g.centroid.y,ref,ha="center",va="center",fontsize=9)
for key,g in nativeg.items():ax.add_patch(Patch(list(g.exterior.coords),facecolor="#b9a765",edgecolor="none",alpha=.65))
for ref,xy in marks.items():
 if ref.startswith("J")or(ref.startswith("U")and ref[1:].isdigit()):ax.plot(*xy,"r.",ms=5)
for i,r in enumerate(access):
 if "x_mm"in r:
  ax.plot(r["x_mm"],r["y_mm"],"o",mfc="none",mec="#006d63",ms=11)
  ax.annotate(str(i+1),(r["x_mm"],r["y_mm"]),xytext=(5,-12),textcoords="offset points",fontsize=8,color="#006d63")
ax.set_xlim(0,100);ax.set_ylim(90,0);ax.set_aspect("equal");ax.grid(alpha=.2);ax.set_xlabel("x mm");ax.set_ylabel("y mm");ax.set_title("Frozen PCB: native body/pads and existing probe candidates\nRed = native component marking; green index = access CSV; review only, no CAD edits")
fig.tight_layout();fig.savefig(p/"ASSEMBLY_AND_PROBE_REVIEW.png",dpi=150);plt.close(fig)
out={"nativeBodyOutlines":len(bodies),"nominalBodyOverlapPairs":[q for q in bc if q["overlapArea_mm2"]>1e-8],"minimumNominalBodyPair":bc[0],"maskUnder0p1":[q for q in mg if q["nativeMaskBridgeEstimate_mm"]<.1],"maskMinByRef":{ref:min(q["nativeMaskBridgeEstimate_mm"]for q in mg if q["ref"]==ref)for ref in ["U5","U9","U10","U11","U12"]},"testAccessCandidates":len(access),"nativeDrill20PTH":[q for q in nativepads if q["nativeDrill_mm"]is not None],"sourcesReviewed":"6 sources capped; ST direct download567, official web PDF package text accessible. Existing other4 PDFs reuse; no tool install."}
(p/"ASSEMBLY_GEOMETRY_SUMMARY.json").write_text(json.dumps(out,indent=2),encoding="utf8")
print(json.dumps({k:v for k,v in out.items()if k not in["maskUnder0p1","nativeDrill20PTH"]},ensure_ascii=False));print("maskbelow.1",len(out["maskUnder0p1"]))
