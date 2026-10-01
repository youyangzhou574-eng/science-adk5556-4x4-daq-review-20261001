import pathlib,json,re
P=pathlib.Path(__file__).resolve().parent
O=P.parent/'R21_ENGINEERING_R21_NATIVE_AND_LIMITED_VALIDATION_V1'
h=json.loads((P/'CONTEXT_A.json').read_text('utf8'))['parsed']['value']
assert h['project']['friendlyName']=='SCIENCE_ADK5556_4X4_R21_NATIVE_CORRECTION_WORK'
pages=[dict(uuid=x['uuid'],index=i,name=x['name'])for i,x in enumerate(h['schematics'][0]['page'])]
ctx=dict(project_uuid=h['project']['uuid'],pages=pages)
(P/'PROJECT_CONTEXT.json').write_text(json.dumps(ctx,indent=2)+'\n','utf8')
s=(O/'capture_baseline.js').read_text('utf8')
s='const plan='+json.dumps(ctx)+';'+s[s.index('const project='):]
(P/'capture.js').write_text(s,'utf8')
print(json.dumps(ctx))
