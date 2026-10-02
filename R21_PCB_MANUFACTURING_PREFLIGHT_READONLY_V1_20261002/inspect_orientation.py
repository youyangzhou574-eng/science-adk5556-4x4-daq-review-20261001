import pathlib,json
p=pathlib.Path(__file__).parent;a=json.loads((p.parent/"R21_PCB_LOCAL_POUR_CLEARANCE_AND_FINAL_WARM_COLD_V1"/"COLD_CAPTURE_AND_NATIVE.json").read_text(encoding="utf8"))["parsed"]["value"]["capture"];f=json.loads((p/"FROZEN_FOOTPRINT_RECORDS.json").read_text())
for ref in ["U5","U9","U11"]:
 c=next(c for c in a["parts"]if c["ref"]==ref)
 for pad in c["pads"][:3]:
  q=next(r["body"]for r in f[c["footprint"]["uuid"]]if r["header"]["type"]=="PAD"and r["body"]["num"]==pad["number"])
  print(ref,pad["number"],"APIrotation",pad["rotation"],"shape",str(pad["pad"])[:80],"nativecenter",q["centerX"],q["centerY"],"angles",q["padAngle"],q["relativeAngle"],"default",str(q["defaultPad"])[:120])

