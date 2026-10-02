exec((__import__('pathlib').Path(__file__).parent/'filled_geometry.py').read_text('utf8'))
for key in('U14-2','U14-11','U12-5','U9-5'):
 p=next(p for p in pads if p['key']==key);print('TARGET',key,p['pad'],p['rotation'],p['geometry'].bounds)
 for dx,dy in[(0,-70),(0,70),(-70,0),(70,0),(0,-130),(0,130),(-130,0),(130,0)]:
  q=(p['x']+dx,p['y']+dy);g=LineString([(p['x'],p['y']),q]).buffer(9.2,cap_style=1);vg=Point(*q).buffer(18.2)
  blockers={'pad':[x['key']for x in pads if x['net']!=p['net']and g.intersects(x['geometry'])],'L1Trace':[(t['id'],t['net'],t['points'])for t in traces if t['layer']==1 and t['net']!=p['net']and g.intersects(t['geometry'])],'via':[(x['id'],x['net'],x['x'],x['y'])for x in vias if x['net']!=p['net']and g.intersects(x['geometry'])],'viaLandingTrace':[(t['net'],t['layer'],t['id'])for t in traces if t['net']!=p['net']and vg.intersects(t['geometry'])]}
  print(dx,dy,json.dumps(blockers))
