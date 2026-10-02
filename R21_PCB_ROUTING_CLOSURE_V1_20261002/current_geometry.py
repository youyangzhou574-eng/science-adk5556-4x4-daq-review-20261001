exec((__import__('pathlib').Path(__file__).parent/'prepare_p1.py').read_text('utf8').split('for net in selected:')[0])
for label in('P1_SIGNAL_ROUTE_PLAN','P1_RESIDUAL_PLAN','P1_DOGLEG_PLAN'):
 prev=json.loads((P/(label+'.json')).read_text('utf8'))
 for t in prev['paths']:traces.append(dict(t,geometry=LineString(t['points']).buffer(t['width']/2,cap_style=1)))
 for q in prev['vias']:vias.append(dict(q,geometry=Point(q['x'],q['y']).buffer(q['diameter']/2)))
p1paths=[];p1vias=[]
if (P/'APPLY_LOCAL_MOVES.json').exists():
 actual=json.loads((P/'APPLY_LOCAL_MOVES.json').read_text('utf8'))['parsed'];assert actual['ok']
 for c in actual['value']['actual']:
  for q in c['pads']:
   p=next(p for p in pads if p['ref']==c['ref']and p['number']==q['number']);assert p['net']==q['net']
   oldx,oldy=p['x'],p['y'];p['geometry']=translate(rotate(p['geometry'],q['rotation']-p['rotation'],origin=(oldx,oldy)),q['x']-oldx,q['y']-oldy)
   p.update(x=q['x'],y=q['y'],rotation=q['rotation'],pad=q['pad'])
  part=next(p for p in v['parts']if p['ref']==c['ref']);part.update(x=c['x'],y=c['y'],rotation=c['rotation'])
if (P/'P1_FINISH_LINE_0_RUN.json').exists():
 prev=json.loads((P/'P1_FINISH_PLAN.json').read_text('utf8'))
 for t in prev['paths']:traces.append(dict(t,geometry=LineString(t['points']).buffer(t['width']/2,cap_style=1)))
 for q in prev['vias']:vias.append(dict(q,geometry=Point(q['x'],q['y']).buffer(q['diameter']/2)))
