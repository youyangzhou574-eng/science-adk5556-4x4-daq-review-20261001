import pathlib,json
from pypdf import PdfReader
p=pathlib.Path(__file__).parent
out=[]
for name in ["ADS8684","LM73100","TPS3890","BAT54S"]:
 r=PdfReader(p/"sources"/(name+".pdf"));pages=[]
 for i,pg in enumerate(r.pages):
  t=pg.extract_text()
  if ("LAND PATTERN" in t or "PACKAGE OUTLINE" in t or "Package outline" in t or "Pin Configuration" in t):pages.append({"page1":i+1,"text":t})
 (p/"sources"/(name+"_PACKAGE_EXTRACT.json")).write_text(json.dumps(pages,ensure_ascii=False,indent=2),encoding="utf8")
 out.append({"name":name,"packagePages":[q["page1"]for q in pages]})
print(json.dumps(out))

