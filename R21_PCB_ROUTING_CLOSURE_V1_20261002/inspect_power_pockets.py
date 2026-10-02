exec((__import__('pathlib').Path(__file__).parent/'filled_geometry.py').read_text('utf8'))
for key in('U4-16','U11_CT_C-2','U12-2','C_TIA_OP-2'):
 p=next(p for p in pads if p['key']==key);print('TARGET',key,p['x'],p['y'],p['geometry'].bounds)
 g=p['geometry'].buffer(70)
 print(json.dumps({'traces':[{k:v for k,v in t.items()if k!='geometry'}for t in traces if t['layer']==1 and t['net']!=p['net']and g.intersects(t['geometry'])],'vias':[{k:v for k,v in q.items()if k!='geometry'}for q in vias if q['net']!=p['net']and g.intersects(q['geometry'])],'pads':[(q['key'],q['net'],q['x'],q['y'])for q in pads if q['net']!=p['net']and g.intersects(q['geometry'])]}))
