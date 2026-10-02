import pathlib,json,zipfile,collections
p=pathlib.Path(__file__).parent;o=p.parent/"R21_PCB_LOCAL_POUR_CLEARANCE_AND_FINAL_WARM_COLD_V1";a=json.loads((o/"COLD_CAPTURE_AND_NATIVE.json").read_text(encoding="utf8"))["parsed"]["value"]["capture"]
def visit(v,path=""):
 if isinstance(v,dict):
  for k,x in v.items():
   if any(s in k.lower() for s in ["solder","mask","paste","edge","island","annular","ring","hole","drill","silk"]):print("RULE",path+"/"+k,str(x)[:1100])
   visit(x,path+"/"+k)
visit(a["rules"])
n=json.loads(a["netlist"])
print("NETKEYS",list(n))
print("COMPSAMPLE",json.dumps(n.get("components",{}).get("gge82",{}),ensure_ascii=False)[:1800])
z=zipfile.ZipFile(o/"SCIENCE_ADK5556_4X4_R21_PCB_CLOSED_REVIEW.epro2");raw=z.read(next(n for n in z.namelist()if n.endswith(".epru"))).decode("utf8");active=False;counts=collections.Counter()
for ln in raw.splitlines():
 if "||" not in ln:continue
 try:h,q=ln.split("||",1);h=json.loads(h);q=json.loads(q.rstrip("|"))
 except:continue
 if h["type"]=="DOCHEAD":active=q.get("docType")=="FOOTPRINT"
 if active:counts[(h["type"],q.get("layerId"))]+=1
print("FPCOUNTS",str(counts))
