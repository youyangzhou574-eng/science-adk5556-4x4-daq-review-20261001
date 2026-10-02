import json,pathlib,collections,csv
p=pathlib.Path(r"E:\open\SCIENCE_ADK5556_4X4_DAQ_REPLICA\R21_PCB_LOCAL_POUR_CLEARANCE_AND_FINAL_WARM_COLD_V1")
a=json.loads((p/"COLD_CAPTURE_AND_NATIVE.json").read_text(encoding="utf-8"))["parsed"]["value"]["capture"]
print("CAPTURE_KEYS",list(a))
print("RULES",json.dumps(a["rules"],ensure_ascii=False)[:3500])
print("PARTS_SELECTED")
for c in a["parts"]:
 if c["ref"] in ["U1","U2","U3","U4","U5","U6","U7","U8","U9","U10","U11","J1","J2","J3","J4","D1","D_TIA0"]:
  print(json.dumps(c,ensure_ascii=False)[:1400])
seen=set()
for ln in a["source"].splitlines():
 if "||" not in ln:continue
 h,q=ln.split("||",1)
 try:h=json.loads(h);q=json.loads(q.rstrip("|"))
 except:continue
 k=h["type"]
 if k not in seen and k in ["LINE","VIA","POUR","POURED","POLY","PAD","COMPONENT","ATTR","TEXT"]:print("RECORD",k,json.dumps(q,ensure_ascii=False)[:1500]);seen.add(k)
