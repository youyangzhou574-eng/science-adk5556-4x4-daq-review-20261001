import pathlib,json,sys,datetime
p=pathlib.Path(__file__).resolve().parent
f=p/'EXECUTION_BUDGET.json'
v=json.loads(f.read_text('utf8'))
k=sys.argv[1];n=int(sys.argv[2]) if len(sys.argv)>2 else 1
if v.get('stop'):raise SystemExit('Sticky stop active')
elapsed=(datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(v['startUTC'].replace('Z','+00:00'))).total_seconds()/60
if elapsed>=v['approvedMinutes']:raise SystemExit('Time budget exhausted')
if v['actual'][k]+n>v['limits'][k]:raise SystemExit('Hard quota exhausted: '+k)
v['actual'][k]+=n
v.setdefault('reservations',[]).append({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'kind':k,'count':n,'reason':sys.argv[3] if len(sys.argv)>3 else 'pre-debit'})
f.write_text(json.dumps(v,indent=2)+'\n','utf8')
print(json.dumps({'reserved':k,'count':v['actual'][k],'limit':v['limits'][k],'elapsedMinutes':elapsed}))
