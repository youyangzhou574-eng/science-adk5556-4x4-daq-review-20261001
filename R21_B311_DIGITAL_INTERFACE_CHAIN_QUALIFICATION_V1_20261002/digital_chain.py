import math
def series_paths(pads,sources,connectors,resistors):
 result=[]
 for r in resistors:
  pp=[p for p in pads if p['ref']==r]
  if len(pp)!=2 or not all(p['net'] for p in pp):continue
  for inside,outside in [pp,pp[::-1]]:
   for s in pads:
    if s['ref'] not in sources or s['net']!=inside['net']:continue
    for c in pads:
     if c['ref'] not in connectors or c['net']!=outside['net']:continue
     l1=math.dist(s['xy'],inside['xy']);l2=math.dist(outside['xy'],c['xy']);span=math.dist(inside['xy'],outside['xy']);direct=math.dist(s['xy'],c['xy'])
     result.append({'orderedNodes':[x['ref']+'.'+x['pad'] for x in [s,inside,outside,c]],'resistor':r,'insideNet':inside['net'],'outsideNet':outside['net'],'segment1Mm':l1,'segment2Mm':l2,'wireLengthMm':l1+l2,'resistorPadSpanMm':span,'functionalLengthWithResistorSpanMm':l1+l2+span,'directEndpointMm':direct,'stretch':(l1+l2+span)/direct if direct else None,'direction':'undirected actual-net functional geometry; RX/SWD/NRST not claimed MCU outputs'})
 return result
