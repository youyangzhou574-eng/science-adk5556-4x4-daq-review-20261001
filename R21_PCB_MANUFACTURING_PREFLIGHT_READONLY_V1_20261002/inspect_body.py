import pathlib,json
p=pathlib.Path(__file__).parent;ds=json.loads((p/"FROZEN_FOOTPRINT_RECORDS.json").read_text())
for u in ["b6beb3a5f30c65ef","8a281445258384ed","e13794d22038af93","9c03f5c4cb2f3661","6e95b9266e8dd13f"]:
 print("FP",u)
 for r in ds[u]:
  q=r["body"]
  if r["header"]["type"]=="FILL"and q.get("layerId") in [49,50]:print(r["header"]["type"],q)

