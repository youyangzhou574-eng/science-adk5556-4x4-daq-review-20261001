from pathlib import Path
import json,csv,datetime,hashlib
P=Path("E:/open/SCIENCE_ADK5556_4X4_DAQ_REPLICA/R21_B22_STRUCTURED_CHANNEL_ARRAY_PLACEMENT_V1");N=json.loads((P/'PLACEMENT_B22.json').read_text());A=json.loads((P/'INDEPENDENT_FINAL_AUDIT.json').read_text())
B=json.loads((P/'EXECUTION_BUDGET.json').read_text());B['status']='COMPLETE_BLOCKED_NO_THIRD_ADJUSTMENT';B['finishedUTC']=datetime.datetime.now(datetime.timezone.utc).isoformat();(P/'EXECUTION_BUDGET.json').write_text(json.dumps(B,indent=2),encoding='utf8')
viol=[r for r in A['extraDecapPinLocalChecks']if not r['passNoIncrease']]
with(P/'EXTRA_LOCAL_PIN_DISTANCES.csv').open('w',encoding='utf-8-sig',newline='')as f:
 w=csv.DictWriter(f,fieldnames=list(A['extraDecapPinLocalChecks'][0]));w.writeheader();w.writerows(A['extraDecapPinLocalChecks'])
with(P/'STRUCTURED_GROUPS.csv').open('w',encoding='utf-8-sig',newline='')as f:
 fields=['name','kind','refs','axis','pitchMm','pitchXmm','pitchYmm','rotation','reason'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for r in N['templates']:w.writerow({k:','.join(r[k])if k=='refs'else r.get(k,'')for k in fields})
scope=[
 {'requirement':'TIA/ROW four-channel roles','result':'PASS_PIN_FACING_2PLUS2_EXCEPTION','evidence':'8 groups same rotation and symmetric two pairs; U1/U2 opposite-side pins prevent a selected feasible single4line under strict baseline distances'},
 {'requirement':'ADC R/C4x2 inputs','result':'PASS','evidence':'one common four-column2row pitch2.4mm; real94checks no increase'},
 {'requirement':'ADC AVDD9/30 and REFCAP cap banks','result':'HOLD_LOCAL_FEASIBILITY','evidence':'three banks retain B2.1 baseline after finite equal-pitch templates fail strict distances/collision'},
 {'requirement':'ADC REFIO/DVDD cap banks','result':'PASS_OFFLINE_ROW','evidence':'REFIO y-row3.299995; DVDD x-row3.299995mm'},
 {'requirement':'BIAS VCM/VEX paired placement','result':'PARTIAL_CENTRAL_PAIRING_AXIS_MIRROR_HOLD','evidence':'HF/FB/ISO centers centrally paired about U3; requested common-axis reflection is not implemented (HOLD); not a footprint/net reflection'},
 {'requirement':'reference divider banks','result':'PASS_ROW_AND_COLUMN','evidence':'two five-member banks, not one entire divider row'},
 {'requirement':'POWER common mirrored U9/U10 templates','result':'PARTIAL_ROLE_ROWS_MIRROR_HOLD','evidence':'both8member control banks rows, but pitch3.3000204 and2.3750032 differ; not exact paired mirror'},
 {'requirement':'DIGITAL U13/14/15 IC and cap rows','result':'PARTIAL_LOCAL_ANCHORS_RETAINED','evidence':'IC macro anchors retained; no new common IC row/2x2 template is implemented'},
 {'requirement':'J3/J4 identical local template','result':'PARTIAL_PROTECTOR_ROWS_TEMPLATE_HOLD','evidence':'individual resistor/diode rows passed; J3 resistor vertical versus J4 horizontal, not same complete template'},
 {'requirement':'all critical local pin distances','result':'HOLD_EXTRA_FIVE','evidence':'94 inherited pass;5 of12 added real-net pin-pair checks across10 IC/passive combinations increase by.09155 to1.35178mm'}
]
(P/'REQUIREMENT_ACCEPTANCE_MATRIX.json').write_text(json.dumps(scope,indent=2),encoding='utf8')
gates={'B22_OFFLINE_IDENTITY':'PASS','B22_BODY_AND_PAD_PROXY':'PASS','B22_INHERITED_94_PIN_DISTANCE':'PASS_NO_INCREASE','EXTRA_IC_LOCAL_DISTANCES':'HOLD_FIVE_INCREASES','B22_ALL_STRUCTURED_REQUIREMENTS':'PARTIAL_HOLD','USER_FINAL_VISUAL_SELECTION':'PENDING','CAD_RELEASED':False,'NATIVE_DRC':'NOT_RUN','FFC_EXACT_ACTUATOR':'HOLD','MANUFACTURING_RELEASED':False,'BENCH_RELEASED':False,'STOP':'TWO_ADJUSTMENTS_AND_ONE_IMAGE_USED_NO_FURTHER_COORDINATE_EDITS'}
(P/'GATES.json').write_text(json.dumps(gates,indent=2),encoding='utf8')
pairs='\n'.join('|{ic}.{icPad}|{passive}.{passivePad}|{beforeMm:.6f}|{afterMm:.6f}|{deltaMm:+.6f}|'.format(**v)for v in viol)
coverage='\n'.join('|'+s['requirement']+'|'+s['result']+'|'+s['evidence']+'|'for s in scope)
report=f'''# B2.2 structured-channel array placement — partial visual draft / HOLD
Only circuit project SCIENCE_ADK5556_4X4_DAQ_REPLICA. Full completed ruling assistant3d968530-1342-4bbd-9af0-dae4f321ab20 / parenta9ed76f1-da40-41ef-822c-7751b8071c0c is PRO_B22_RULING_FULL.md.
User asked for Science-like regular passive arrays within functions; no additional area compression. Earlier B2.1 conditional480min native scope stays dormant and is not automatically migrated to B2.2.
## Outcome
A complete176-coordinate B2.2 visual draft was generated.125 positions/orientations changed, all15IC+4connector macro anchors exactly fixed (plus6 short-local parts). Body bbox71.0000204x63.5000124mm unchanged.552pads/514assigned/107nets/36NC+2emptyMP remain identical; no native PCB, values, signal mapping, footprint or board-frame writes.
All15400 different-component pairs independently examined for body and conservative pad-proxy; both0area overlaps >1e-8mm². FFC planning keepout0; exact actuator/mating not qualified.
Inherited94 actual IC-pad→passive-pad distances all no increase (max0; largest reduction3.869006mm). These include RF/CF functional paths through series resistors, not false direct-net claims.
However additional real-net local checks find five increases. No universal decoupling/high-Z distance PASS. Overall candidate is PARTIAL_VISUAL_HOLD, not CAD-ready. No third adjustment or second image.
## Implemented geometry
TIA/ROW same role now consistent rotation and pin-facing mirrored2+2 patterns. Channel order follows physical IC perimeter0→1→2→3, not falsely four left-to-right columns.
ADC inputs are an actual4-column2-row group at2.4mm pitch, with correct pin identity. REFIO/DVDD local cap rows align. VCM/VEX HF/FB/ISO centers use central positional pairing around U3; the requested common-axis reflection is NOT implemented and remains PARTIAL/HOLD. Copper layers/pin identity are not mirrored.
Divider banks, MUXpulls, Power control resistors, supervisor divider and debug protectors use local regular rows/columns.56declared groups include singleton local placements and3retained exceptions: this does not mean56multi-element arrays. STRUCTURED_GROUPS.csv gives all actual membership, directions and pitches.
No optimization library, EDA API experiment, auto-layout plugin or new algorithm family. Only finite local templates tested with actual pad/collision gates.
## Requirement coverage and limits
|Requested group|Result|Actual evidence|
|---|---|---|
{coverage}
## Added pin-local checks — five open items
No relaxed engineering threshold was invented. The local conservative rule is B2.1 +1e-6mm; a failure here is a coordinate limitation, not physical instability or measured electrical error.
|IC pin|Passive pin|B2.1mm|B2.2mm|Delta mm|
|---|---|---:|---:|---:|
{pairs}
All12added pin-pair comparisons across10 IC/passive combinations are in EXTRA_LOCAL_PIN_DISTANCES.csv. U13/U14/U15 decoupling and other additional checks not listed here did not grow.5failures cannot be hidden behind the inherited94PASS.12pairs are generated by10selected IC/passive combinations because each U11/U12 VDD cap matches two IC pads.
## Budget and first failure
Approved120min, at most2internal adjustments and1comparison image. Actual2/2adjustments and1/1image. AllCAD/GUI/native/simulation/sources/Gerber/procurement/manufacturing/bench0.
Adjustment01 stopped at ADC_DVDD: a previously adopted bank occupied an unprocessed critical location. This local implementation scheduling error is preserved in ADJUSTMENT_01.log and structured_placement_FIRST_FAILED.py. First partial coordinates were not emitted before that exception; no claim of a fullfirst-coordinate archive.
Original sites for future critical passives were reserved until adopted. Real-geometry unit regression RESERVATION_RED failed, RESERVATION_GREEN passed. These tests did not start candidate passes. Adjustment02 completed and independent audit emitted allchecks. No third layout pass, no reducedcollision filter, no exception post-hoc labelled PASS.
InputSHA: all7originalfiles and local copies unchanged. First-failed code is historical evidence, not an alternate runnable plan. initialize_stage.py refuses a pre-existing budget; historical preparation sources are not a safe one-click re-run. The final figure was viewed; source is exact same coordinate data as audit.
## Deliverables
PLACEMENT_B22.json/CSV, onePLACEMENT_B21_VS_B22.png, actual geometry/body source/register, seveninputmanifest, STRUCTURED_GROUPS.csv, KEY_PIN_DISTANCE_B22.csv, EXTRA_LOCAL_PIN_DISTANCES.csv, fullindependentaudit, acceptance matrix, GATES/budget/ledger, initial failure+RED/GREEN, ownscripts, fullruling and freshfinalreview.
Raw accountSQLite/credentials/third-partyfullPDF/GitLFS not included. Public short report/directreadable files/ZIP supplementation only.
## Next engineering decision
Please review this oneB2.2 draft and actual open items together. Do not re-open wholeplacement, EDA theory, MIMO or descriptor research.
A focused bounded engineering closure would limit coordinate corrections to the five listed local capacitors, three retained ADC cap banks, and common power/debug/digital role templates, only if actual pad distances/collision keep macro topology.
User explicitly requests larger bounded execution time/count/autonomy in normal reports. If a further correction is required, request one180min finite closure (40localpins/60localtemplates/30audit+oneimage/50delivery), at most2adjustments/1image; CAD0. No automatic execution of this request.
After final selection and complete Pro release, retain a separate480min native request with copy2/session4/save10/import2/audit6/DRC8/pour2/export1/image3. Previous B2.1 conditionalbudget does not authorize this B2.2candidate or eliminate current HOLD.
END-OF-COMPLETE-R21-B22-STRUCTURED-CHANNEL-PARTIAL-VISUAL-RECEIPT
'''
(P/'COMPLETE_B22_RECEIPT.md').write_text(report,encoding='utf8')
(P/'README.md').write_text('''# B2.2 local structured-channel visual draft
[Complete receipt](COMPLETE_B22_RECEIPT.md) · [One comparison](PLACEMENT_B21_VS_B22.png) · [176 coordinates](PLACEMENT_B22.csv) · [Groups](STRUCTURED_GROUPS.csv) · [Added distances](EXTRA_LOCAL_PIN_DISTANCES.csv) · [All gates](GATES.json).
Partial draft only: inherited94critical distances PASS, fiveadditional local increases and unfinished bank/mirror requirements HOLD. No native PCB/DRC/routing/manufacturing.
''',encoding='utf8')
with(P/'PLAN_AND_LEDGER.md').open('a',encoding='utf8')as f:f.write('Task2: completed second and final adjustment;125changed,94noincrease,15400pairs each0. Task3: independent real-pad audit found5extra local increases, preserveHOLD, no thirdadjustment. Task4: exactlyoneimage exported/viewed. Further coordinates/figures STOP. Pending onefresh finalreview and GitHubhandoff.\nRuling: additional pin-local failure and unmatchedtemplate requirements remain visible; overallPARTIALHOLD, no numerical relaxation or permission to correct outside2passes.\n')
print(json.dumps({'reportBytes':(P/'COMPLETE_B22_RECEIPT.md').stat().st_size,'fiveExtraOpen':len(viol),'budget':B['actual']}))

