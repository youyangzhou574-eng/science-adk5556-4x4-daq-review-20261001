import pathlib,json
p=pathlib.Path(__file__).parent;o=p.parent/"R21_PCB_LOCAL_POUR_CLEARANCE_AND_FINAL_WARM_COLD_V1";a=json.loads((o/"COLD_CAPTURE_AND_NATIVE.json").read_text(encoding="utf8"))["parsed"]["value"]["capture"]
print("PGOOD",[c["ref"]+"."+d["number"]for c in a["parts"]for d in c["pads"]if d["net"]=="PGOOD"])
d=json.loads((p/"FROZEN_FOOTPRINT_RECORDS.json").read_text())
print("missingBody",[c["ref"]for c in a["parts"]if not any(r["header"]["type"]=="POLY"and r["body"].get("layerId")==48 for r in d[c["footprint"]["uuid"]])])
for r in d["b6beb3a5f30c65ef"]:
 if r["header"]["type"]=="LAYER" and r["body"].get("layerId") in [48,49,50,51]:print(r["body"])
print("POLY3example",[r["body"]for r in d["b6beb3a5f30c65ef"]if r["header"]["type"]=="POLY"and r["body"].get("layerId")==3][:3])

