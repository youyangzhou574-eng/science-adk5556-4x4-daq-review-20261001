import pathlib,json,zipfile
p=pathlib.Path(__file__).parent;z=zipfile.ZipFile(p.parent/"R21_PCB_LOCAL_POUR_CLEARANCE_AND_FINAL_WARM_COLD_V1"/"SCIENCE_ADK5556_4X4_R21_PCB_CLOSED_REVIEW.epro2")
raw=z.read(next(n for n in z.namelist() if n.endswith(".epru"))).decode("utf8")
active=None; wanted={"389528125cb39182","87b2e6ab0bf2243f","54b100f56e34bff6","805f84989d4eb67b","9c03f5c4cb2f3661","6e95b9266e8dd13f"}
for ln in raw.splitlines():
 if "||" not in ln:continue
 try:h,q=ln.split("||",1);h=json.loads(h);q=json.loads(q.rstrip("|"))
 except:continue
 if h["type"]=="DOCHEAD":
  active=q.get("uuid") if q.get("docType")=="FOOTPRINT" else None
  if active in wanted:print("DOCHEAD",q)
 if active in wanted and h["type"] in ["PAD","CANVAS"]:print(active,h["type"],q)

