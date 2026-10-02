from pathlib import Path
import json
P=Path(__file__).parent
project='ee4f96f0b67e0b9c85e719fedce50790f5a49c47e4db3392e90aea8fef4c93c9'
old=P.parent/'R21_PCB_LOCAL_POUR_CLEARANCE_AND_FINAL_WARM_COLD_V1'
pcb=(old/'capture_routing.js').read_text('utf8').replace('7efd53fbc610430d096d3e416ed545dafaea621ce2f02ed4c02d0ed9d65ed701',project)
sch=(P.parent/'R21_NATIVE_PIN_NET_CORRECTION_AND_FINAL_DRAWING_V1'/'preclose_snapshot.js').read_text('utf8').replace('b771f646994e1e87ccac719bcaeddd7f79898452652eb8c78e76c7463539d085',project)
# One complete baseline batch across schematic+PCB, no native export/save.
sch=sch.replace('return {project,pages};','const schematic={project,pages};')
pcb=pcb.replace('const pr=', 'const pr=').replace('return {parts,','const pcb={parts,').rstrip().rstrip(';')+'; return {schematic,pcb};'
(P/'capture_baseline.js').write_text(sch+'\n'+pcb,'utf8')
(P/'capture_pcb.js').write_text((old/'capture_routing.js').read_text('utf8').replace('7efd53fbc610430d096d3e416ed545dafaea621ce2f02ed4c02d0ed9d65ed701',project),'utf8')
(P/'search_connector_prefix.js').write_text("const libraryUuid=await eda.lib_LibrariesList.getSystemLibraryUuid(); return {libraryUuid,items:await eda.lib_Device.search('171856',libraryUuid,undefined,undefined,40,1)};",'utf8')
print('Prepared one full baseline batch and same-family lookup')
