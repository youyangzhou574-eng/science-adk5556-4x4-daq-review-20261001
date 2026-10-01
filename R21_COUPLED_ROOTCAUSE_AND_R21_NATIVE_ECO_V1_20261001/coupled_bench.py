"""Frozen-candidate full and partitioned benches, with explicit ideal boundaries."""
import re,json
from science import ROOT
from make_cases import emit
def make(name,rows=4,cols=4,load='800',state=0,vdd=5,analysis='static',method='trap',solver='default'):
    resistors=[[8000. if load=='8000' else 800. for j in range(4)] for i in range(4)]
    if load=='high_target':resistors[state if state>=0 else 0][0]=8000.
    s=[name,'.include "../../models/OPA4388_ORIGINAL.LIB"','.include "../../models/OPAx388.LIB"',f'V5 v5 0 {vdd}','VREF ref 0 DC 2.5 AC 1','RCM_IN ref vcm_cmd 1k','XCM vcm_cmd cmfb v5 0 cmdrv OPAx388','RCMISO cmdrv vcm 1k','RCMFB vcm cmfb 4.99k','CCMHF cmdrv cmfb 100p','CCML vcm 0 1n','RUP vcm vexcmd 10k','RDN vexcmd 0 90k','XEX vexcmd exfb v5 0 exdrv OPAx388','REXISO exdrv vexc 1k','REXFB vexc exfb 4.99k','CEXHF exdrv exfb 100p','CEXL vexc 0 1n','.model MUX SW(Ron=5 Roff=1e12 Vt=.5 Vh=.1)']
    for i in range(4):
        sel='PULSE(0 1 100u 10n 10n 1m 10m)' if analysis=='transient' and i==state else str(int(i==state)) if analysis!='transient' else '0'
        s += [f'VSEL{i} sel{i} 0 {sel}',f'BNS{i} ns{i} 0 V=1-V(sel{i})',f'SA{i} vexc cmd{i} sel{i} 0 MUX',f'SB{i} vcm cmd{i} ns{i} 0 MUX']
        if i<rows:s += [f'XR{i} cmd{i} fb{i} v5 0 drv{i} OPA4388',f'RISO{i} drv{i} row{i} 1k',f'RFB{i} row{i} fb{i} 4.99k',f'CHF{i} drv{i} fb{i} 100p']
        else:s += [f'BBOUNDROW{i} row{i} 0 V=V(cmd{i})']
        s += [f'CLROW{i} row{i} 0 1n']
    for j in range(4):
        if j<cols:
            s += [f'XT{j} vcm minus{j} v5 0 tdrv{j} OPA4388',f'RSENSE{j} col{j} minus{j} 10k',f'RTISO{j} tdrv{j} tap{j} 1k',f'RF{j} tap{j} col{j} 4.99k',f'CF{j} tap{j} col{j} 2.2n',f'CHFT{j} tdrv{j} minus{j} 22p',f'RADC{j} tap{j} ain{j} 100',f'CADC{j} ain{j} 0 10n',f'RIN{j} ain{j} 0 1meg']
        else:s += [f'BBOUNDCOL{j} col{j} 0 V=V(vcm)']
        s += [f'CLCOL{j} col{j} 0 1n']
        s += [f'RA{i}_{j} row{i} col{j} {resistors[i][j]:g}' for i in range(4)]
    saved=['v(vcm)','v(vexc)','v(vexcmd)','v(cmdrv)','v(exdrv)']+[f'v(row{i})'for i in range(4)]+[f'v(col{i})'for i in range(4)]+[f'v({n}{i})'for n in ['drv']for i in range(rows)]+[f'v({n}{i})'for n in ['tdrv','tap','ain']for i in range(cols)]
    # Full internal-node initial guesses copied from a real, qualified macro-model OP.
    # Nodesets are Newton initial guesses, not imposed voltages/ICs and not model edits.
    raw=(ROOT/'results'/'diag_tia_opseed'/'op.raw').read_text()
    names=[line.split()[1:] for line in raw.split('Variables:\n')[1].split('Values:\n')[0].splitlines() if line.strip()]
    vv=raw.split('Values:\n')[1].splitlines();vals=[float(vv[0].split()[1])]+[float(l) for l in vv[1:] if l.strip()]
    for amp in ['xcm','xex']+[f'xr{i}'for i in range(rows)]+[f'xt{j}'for j in range(cols)]:
        for (n,typ),val in zip(names,vals):
            if typ=='voltage' and n.startswith('v(x1.'):
                newnode=n.replace('x1.',amp+'.')
                if amp in ['xcm','xex']:newnode=newnode.replace('opa4388','opax388')
                s.append('.nodeset '+newnode+'='+format(val,'.15g'))
    seed=['v(vcm)=2.5','v(vexc)=2.25','v(vexcmd)=2.25','v(cmfb)=2.5','v(exfb)=2.25','v(cmdrv)=2.525','v(exdrv)=2.25']
    for i in range(4):
        value=2.25 if i==state and analysis!='transient' else 2.5
        seed += [f'v(row{i})={value}',f'v(cmd{i})={value}']
        if i<rows:seed += [f'v(fb{i})={value}',f'v(drv{i})={value-(2.5-value)*sum(1000/x for x in resistors[i])}']
    for j in range(cols):
        it=.25/resistors[state][j] if state>=0 and analysis!='transient' else 0
        tap=2.5+4990*it;drv=tap+1000*(it+tap/1000100)
        seed += [f'v(col{j})=2.5',f'v(minus{j})=2.5',f'v(tap{j})={tap}',f'v(ain{j})={tap}',f'v(tdrv{j})={drv}']
    s+=['.nodeset '+' '.join(seed),'.save '+('all' if name.endswith('_seed') else ' '.join(saved)),'.options method='+method]
    s+=['.control','set wr_singlescale','set wr_vecnames','set numdgt=15']
    if solver=='klu':s+=['option klu']
    s+=['optran 1 1 1 200n 100u 0','op','wrdata op.txt '+' '.join(saved)]
    if name.endswith('_seed'):s+=['set filetype=ascii','write op.raw all']
    if analysis=='static':
        s+=['ac dec 80 1 100meg','wrdata ac.txt '+' '.join(saved)]
    elif analysis=='pz':
        # SISO port can miss unobservable internal modes; do not claim exhaustive full-state poles.
        s+=['pz ref 0 ain0 0 vol pol','print all > pz.txt']
    else:
        s+=['tran 200n 600u 0 100n','wrdata trace.txt '+' '.join(saved)]
    s+=['quit','.endc','.end'];emit(name,s)
    (ROOT/'cases'/(name+'.json')).write_text(json.dumps({'rowsMacro':rows,'colsMacro':cols,'actualMacroCount':2+rows+cols,'state':state,'load':load,'vdd':vdd,'analysis':analysis,'method':method,'solver':solver,'boundary':'unmodeled row command and column VCM are ideal controlled voltage sources; no full-board claim','correctedBias':True,'saved':saved,'arrayOhms':resistors},indent=2))
    return name
