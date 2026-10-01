from pathlib import Path
from science import ROOT,OLD
def emit(name,lines):
    (ROOT/'cases'/(name+'.cir')).write_text('\n'.join(lines)+'\n',encoding='ascii')
def loop(kind,inj):
    n=f'loop_{kind}_{inj}'
    s=[n,'.include "../../models/OPA4388_ORIGINAL.LIB"','V5 v5 0 5','VCM vcm 0 2.5',f'VTEST minus fb DC 0 AC {1 if inj=="v" else 0}',f'ITEST 0 minus DC 0 AC {1 if inj=="i" else 0}']
    if kind=='fixture':
        # Exact bilateral two-port y11=10uS,y22=1mS,k1=100/(1+s/2pi1k)*1mS,k3=0.
        # Return ratio exact: T=k1/(y11+y22), finite input impedance is retained.
        s=['Known one-pole Norton negative feedback fixture','VTEST minus fb DC 0 AC '+str(int(inj=='v')),'ITEST 0 minus DC 0 AC '+str(int(inj=='i')),'RIN minus 0 100k','ROUT fb 0 1k','EGAIN z 0 minus 0 100','RP z pole 1k','CP pole 0 159.1549431n','GOUT fb 0 pole 0 1m']
    elif kind=='row':
        s+=['VCMD cmd 0 2.25','X1 cmd minus v5 0 drv OPA4388','RISO drv row 1k','RFB row fb 4.99k','CHF drv fb 100p','RLOAD row vcm 200','CL row 0 1n']
    elif kind=='tia':
        s+=['X1 vcm minus v5 0 drv OPA4388','RISO drv tap 1k','RSENSE col fb 10k','RF tap col 4.99k','CF tap col 2.2n','RARRAY col row 200','VROW row 0 2.4375','CL col 0 1n','RADC tap ain 100','CADC ain 0 10n','RIN ain 0 1meg','CHF drv fb 22p']
    elif kind in ['vcm','vexc']:
        dc='2.5' if kind=='vcm' else '2.25'
        s[1]='.include "../../models/OPAx388.LIB"'
        s+=['VCMD cmd 0 '+dc,'X1 cmd minus v5 0 drv OPAx388','RISO drv tap 1k','RFB tap fb 4.99k','CHF drv fb 100p','CL tap 0 1n','RLOAD tap 0 1meg']
    else:raise ValueError(kind)
    s+=['.control','set wr_singlescale','set wr_vecnames']
    if kind!='fixture':s+=['optran 0 0 0 200n 2m 0']
    s+=['op','wrdata op.txt v(minus) v(fb)'+(' v(drv)' if kind!='fixture' else ''),'ac dec 100 1 100meg','let er=real(v(minus))','let ei=imag(v(minus))','let fr=real(v(fb))','let fi=imag(v(fb))','let ir=real(-i(VTEST))','let ii=imag(-i(VTEST))','wrdata ac.txt er ei fr fi ir ii','quit','.endc','.end']
    emit(n,s)
    return n
def corrected_legacy():
    original=(OLD/'make_coupled.py').read_text(encoding='utf-8')
    text=original.replace("'RUP vcm vexcmd 90k','RDN vexcmd 0 10k'","'RUP vcm vexcmd 10k','RDN vexcmd 0 90k'")
    (ROOT/'evidence'/'make_coupled_bias_corrected.py.txt').write_text(text,encoding='utf-8')
    return ROOT/'evidence'/'make_coupled_bias_corrected.py.txt'
def admittance(kind,port):
    # Independent open-port Y measurement; inductor preserves original DC connection,
    # AC coupling blocks port source DC. No macro-model lines are changed.
    base=(ROOT/'cases'/f'loop_{kind}_v.cir').read_text().splitlines()
    idx=base.index('.control');s=base[:idx]
    s=[x for x in s if not (x.startswith('VTEST ') or x.startswith('ITEST '))]
    s[0]=f'Port admittance {kind} {port}'
    s+=['LDC minus fb 1e9',f'VE ep 0 DC 0 AC {int(port=="e")}',f'VF fp 0 DC 0 AC {int(port=="f")}','CE ep minus 1m','CFPORT fp fb 1m']
    s+=['.control','set wr_singlescale','set wr_vecnames','set numdgt=15']
    s+=['op','wrdata op.txt v(minus) v(fb)'+(' v(drv)' if kind!='fixture' else ''),'ac dec 100 1 100meg','let yer=real(-i(VE))','let yei=imag(-i(VE))','let yfr=real(-i(VF))','let yfi=imag(-i(VF))','let er=real(v(minus))','let ei=imag(v(minus))','let fr=real(v(fb))','let fi=imag(v(fb))','wrdata ac.txt yer yei yfr yfi er ei fr fi','quit','.endc','.end']
    name=f'yport2_{kind}_{port}';emit(name,s);return name
if __name__=='__main__':
    import sys
    if sys.argv[1]=='loops':
        for k in ['fixture','row','tia','vcm','vexc']:
            for i in ['v','i']:print(loop(k,i))
    elif sys.argv[1]=='bias':print(corrected_legacy())
