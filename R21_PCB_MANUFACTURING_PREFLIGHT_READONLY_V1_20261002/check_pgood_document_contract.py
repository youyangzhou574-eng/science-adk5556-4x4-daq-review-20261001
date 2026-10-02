import pathlib,json,csv,hashlib
p=pathlib.Path(__file__).parent
def rows(n):
 with(p/n).open(encoding="utf8")as f:return list(csv.DictReader(f))
r=rows("EXISTING_TEST_ACCESS_CANDIDATES.csv");pg=next(x for x in r if x["target"]=="PGOOD");actual=pg["ref"]+"."+pg["pad"]
paths=["ASSEMBLY_AND_TEST_ACCESS_CHECKLIST.md","COMPLETE_MANUFACTURING_PREFLIGHT_RECEIPT.md"]
out={"PGOODActual":actual,"documentationExpected":"R_RST.2","consistent":all(actual in(p/n).read_text(encoding="utf8") for n in paths),"phase":"before final-review documentation fix","scope":"read-only document contract; no CAD/scientific rerun"}
(p/"DOCUMENT_CONTRACT_RED.json").write_text(json.dumps(out,indent=2),encoding="utf8")
print(json.dumps(out))

