from pathlib import Path
import json
p=Path(__file__).parent;plan=json.loads((p/'C_NATIVE_BUILD_PLAN.json').read_text(encoding='utf-8'))
src=(p/'build_c_page0.js').read_text(encoding='utf-8');tail=src[src.index('; const result=')+1:]
start=tail.index(' const all=');end=tail.index(' for(let i=0;')
cleanup=tail[start:end]
tail=tail[:start]+' if(plan.clean){\n'+cleanup+'\n}\n'+tail[end:]
tail=tail.replace('350+(i%4)*560,220+Math.floor(i/4)*420','350+((q.layoutIndex)%4)*560,220+Math.floor(q.layoutIndex/4)*420')
chunks=[]
for page in plan['pages'][1:]:
 parts=[dict(q,layoutIndex=i)for i,q in enumerate(x for x in plan['parts']if x['page']==page['index'])]
 for n in range(0,len(parts),8):
  group=parts[n:n+8];q={'project':plan['project'],'page':page,'parts':group,'clean':n==0,'save':page['index']in[2,5] and n+8>=len(parts)}
  name='C_PAGE%d_CHUNK%d'%(page['index'],n//8)
  (p/(name+'.js')).write_text('const plan='+json.dumps(q,ensure_ascii=False)+';'+tail,encoding='utf-8')
  chunks.append({'label':name,'codeFile':name+'.js','cost':{'save':1}if q['save']else {},'expectedRefs':[x['ref']for x in group]})
(p/'REMAINING_NATIVE_CHUNKS.json').write_text(json.dumps(chunks,indent=2),encoding='utf-8')
print(json.dumps({'chunks':len(chunks),'pageCounts':{i:sum(x['page']==i for x in plan['parts'])for i in range(6)},'maxPartsPerChunk':8}))
