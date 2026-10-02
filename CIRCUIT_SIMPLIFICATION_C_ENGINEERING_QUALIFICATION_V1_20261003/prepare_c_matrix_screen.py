import pathlib,json
P=pathlib.Path(__file__).resolve().parent
folder=P/'cases'/'matrix800_selected_op';folder.mkdir(parents=True,exist_ok=True)
lines=['C full16 resistor five-amplifier candidate OP, ideal reference and equivalent mux',
 '.include "../../models/OPAx388.LIB"','.include "../../models/OPA4388_ORIGINAL.LIB"',
 'V5 v5 0 5','VCM vcm 0 2.5','VEX vex 0 2.25','XROW vex fb v5 0 out OPAx388',
 '.model MUX SW(Ron=4.9 Roff=1e12 Vt=.5 Vh=.1)']
for i in range(4):
 lines.extend([f'VSEL{i} sel{i} 0 {int(i==0)}',f'SD{i} out row{i} sel{i} 0 MUX',f'SS{i} row{i} fb sel{i} 0 MUX',f'CLROW{i} row{i} 0 1n'])
for j in range(4):
 lines.extend([f'XT{j} vcm col{j} v5 0 tia{j} OPA4388',f'RF{j} tia{j} col{j} 4.99k',f'CF{j} tia{j} col{j} 2.2n',f'RADC{j} tia{j} ain{j} 100',f'CADC{j} ain{j} 0 10n',f'RIN{j} ain{j} 0 1meg',f'CLCOL{j} col{j} 0 1n'])
 for i in range(4):lines.append(f'RS{i}{j} row{i} col{j} 800')
lines.extend(['.options method=gear','.control','set wr_singlescale','set wr_vecnames','set numdgt=15','op',
 'wrdata op.txt v(row0) v(row1) v(row2) v(row3) v(col0) v(col1) v(col2) v(col3) v(tia0) v(tia1) v(tia2) v(tia3) v(ain0) v(ain1) v(ain2) v(ain3)','quit','.endc','.end'])
(folder/'case.cir').write_text('\n'.join(lines)+'\n','utf8')
(folder/'ASSUMPTIONS.json').write_text(json.dumps({'full16resistor':True,'OPAmacros':5,'uneditedOfficialOPAmacros':True,'reference':'ideal 2.5/2.25, no REF3025 impedance/noise/startup qualification','mux':'equivalent SW4.9ohm/Roff1e12, not full TMUX model','adc':'1meg input resistance with100ohm10nF RC, no ADS internal dynamic model','cable':'unmeasured1nF per row and col','sensorOhm':800,'selectedRow':0,'targetMeanErrorPercent':1,'stage':'OP screen, not hardware or AC/PZ pass'},indent=2),'utf8')
print('prepared full16R 5macro oneOP only')
