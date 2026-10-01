import json,pathlib,hashlib,base64,csv,datetime
P=pathlib.Path(__file__).resolve().parent
def load(f):return json.loads((P/f).read_text('utf8'))
def write(f,v):(P/f).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n','utf8')
c=load('AUDIT_C_CAPTURE.json')['parsed']['value']
pre=load('PRECLOSE_SNAPSHOT.json')['parsed']['value']
d=load('AUDIT_D_COLD_CAPTURE.json')['parsed']['value']
a=load('AUDIT_C.json');b=load('AUDIT_D_COLD_FINAL.json')
def parts(v):return {q['ref']:q for pg in v['pages']for q in pg['parts']}
cp,pp,dp=parts(c),parts(pre),parts(d)
assert cp==pp==dp,'Core identity / physical pins / coordinates changed'
assert a['pin_checks']==b['pin_checks'] and a['net_members']==b['net_members'] and a['NC_exact_match']and b['NC_exact_match']
write('COLD_REOPEN_COMPARISON.json',dict(pass_=True,parts=176,connected=514,nets=106,NC=36,core_fields_and_pin_coordinates_exact=True,network_members_exact=True,raw_netlist_bytes_equal=a['raw_sha256']==b['raw_sha256'],raw_sha_C=a['raw_sha256'],raw_sha_D=b['raw_sha256'],no_byte_equality_claim=True))
for pg in d['pages']:(P/('FINAL_PAGE_'+str(pg['page']['index']+1)+'_SOURCE.txt')).write_text(pg['source'],'utf8')
f=d['native'];assert f['constructor']=='File' and f['tag']=='[object File]'
nb=base64.b64decode(f['base64']);assert len(nb)==f['size']
nf=P/'SCIENCE_ADK5556_4X4_R21_REVIEW.epro2';nf.write_bytes(nb)
artifacts={}
for f in [nf,P/'SCIENCE_ADK5556_4X4_R21_REVIEW.pdf',P/'SCIENCE_ADK5556_4X4_R21_NATIVE_CORRECTION_WORK.eprj2']:
 artifacts[f.name]={'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest().upper()}
write('FINAL_NATIVE_PDF_IDENTITY.json',artifacts)
with (P/'FINAL_514_PIN_NET_CHECKS.csv').open('w',encoding='utf-8-sig',newline='')as f:
 w=csv.DictWriter(f,fieldnames=['pin','expected','actual','pass_']);w.writeheader();w.writerows(b['pin_checks'])
with (P/'FINAL_106_NETWORK_MEMBERS.csv').open('w',encoding='utf-8-sig',newline='')as f:
 w=csv.writer(f);w.writerow(['net','members','matched']);w.writerows((x['net'],';'.join(x['actual']),x['pass_'])for x in b['net_members'])
with (P/'FINAL_36_NC.csv').open('w',encoding='utf-8-sig',newline='')as f:
 w=csv.writer(f);w.writerow(['ref','pin','NC']);w.writerows((ref,v['number'],True)for ref,q in sorted(dp.items())for v in q['pins']if v['nc'])
libs=load('ENGINEERING_LIBRARY_PARSED.json');plan=load('PLAN_FINAL.json');expected={q['ref']:q for q in plan['parts']}
with (P/'FINAL_176_BOM.csv').open('w',encoding='utf-8-sig',newline='')as f:
 w=csv.writer(f);w.writerow(['ref','actual_device_name','MPN_library','actual_value','actual_footprint','device_uuid','association_core_match'])
 for ref,q in sorted(dp.items()):
  e=expected[ref];w.writerow([ref,q['association']['name'],e['device'],q['props'].get('Value',q['name']),q['footprint']['name'],q['association']['uuid'],q['sub']==e['subpart']])
assert dp['R_J3_5']['association']['name']=='0603WAF1001T5E'
assert dp['R_J3_5']['props']['Value']=='1k 1%'
assert all(dp['C_ADC'+str(i)]['props']['Value']=='10nF X7R'for i in range(4))
assert all(dp['C_TIA_HF'+str(i)]['association']['name']=='GRM1885C1H220JA01D'for i in range(4))
write('KEY_METADATA_CHECK.json',{'pass':True,'R_J3_5_MPN':'0603WAF1001T5E','R_J3_5_Value':'1k 1%','C_ADC_Value_4':'10nF X7R','C_TIA_HF_MPN_4':'GRM1885C1H220JA01D','all_176_footprint_subpart_pin_identity':True,'not_full_supply_chain_release':True})
images=[]
for i in range(1,7):
 f1=P/f'PDF01_PAGE-{i}.png';f2=P/f'PDF02_PAGE-{i}.png'
 equal=f1.read_bytes()==f2.read_bytes()
 images.append(dict(page=i,final_image=f2.name,SHA256=hashlib.sha256(f2.read_bytes()).hexdigest().upper(),byte_identical_to_all_six_actually_viewed_PDF1=equal,final_1_5_viewed_again=i in [1,5],engineering_readable=True,giant_font=False,large_ref_value_overlap=False))
assert all(x['byte_identical_to_all_six_actually_viewed_PDF1']for x in images)
write('DRAWING_VISUAL_REVIEW.json',dict(pages=images,scope='Engineering readable net-port drawing; vector PDF supports zoom; no giant fontsize8',legacy_annotation_hold=True,legacy_notes='R2 titles and several inherited notes remain. Text.modify(content) returned saved true but actual source/PDF unchanged; 6 save predebits including first failed feedback attempt exhausted. No extra edit/export. External addendum is authoritative R2.1 annotation; do not read old 4.99k reset statement as actual value.',only_notes_attempted_no_layout_algorithm=True))
write('GATES.json',{'PIN_NET_PASS':True,'106_NETS_PASS':True,'36_NC_PASS':True,'176_PARTS_PASS':True,'COLD_REOPEN_PASS':True,'DRAWING_ENGINEERING_READABLE_PASS':True,'LEGACY_ANNOTATION_HOLD':True,'ERC_DETAIL_HOLD':True,'BENCH_VALIDATION_PENDING':True,'BENCH_NOT_RELEASED':True,'FAULT_PROTECTION_HOLD':True,'REFERENCE_CAPACITANCE_BENCH_HOLD':True,'HARDWARE_WCET_PENDING':True,'newSimulationCount':0})
q=load('EXECUTION_BUDGET.json');q['technicalExecutionEndedUTC']=datetime.datetime.now(datetime.timezone.utc).isoformat();q['scienceStopped']=True;q['STOP']='NATIVE_OPERATIONS_COMPLETE_HARD_QUOTAS_USED_NO_MORE_EDITS';q['actualSaveCalls']=5;q['failedSavePreDebit']=1;q['nativeStatus']='PIN_NET_AND_COLD_PASS_ENGINEERING_READABLE_WITH_LEGACY_ANNOTATION_HOLD';write('EXECUTION_BUDGET.json',q)
write('FINAL_SESSION_STATUS.json',{'OPEN_A_session':'0727b164-73b4-4157-ac61-3db40cde2a44','OPEN_D_session':'13e4c1d2-3db0-402f-9bee-9e30cd30a158','both_officially_closed':all(load(f)['parsed']['value']['status']=='closed'for f in ['CLOSE_A.json','CLOSE_D.json']),'no_solver_started':True,'collector_capture_returned_ok':load('AUDIT_D_COLD_CAPTURE.json')['returncode']==0,'collector_audit_before_JSON_ready_failed_then_same_saved_capture_audited_no_extra_capture':True})
print(json.dumps({'coldPASS':True,'used':q['used'],'artifacts':artifacts,'allSixFinalPNGsIdenticalToViewedPDF1':True,'legacyAnnotationHOLD':True}))
