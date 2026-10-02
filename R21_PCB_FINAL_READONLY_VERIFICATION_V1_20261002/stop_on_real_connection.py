import pathlib,json,datetime
p=pathlib.Path(__file__).parent;f=p/'EXECUTION_BUDGET.json';j=json.loads(f.read_text('utf8'));j['status']='STOP_REAL_V3V3_CONNECTION_ERROR';j['stop']='C_MCU1_1_AND_V3V3_VIA_E255_UNCONNECTED';j['stopUTC']=datetime.datetime.now(datetime.timezone.utc).isoformat();f.write_text(json.dumps(j,indent=2),'utf8')
