import pathlib,json,datetime
p=pathlib.Path(__file__).parent;f=p/'EXECUTION_BUDGET.json';v=json.loads(f.read_text('utf8'))
v['stop']='NATIVE_HARD_QUOTAS_USED_FINAL_COLD_AUDIT_AND_DRC_NOT_COMPLETED';v['status']='BLOCKED_REVIEW_DELIVERY_ONLY';v['stopUTC']=datetime.datetime.now(datetime.timezone.utc).isoformat();f.write_text(json.dumps(v,indent=2),'utf8')
