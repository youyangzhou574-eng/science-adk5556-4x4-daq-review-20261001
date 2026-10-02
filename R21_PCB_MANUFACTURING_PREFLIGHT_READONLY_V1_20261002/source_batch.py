import pathlib,json,datetime,urllib.request,shutil,hashlib
p=pathlib.Path(__file__).parent;(p/"sources").mkdir(exist_ok=True)
b=json.loads((p/"EXECUTION_BUDGET.json").read_text())
b["used"]["officialSources"]=6;b["reservations"].append({"UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),"op":"officialSources","count":5,"scope":"ST G031 datasheet; existing manufacturer ADS8684/LM73100/TPS3890/BAT54S documents; total6 including JLC. OPA/TMUX use prior pin-map acceptance only, no extra datasheet access."})
(p/"EXECUTION_BUDGET.json").write_text(json.dumps(b,indent=2),encoding="utf8")
specs=[
("JLC_CAPABILITIES.html","https://jlcpcb.com/capabilities/pcb-capabilities",None),
("STM32G031K8.pdf","https://www.st.com/resource/en/datasheet/stm32g031k8.pdf",None),
("ADS8684.pdf","https://www.ti.com/lit/ds/symlink/ads8684.pdf",p.parent/"FIRST_BUILD_DETAILED_DESIGN_AND_NATIVE_SCHEMATIC_V1"/"sources"/"ADS8684.pdf"),
("LM73100.pdf","https://www.ti.com/lit/ds/symlink/lm73100.pdf",p.parent/"FIRST_BUILD_ELECTRICAL_CLOSURE_AND_SCHEMATIC_R2_V1"/"sources"/"LM73100.pdf"),
("TPS3890.pdf","https://www.ti.com/lit/ds/symlink/tps3890.pdf",p.parent/"R21_COUPLED_ROOTCAUSE_AND_R21_NATIVE_ECO_V1"/"sources"/"TPS3890.pdf"),
("BAT54S.pdf","https://assets.nexperia.com/documents/data-sheet/BAT54S.pdf",p.parent/"R21_COUPLED_ROOTCAUSE_AND_R21_NATIVE_ECO_V1"/"sources"/"BAT54S.pdf")]
out=[]
for name,url,local in specs:
 dest=p/"sources"/name
 try:
  if local:shutil.copyfile(local,dest);method="reuse frozen manufacturer PDF"
  else:
   with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"}),timeout=20)as r:dest.write_bytes(r.read());method="official anonymous download"
  row={"name":name,"url":url,"method":method,"bytes":dest.stat().st_size,"SHA256":hashlib.sha256(dest.read_bytes()).hexdigest().upper(),"UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),"sourceLocal":str(local) if local else None,"ok":True}
 except Exception as e:row={"name":name,"url":url,"ok":False,"error":str(e)}
 out.append(row)
(p/"SOURCES.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf8")
print(json.dumps(out,ensure_ascii=False))

