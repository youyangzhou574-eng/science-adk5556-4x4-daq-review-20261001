import pathlib,json
p=pathlib.Path(__file__).parent;ds=json.loads((p/"FROZEN_FOOTPRINT_RECORDS.json").read_text())
for u in ["b6beb3a5f30c65ef","8a281445258384ed","e13794d22038af93","9c03f5c4cb2f3661","389528125cb39182"]:
 print(u,[r["body"] for r in ds[u]if r["header"]["type"]=="POLY"and r["body"].get("layerId")==48])

