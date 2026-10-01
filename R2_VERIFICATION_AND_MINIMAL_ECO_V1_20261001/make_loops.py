from pathlib import Path
ROOT=Path(__file__).resolve().parent
def case(kind,revision=0):
 head='Nominal '+kind+' loop revision '+str(revision)+'\n.include "../../models/OPA4388_ORIGINAL.LIB"\nV5 v5 0 5\nVCM vcm 0 2.5\nVTEST minus fb DC 0 AC 1\n'
 if kind=='row':
  body='VCMD cmd 0 2.25\nX1 cmd minus v5 0 drv OPA4388\nRISO drv row 1k\nRFB row fb 4.99k\nCHF drv fb 100p\nRLOAD row vcm 200\nCL row 0 1n\n'
 elif kind=='tia':
  body='X1 vcm minus v5 0 drv OPA4388\nRISO drv tap 1k\nRSENSE col fb 10k\nRF tap col 4.99k\nCF tap col 2.2n\nRARRAY col row 200\nVROW row 0 2.4375\nCL col 0 1n\nRADC tap ain 100\nCADC ain 0 10n\nRIN ain 0 1meg\n'
  if revision:body+='CHF drv fb 100p\n'
 elif kind=='common':
  body='VREF cmd 0 2.5\nX1 cmd minus v5 0 drv OPA4388\nRISO drv tap 1k\nCL tap 0 1n\nRLOAD tap 0 1meg\n'
  if revision:body+='RFB tap fb 4.99k\nCHF drv fb 100p\n'
  else:body+='VFB tap fb 0\n'
 control='.control\nset wr_singlescale\nset wr_vecnames\nop\nwrdata op.txt v(drv) v(minus) v(fb)\nac dec 100 1 100meg\nlet loop=-v(fb)/v(minus)\nlet loop_real=real(loop)\nlet loop_imag=imag(loop)\nwrdata loop.txt loop_real loop_imag\nquit\n.endc\n.end\n'
 (ROOT/'cases'/f'loop_{kind}_r{revision}.cir').write_text(head+body+control,encoding='ascii')
if __name__=='__main__':
 import sys
 for kind in ('row','tia','common'):case(kind,int(sys.argv[1]) if len(sys.argv)>1 else 0)
