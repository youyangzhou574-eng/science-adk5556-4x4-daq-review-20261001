import pathlib,json,datetime,hashlib
p=pathlib.Path(__file__).parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
b={"package":"SCIENCE_ADK5556_4X4_R21_PCB_MANUFACTURING_PREFLIGHT_READONLY_V1","ruling":"CIRCUIT-PRO-R21-PCB-ENGINEERING-CLOSURE-ACCEPT-MANUFACTURING-PREFLIGHT-20261002-16","assistantId":"73707409-40eb-453d-bb08-37bbd07c9179","parentUser":"f5648be9-c6b7-4224-8bcc-833229a8fdfd","startedUTC":now,"limitMinutes":180,"phaseMinutes":{"P0":45,"P1":45,"P2":30,"P3":45,"reserve":15},"limits":{"existingEvidenceReview":1,"checklistContractBatch":1,"officialSources":6},"used":{"existingEvidenceReview":1,"checklistContractBatch":1,"officialSources":1},"forbiddenActual":{"newCAD":0,"session":0,"save":0,"capture":0,"DRC":0,"nativeExport":0,"simulation":0,"Gerber":0,"purchase":0,"manufacture":0,"bench":0,"powerup":0,"localGit":0,"system":0},"status":"READONLY_ACTIVE","reservations":[{"UTC":now,"op":"existingEvidenceReview","count":1,"scope":"single whole frozen-evidence preflight, ordinary read-only followups allowed; no CAD"},{"UTC":now,"op":"checklistContractBatch","count":1,"scope":"ruling16 P0-P3 document batch"},{"UTC":now,"op":"officialSources","count":1,"scope":"JLCPCB PCB capability page"}]}
(p/"EXECUTION_BUDGET.json").write_text(json.dumps(b,indent=2),encoding="utf-8")
root=p.parent/"R21_PCB_LOCAL_POUR_CLEARANCE_AND_FINAL_WARM_COLD_V1"
files={f.name:{"bytes":f.stat().st_size,"SHA256":hashlib.sha256(f.read_bytes()).hexdigest().upper()} for f in root.iterdir() if f.is_file()}
(p/"FROZEN_94_SOURCE_HASHES_BEFORE.json").write_text(json.dumps(files,indent=2),encoding="utf-8")
print("frozenfiles",len(files),"native",files["SCIENCE_ADK5556_4X4_R21_PCB_CLOSED_REVIEW.epro2"])

