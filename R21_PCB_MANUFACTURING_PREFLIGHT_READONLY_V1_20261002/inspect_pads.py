import pathlib,json,zipfile,collections
p=pathlib.Path(__file__).parent;old=p.parent/"R21_PCB_LOCAL_POUR_CLEARANCE_AND_FINAL_WARM_COLD_V1"
a=json.loads((old/"COLD_CAPTURE_AND_NATIVE.json").read_text(encoding="utf8"))["parsed"]["value"]["capture"]
for c in a["parts"]:
 if c["ref"].startswith("U") or c["ref"] in ["J1","J2","J3","J4","D_TIA0"]:
  print(c["ref"],c["manufacturerId"],c["footprint"]["name"],c["x"],c["y"],c["rotation"])
  print([(x["number"],x["net"],x["x"],x["y"],x["pad"],x["hole"])for x in c["pads"]])
z=zipfile.ZipFile(old/"SCIENCE_ADK5556_4X4_R21_PCB_CLOSED_REVIEW.epro2")
print("ZIP first",z.namelist()[:12])
for n in z.namelist():
 if "389528125cb39182" in n or "87b2e6ab0bf2243f" in n:print(n,z.read(n).decode("utf8")[:5000])

