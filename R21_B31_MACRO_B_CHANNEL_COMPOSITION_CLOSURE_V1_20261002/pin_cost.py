import math
def matching_cost(pads,targets):
 value=0
 for net,xy in pads:
  possible=targets.get(net,[]) if net not in ('','GND') else []
  if possible:value+=min(math.dist(xy,p) for p in possible)
 return value
