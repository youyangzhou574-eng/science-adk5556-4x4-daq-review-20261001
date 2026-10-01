from pathlib import Path
import json,re,hashlib
r=Path(__file__).resolve().parent;old=r.parent/'R21_COUPLED_ROOTCAUSE_AND_R21_NATIVE_ECO_V1'
items=[]
for short in ['row','tia']:
 source=old/'cases'/('loop_'+short+'_v.cir');text=source.read_text().split('.control')[0];text=text.replace('"../../models/OPA4388_ORIGINAL.LIB"','"'+str(r/'models/OPA4388_ORIGINAL.LIB')+'"');items.append(('qual_'+short,text,'vtest',['minus','fb','drv']+(['row']if short=='row'else['tap','col','ain'])))
source=old/'cases/part_1row_1tia_800_gear.cir';text=source.read_text().split('.control')[0]
text=text.replace('"../../models/OPA4388_ORIGINAL.LIB"','"'+str(r/'models/OPA4388_ORIGINAL.LIB')+'"').replace('"../../models/OPAx388.LIB"','"'+str(r/'models/OPAx388.LIB')+'"')
items.append(('qual_4macro',text,'vref',['vcm','vexc','row0','col0','tap0','ain0']))
lines=['VCM VEXC local descriptor qualification','.include "'+str(r/'models/OPAx388.LIB')+'"','V5 v5 0 5','VREF ref 0 2.5','VTEST cmminus cmfb DC 0 AC 1','RCM_IN ref vcm_cmd 1k','XCM vcm_cmd cmminus v5 0 cmdrv OPAx388','RCMISO cmdrv vcm 1k','RCMFB vcm cmfb 4.99k','CCMHF cmdrv cmfb 100p','CCML vcm 0 1n','RUP vcm vexcmd 10k','RDN vexcmd 0 90k','XEX vexcmd exfb v5 0 exdrv OPAx388','REXISO exdrv vexc 1k','REXFB vexc exfb 4.99k','CEXHF exdrv exfb 100p','CEXL vexc 0 1n','RCML vcm 0 1meg','REXL vexc 0 1meg']
items.append(('qual_ref2','\n'.join(lines)+'\n','vtest',['cmminus','cmfb','cmdrv','vcm','exdrv','vexc']))
records=[]
for name,net,source,outputs in items:
 net+='\n.save all\n.control\nset filetype=ascii\nset numdgt=15\nset wr_singlescale\nset wr_vecnames\nop\nwrite op.raw all\nlisting e\n'
 for j,hz in enumerate([.01,.1,1,10,100,1e3,1e4,1e5,1e6,1e7,1e8,3e8]):net+='ac lin 1 %g %g\nwrdata ac_%02d.txt '%(hz,hz,j)+' '.join('v('+x+')'for x in outputs)+'\n'
 net+='ac dec 50 1 300meg\nwrdata dense.txt '+' '.join('v('+x+')'for x in outputs)+'\nquit\n.endc\n.end\n';(r/'cases'/ (name+'.cir')).write_text(net);records.append({'name':name,'source':source,'outputs':outputs,'loopReturnNodes':outputs[:2]if name in ('qual_row','qual_tia','qual_ref2')else None,'temperatureC':27,'fullNetworkPortAC':False,'purpose':'P0 local five-family actual primitive/AC qualification, no native or internal certificate claim','origin':str(old/'cases'/('loop_'+name[5:]+'_v.cir'))if name in ('qual_row','qual_tia')else str(source),'netlistSHA256':hashlib.sha256((r/'cases'/(name+'.cir')).read_bytes()).hexdigest()})
(r/'LOCAL_QUALIFICATION_CASES.json').write_text(json.dumps(records,indent=2));print(json.dumps([{'name':a['name'],'analyses':14}for a in records]))
