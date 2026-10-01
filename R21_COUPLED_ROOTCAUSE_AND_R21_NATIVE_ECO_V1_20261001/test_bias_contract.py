"""Independent scalar contract: the physical intended bias is 0.9*VCM."""
import re, sys, json
from pathlib import Path
def spice_number(s):
    m=re.fullmatch(r'([0-9.]+)([kKmMuUnNpP]?)',s)
    return float(m[1])*{'':1,'k':1e3,'m':1e-3,'u':1e-6,'n':1e-9,'p':1e-12}[m[2].lower()]
def check(path):
    s=Path(path).read_text(encoding='utf-8')
    up=re.search(r'RUP vcm vexcmd ([0-9.]+[kK]?)',s)
    dn=re.search(r'RDN vexcmd 0 ([0-9.]+[kK]?)',s)
    r1,r2=spice_number(up[1]),spice_number(dn[1])
    v=2.5*r2/(r1+r2)
    out={'file':str(path),'Rup_Ohm':r1,'Rdn_Ohm':r2,'VCM_V':2.5,'command_V':v,'required_V':2.25,'PASS':abs(v-2.25)<1e-12}
    print(json.dumps(out))
    return out['PASS']
if __name__=='__main__':sys.exit(0 if check(sys.argv[1]) else 1)
