from pathlib import Path
ROOT=Path(__file__).resolve().parent
def make(revision=2,ohms=800,vdd=5):
 s=['Coupled 4x4 eight state actual amplifiers r'+str(revision),'.include "../../models/OPA4388_ORIGINAL.LIB"','.include "../../models/OPAx388.LIB"',f'V5 v5 0 {vdd}','VREF ref 0 2.5','RCM_IN ref vcm_cmd 1k','XCM vcm_cmd cmfb v5 0 cmdrv OPAx388','RCMISO cmdrv vcm 1k','RCMFB vcm cmfb 4.99k','CCMHF cmdrv cmfb 100p','CCML vcm 0 1n','RUP vcm vexcmd 90k','RDN vexcmd 0 10k','XEX vexcmd exfb v5 0 exdrv OPAx388','REXISO exdrv vexc 1k','REXFB vexc exfb 4.99k','CEXHF exdrv exfb 100p','CEXL vexc 0 1n','.model MUX SW(Ron=5 Roff=1e12 Vt=.5 Vh=.1)']
 for i in range(4):
  t=(2*i+1)*1.2e-3
  s += [f'VSEL{i} sel{i} 0 PULSE(0 1 {t} 10n 10n 1.2m 10m)',f'BNS{i} ns{i} 0 V=1-V(sel{i})',f'SA{i} vexc cmd{i} sel{i} 0 MUX',f'SB{i} vcm cmd{i} ns{i} 0 MUX',f'XR{i} cmd{i} fb{i} v5 0 drv{i} OPA4388',f'RISO{i} drv{i} row{i} 1k',f'RFB{i} row{i} fb{i} 4.99k',f'CHF{i} drv{i} fb{i} 100p',f'CLROW{i} row{i} 0 1n']
 for j in range(4):
  s += [f'XT{j} vcm minus{j} v5 0 tdrv{j} OPA4388',f'RSENSE{j} col{j} minus{j} 10k',f'RTISO{j} tdrv{j} tap{j} 1k',f'RF{j} tap{j} col{j} 4.99k',f'CF{j} tap{j} col{j} 2.2n',f'CHFT{j} tdrv{j} minus{j} '+('22p' if revision==2 else '100p'),f'RADC{j} tap{j} ain{j} 100',f'CADC{j} ain{j} 0 10n',f'RIN{j} ain{j} 0 1meg',f'CLCOL{j} col{j} 0 1n']
  s += [f'RA{i}_{j} row{i} col{j} {ohms}'for i in range(4)]
 saved=' '.join(f'v({n}{i})'for n in ['ain','row','drv','tdrv']for i in range(4))+' v(vcm) v(vexc) v(cmdrv) v(exdrv) i(V5)'
 s += ['.save '+saved,'.control','set wr_singlescale','set wr_vecnames','optran 0 0 0 500n 2m 0','tran 500n 9.6m 0 500n','wrdata trace.txt '+saved,'quit','.endc','.end']
 p=ROOT/'cases'/f'coupled_r{revision}_{ohms}_{str(vdd).replace(".","p")}.cir';p.write_text('\n'.join(s)+'\n',encoding='ascii');return p.name
if __name__=='__main__':
 import sys
 print(make(int(sys.argv[1])if len(sys.argv)>1 else 2,int(sys.argv[2])if len(sys.argv)>2 else 800,float(sys.argv[3])if len(sys.argv)>3 else 5))
