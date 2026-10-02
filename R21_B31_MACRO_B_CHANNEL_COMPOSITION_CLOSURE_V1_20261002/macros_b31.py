from b31_core import *
import sys
if __name__=='__main__':
 b1=json.loads((P/'MACRO_B.json').read_text())['positions']
 b2=dict(b1);b2.update({'U1':(17,28,90),'U2':(17,49,90),'U4':(31,28,90),'U3':(44,26,0),'U6':(43,14,180),'U5':(38,49,180),'U7':(57,49,180),'U13':(54,37,90),'U14':(55,22,90),'U15':(60,36,180),'J3':(68,55,90),'J4':(68,35,90),'U9':(16,7,0),'U8':(32,7,180),'U10':(48,7,0),'U11':(20,17,0),'U12':(53,16,0)})
 candidates=[]
 for label,pos in [('B1',b1),('B2',b2)]:
  reserve('macroCandidates',label+' actual19 anchors finite candidate')
  a=macro_audit(pos);a['label']=label;save('MACRO_'+label+'_AUDIT.json',a);candidates.append(a)
 legal=[a for a in candidates if not a['physicalCollisions']]
 assert legal,'NO_LEGAL_MACRO'
 choice=min(legal,key=lambda a:a['score']);save('MACRO_SELECTION.json',{'selected':choice['label'],'positions':choice['positions'],'selectedOnce':True,'hardMacroProxyCollisionGate':True,'allCandidateScores':[{k:a[k] for k in ['label','score','physicalCollisions','bbox','largestSampledEmptyRectangle','signalLengthSumMm']} for a in candidates]})
 print(json.dumps({'selected':choice['label'],'candidates':[{k:a[k] for k in ['label','score','physicalCollisions','bbox','largestSampledEmptyRectangle','signalLengthSumMm']} for a in candidates]}))
