from pathlib import Path
import json,zipfile,hashlib
p=Path(__file__).parent
def sha(b):return hashlib.sha256(b).hexdigest().upper()
def strip(data):
    result=[]; count=0
    for line in data.splitlines(keepends=True):
        if line.startswith(b'{"type":"DOCHEAD"'):
            prefix,rest=line.split(b'||',1)
            text=rest.decode('utf-8'); obj,end=json.JSONDecoder().raw_decode(text)
            removed=[k for k in ('user','client') if k in obj]
            for k in removed:del obj[k]
            if removed:
                line=prefix+b'||'+json.dumps(obj,ensure_ascii=False,separators=(',',':')).encode()+text[end:].encode()
                count+=1
        result.append(line)
    out=b''.join(result)
    assert [x for x in data.splitlines(keepends=True) if not x.startswith(b'{"type":"DOCHEAD"')]==[x for x in out.splitlines(keepends=True) if not x.startswith(b'{"type":"DOCHEAD"')]
    for line in out.splitlines():
        if line.startswith(b'{"type":"DOCHEAD"'):
            obj,end=json.JSONDecoder().raw_decode(line.split(b'||',1)[1].decode());assert 'user' not in obj and 'client' not in obj
    return out,count
original=p/'C101_FINAL_CANDIDATE_LEGACY_PCB_NOT_FOR_USE.epro2'
public=p/'C101_PUBLIC_METADATA_STRIPPED_LEGACY_PCB_NOT_FOR_USE.epro2'
members=[]
with zipfile.ZipFile(original) as zin,zipfile.ZipFile(public,'w',zipfile.ZIP_DEFLATED) as zout:
    for info in zin.infolist():
        data=zin.read(info.filename)
        cleaned,n=strip(data) if info.filename.endswith('.epru') else (data,0)
        zout.writestr(info,cleaned)
        members.append({'member':info.filename,'changedDOCHEADCount':n,'nonHeaderBytesIdentical':True,'otherMemberBytesIdentical':n==0,'originalSHA256':sha(data),'publicSHA256':sha(cleaned)})
outdir=p/'PUBLIC_ACTUAL_SCH_SOURCE';outdir.mkdir(exist_ok=True)
sources=[]
for source in sorted((p/'ACTUAL_SCH_SOURCE').iterdir()):
    data=source.read_bytes();cleaned,n=strip(data);(outdir/source.name).write_bytes(cleaned)
    sources.append({'path':source.name,'changedDOCHEADCount':n,'nonHeaderBytesIdentical':True,'originalSHA256':sha(data),'publicSHA256':sha(cleaned)})
audit={'originalNativeBytes':original.stat().st_size,'originalNativeSHA256':sha(original.read_bytes()),'publicNativeFile':public.name,'publicNativeBytes':public.stat().st_size,'publicNativeSHA256':sha(public.read_bytes()),'members':members,'schSources':sources,'nativeExportOperationsAdded':0,'CADOperationsAdded':0,'publicDerivativeColdReopened':False,'legacyPCB':'Old176PCB remains NOT_FOR_USE; no C PCB created','privateAccountSQLitePublished':False,'originalNativeUnmodified':True}
(p/'NATIVE_PUBLIC_PRIVACY_DERIVATIVE.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
with zipfile.ZipFile(original) as a,zipfile.ZipFile(public) as b:
    assert a.namelist()==b.namelist()
    for n in a.namelist():
        x,y=a.read(n),b.read(n)
        expected,_=strip(x) if n.endswith('.epru') else (x,0)
        assert expected==y
(p/'NATIVE_PUBLIC_PRIVACY_VERIFICATION.json').write_text(json.dumps({'PASS':True,'originalSHA256':audit['originalNativeSHA256'],'publicSHA256':audit['publicNativeSHA256'],'changedHeaders':sum(x['changedDOCHEADCount'] for x in members),'allOtherMembersAndNonHeaderLinesIdentical':True,'all12SourcesNonHeaderBytesIdentical':True,'publicDerivativeColdReopened':False},indent=2),encoding='utf-8')
results=p/'CLI_REVIEW_RESULTS';results.mkdir(exist_ok=True)
index=[]
for f in sorted(p.glob('*.json')):
    q=json.loads(f.read_text(encoding='utf-8'))
    if not isinstance(q,dict) or 'command' not in q or 'parsed' not in q:continue
    parsed=q['parsed']; value=parsed.get('value') if isinstance(parsed,dict) else None
    omit=any(x in f.stem for x in ('CAPTURE','MATERIAL','COPY_IDENTITY','NATIVE_PDF_EXPORT'))
    result={'startedUTC':q.get('started_utc'),'returncode':q.get('returncode'),'ok':parsed.get('ok') if isinstance(parsed,dict) else None,'durationMs':parsed.get('durationMs') if isinstance(parsed,dict) else None,'error':parsed.get('error') if isinstance(parsed,dict) else None,'value':None if omit else value,'omittedRawContext':omit,'originalReceiptSHA256':sha(f.read_bytes())}
    (results/f.name).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');index.append({'receipt':f.name,'returncode':q.get('returncode'),'ok':result['ok'],'rawPublic':False})
(p/'CLI_OPERATION_INDEX.json').write_text(json.dumps(index,indent=2),encoding='utf-8')
print(json.dumps({'publicBytes':audit['publicNativeBytes'],'publicSHA256':audit['publicNativeSHA256'],'headers':sum(x['changedDOCHEADCount'] for x in members),'sources':len(sources),'CLIReceipts':len(index)}))
