# B2.2 structured-channel array placement — partial visual draft / HOLD
Only circuit project SCIENCE_ADK5556_4X4_DAQ_REPLICA. Full completed ruling assistant3d968530-1342-4bbd-9af0-dae4f321ab20 / parenta9ed76f1-da40-41ef-822c-7751b8071c0c is PRO_B22_RULING_FULL.md.
User asked for Science-like regular passive arrays within functions; no additional area compression. Earlier B2.1 conditional480min native scope stays dormant and is not automatically migrated to B2.2.
## Outcome
A complete176-coordinate B2.2 visual draft was generated.125 positions/orientations changed, all15IC+4connector macro anchors exactly fixed (plus6 short-local parts). Body bbox71.0000204x63.5000124mm unchanged.552pads/514assigned/107nets/36NC+2emptyMP remain identical; no native PCB, values, signal mapping, footprint or board-frame writes.
All15400 different-component pairs independently examined for body and conservative pad-proxy; both0area overlaps >1e-8mm². FFC planning keepout0; exact actuator/mating not qualified.
Inherited94 actual IC-pad→passive-pad distances all no increase (max0; largest reduction3.869006mm). These include RF/CF functional paths through series resistors, not false direct-net claims.
However additional real-net local checks find five increases. No universal decoupling/high-Z distance PASS. Overall candidate is PARTIAL_VISUAL_HOLD, not CAD-ready. No third adjustment or second image.
## Implemented geometry
TIA/ROW same role now consistent rotation and pin-facing mirrored2+2 patterns. Channel order follows physical IC perimeter0→1→2→3, not falsely four left-to-right columns.
ADC inputs are an actual4-column2-row group at2.4mm pitch, with correct pin identity. REFIO/DVDD local cap rows align. VCM/VEX HF/FB/ISO centers use central positional mirror around U3; copper layers/pin identity are not mirrored.
Divider banks, MUXpulls, Power control resistors, supervisor divider and debug protectors use local regular rows/columns.56declared groups include singleton local placements and3retained exceptions: this does not mean56multi-element arrays. STRUCTURED_GROUPS.csv gives all actual membership, directions and pitches.
No optimization library, EDA API experiment, auto-layout plugin or new algorithm family. Only finite local templates tested with actual pad/collision gates.
## Requirement coverage and limits
|Requested group|Result|Actual evidence|
|---|---|---|
|TIA/ROW four-channel roles|PASS_PIN_FACING_2PLUS2_EXCEPTION|8 groups same rotation and symmetric two pairs; U1/U2 opposite-side pins prevent a selected feasible single4line under strict baseline distances|
|ADC R/C4x2 inputs|PASS|one common four-column2row pitch2.4mm; real94checks no increase|
|ADC AVDD9/30 and REFCAP cap banks|HOLD_LOCAL_FEASIBILITY|three banks retain B2.1 baseline after finite equal-pitch templates fail strict distances/collision|
|ADC REFIO/DVDD cap banks|PASS_OFFLINE_ROW|REFIO y-row3.299995; DVDD x-row3.299995mm|
|BIAS VCM/VEX paired placement|PASS_POSITIONAL_CENTRAL_MIRROR_ONLY|HF/FB/ISO centers centrally paired about U3; this is not a footprint/net reflection|
|reference divider banks|PASS_ROW_AND_COLUMN|two five-member banks, not one entire divider row|
|POWER common mirrored U9/U10 templates|PARTIAL_ROLE_ROWS_MIRROR_HOLD|both8member control banks rows, but pitch3.3000204 and2.3750032 differ; not exact paired mirror|
|DIGITAL U13/14/15 IC and cap rows|PARTIAL_LOCAL_ANCHORS_RETAINED|IC macro anchors retained; no new common IC row/2x2 template is implemented|
|J3/J4 identical local template|PARTIAL_PROTECTOR_ROWS_TEMPLATE_HOLD|individual resistor/diode rows passed; J3 resistor vertical versus J4 horizontal, not same complete template|
|all critical local pin distances|HOLD_EXTRA_FIVE|94 inherited pass;5 of10 added real-net local checks increase by.09155 to1.35178mm|
## Added pin-local checks — five open items
No relaxed engineering threshold was invented. The local conservative rule is B2.1 +1e-6mm; a failure here is a coordinate limitation, not physical instability or measured electrical error.
|IC pin|Passive pin|B2.1mm|B2.2mm|Delta mm|
|---|---|---:|---:|---:|
|U11.1|U11_SENSE_C.1|2.628979|3.980762|+1.351783|
|U11.5|U11_CT_C.1|3.221233|4.015970|+0.794737|
|U12.4|U12_VDD_C.1|7.618681|7.710231|+0.091550|
|U12.1|U12_SENSE_C.1|2.628979|3.294073|+0.665095|
|U12.5|U12_CT_C.1|7.200570|7.398292|+0.197722|
All10added comparisons are in EXTRA_LOCAL_PIN_DISTANCES.csv. U13/U14/U15 decoupling and other additional checks not listed here did not grow.5failures cannot be hidden behind the inherited94PASS.
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
