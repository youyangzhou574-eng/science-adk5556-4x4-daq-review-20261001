from science import ROOT,OLD
from coupled_bench import emit
text=(OLD/'cases'/'loop_tia_v.cir').read_text().split('.control')[0];lines=text.splitlines();lines[0]='PZ single OPA closed TIA qualifier at ADC current port'
lines=[line for line in lines if not line.startswith('ITEST ') and not line.startswith('VTEST ')]
lines+=['VJOIN minus fb 0','.control','set numdgt=15','set filetype=ascii','optran 0 0 0 200n 2m 0','op','wrdata op.txt v(minus) v(fb) v(drv) v(ain)','pz ain 0 ain 0 cur pol','print all > pz.txt','write pz.raw all','quit','.endc','.end']
emit('pz_single_tia',lines)
