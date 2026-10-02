from b31_core import *
import hashlib
a=json.loads((P/'FULL_GEOMETRY_AND_IDENTITY_AUDIT.json').read_text());c=json.loads((P/'MACRO_COMPOSITION_AUDIT.json').read_text())
text='''# SCIENCE_ADK5556_4X4_R21_B31_MACRO_B_CHANNEL_COMPOSITION_CLOSURE_V1
## COMPLETE / PARTIAL-HOLD RECEIPT — CAD0

## Authority and outcome
Full ruling assistant8b60f0ef-4a1c-4e51-b76b-74461c7dcc6f parent565ab528-c339-4d78-ae17-3b56d1c83116: B3 method PASS, A layout rejected, 300min/macro2/placement3/image2 newB31 approved. User continuous PCB/automatic-report authority retained. No old budget inherited. Original MacroB B1 and compact-right B2 assessed; both collision0, final corrected actual-pin score selectsB2. All19 macro anchors fixed across three actual passes. B3-A onlybefore; no U14-only patch, noB2.x old-block coordinate seed.
Complete output is PASS1; unsuccessful pass3 is not complete. PARTIAL/HOLD, no user'svisualselection, candidate-final false, CAD_RELEASED=false.

## Actual offline evidence
'''+f'''176parts/552pads/514assigned/107nets/36ordinaryNC+2emptyJ2MP. Frozen source metadata/footprints/padnumbers/nets copied unchanged; inputSHA allPASS. Offline source evidence only, NOT new nativewarm/cold/netlist audit.
All15400pairs: body overlap0, conservative body+pad proxy overlap0, minimum gap{a['minimumPhysicalGapMm']:.9f}mm. Not actualCAD DRC/manufacturing clearance/routability.
106registered key pairs allnoincrease vsB21, maxdelta{a['keyMaxDeltaMm']:.9f}mm. Includes16RF/CF functionaltap/sensepairs, not fictionaldirectopampnets. Not allpads/routes.
CompleteTIA24role parts and ROW16role parts repeatabilityPASS: actual output/sense-pin midpoint outward quadrants, common role centres under reflections, role-dependent realizable inward rotations, independent fullrole/4channel recomputation. NOT exact mirror of all3pinclampGND/V5pads or routed/performance evidence.
Bodybbox{c['bodyWidthHeightMm'][0]:.7f}x{c['bodyWidthHeightMm'][1]:.7f}mm, physicalaspect{c['physicalBBox']['aspectRatio']:.9f}; priorB3A83.9003192x58.3210984, narrower/taller/closer square. No boardoutline. Largest sampled1mm full emptyrectangle{c['largestSampledInternalEmptyRectangle']['areaMm2']}mm2, excludesbboxedgecells; quantized proxy NOT exact continuousgap or humanbeauty.
Six old-family necessary rigidreuse upperbounds<=70% using distanceinvariants/existingSciPyMILP audit only, no newplacementoptimizer/product. Doesnotproveaesthetics.
31selectedreal same-net edge sumB22{c['B2231EdgeSumMm']:.9f}→B3A{c['B3A31EdgeSumMm']:.9f}→B31{c['selectedRepresentative31EdgeSumMm']:.9f}mm. Not allnets/crossings/routedlength/noise/speed.
'''+'''
## Explicit chain HOLD
ROW0/3 ISO2→J2 +7.308854946961/+7.387876567226mm vsB22; ROW1−.406797118237, ROW2−7.452797618102. ROW0/3 −2.140046558554/−9.080137102919 vsB3A. Below Pro's current~+16mm deterioration, but still substantial: ROW3+106.6% vs old6.93mm. Local conservative+5mm aim is desktop's stricter target, NOT Pro verbatim; failed and retainedHOLD, no after-result threshold relaxation.
J1.1→U9.5 +2.545088044812mm vsB22 (10.829797485560→13.374885530372), −3.921320932045 vsB3A, about+23.5%. SelectedcompactB2 gives continuous powerchain, narrowerbbox/loweroverallscore, a concrete composition rationale, but stillneedsengineeringacceptance. PowerInputNoIncrease=false, not automaticjustificationPASS.
Extra ADC_IN2 R_ADC2→C_ADC2 +.150831741575mm vsB22 (+1.726216093918 vsB3A). All31rows published, four increased vsB22 despite sum improvement.

## Three actual passes, preserved failures
PASS1 complete176, all15400collision0,106keys and completecellsPASS; interfacechainsaboveHOLD. Exactpass1positions/fullCSV/audit retained.
PASS2 commonROWISO inward compactradius attempted, failed NO_LOCAL_POSITION C_ROW_OP: newrolescrowdedV5decoupler. Partial/trace preserved; nofulloutput.
PASS3 reserved bothV5caps from THIS package's successfulpass1, notB3A/B22, thenrebuiltcompletechannel finite templates with commonrole tiers and allfour actualISO2→J2costs. Failed NO_COMPLETE_ROW_CELL_TEMPLATE. Partial/traces/rejectedpairs retained; no claim outsidefinitecandidatesgeometrically/electricallyimpossible. Nofull176from3; availablecomplete only1.
Actualmacro2/2 placement3/3 images2/2. STOP B31_PLACEMENT_HARD_QUOTA_USED_REPRESENTATIVE_CHAINS_HOLD. No4thpass/3rdimage/extramacro/newsource/CAD/native/routing/outline/simulation/APIresearch/GUI/manufacturing/procurement/bench/Gerber/localGit/system.

Multi-pad score genuinelyfixed and used in cell/freeplacement: eachmeaningfulpadwithICsame-nettargets choosesnearestthenallpads sum, includesEN/control/input/output/supply, excludesGND/unmapped.106functionalRF/CFbounds separately checked; notfalse directmapping. First-pad-sensitive test oldomission0 vs expected5 RED then fixedsum5 GREEN3tests; nottext-onlyfix/oldcoordsreuse.
Initialmacroscore wrongU4CMD3 NC15 correctedactual18; U11V3V3pin4→V5 corrected tofunctionaldivider sense1. Directsame-net validation before176generation. Same2macrocoordinates frozen, initialaudits/selection retained BEFORE_NET_ENDPOINT_FIX, rescoredsamecandidates; no3rdmacro. Largestemptyrectangleoriginallycountedboundaryband, correctedexcludeedgecells, oldmetricretained. Localimplementationomissions, nottoolbug/physicalinstability.
PASS1 codebackup occurredafterpass2edit; renamed construct_b31_PASS2_ERA_NOT_PASS1_EXECUTED.py, notexactpass1executedbytes. Pass1 actualpositions/trace/audit retained. Currentconstruct_b31.py ispass3version, notone-clickresume/init/resetbudget. Construction only explicitmainreservation. No new source.

## Visuals
Two allowed FINAL-named PNGs generated and actuallyviewed. B3A_vs_B31_FINAL.png same-mmcomparison, B31_FINAL_NO_COPPER_AND_CELLS.png actual176/552, full8cellcontours, analog/digital/powerarrows. FINALfilenameProrequired; contentsclearlycompletePASS1/HOLD, notacceptedfinal/nativeboard. Dashednaturalbodybbox notboardoutline; arrowsassociationsnotcopper. Passivedesignators viaPLACEMENT_B31.csv andALL_552_PIN_MAP_B31.csv. SmallpowerIC/padlabels partlyoverlap, no3rdimagepolish. Central/lowerblank and concentratedADCsupplies remain; notclaimScienceaesthetic achieved.
FFC2005290081 eightROW/COL+2emptyMP frozen, planningkeepout0; exactactuator/bodydatum/mating/cabledimensionsHOLD. UserconfirmedthinFFC/FPCtype, notpersonallyspecificpitch. No new mechanicalsource.

## Review, scope and next decision
One fresh-context finalreview/disposition appended, no newcoordinate/image afterquota. InputSHAunchanged. Allownedsource/failure/report/readableattachments directpublicfile+manifestZIP, thirdpartybulk/accountSQLite/credentials/otherprojectexcluded. Fixedcommit/publicSHAverification suppliedafterupload. Publicconsistency doesn't prove Proreadattachments.
Please judge actualpass1 completecells/visualcomposition and fourgrowthrows. Either explicitlyaccept disclosedROW/J1proxyvariances underPro~16mmcondition and awaituseractualvisualchoice, or issueONEconcretefiniteROWcell+V5capco-placementscope. No additionalMIMO/API/tooltheory/arbitraryfullvariants. Desktop+5aimfailure isnotliteralProrefusal, nor desktopacceptance.
At USER'S EXPLICIT REQUEST for moreboundedexecutiontime/count/autonomy, request ONLY IF additionalcorrectionneeded: 240min (ROWcell+V5cap45, conditionalfixedmacroplacement75,fullaudit40,images/delivery80); macro0 unlessProexplicitlynew2essential,placement<=2,images<=2,newsource/CAD/native/routing/outline/toolAPIresearch/simulation0. Ordinarynecessaryengineeringimplementationautonomous,106bounds/full4channelroles/identity/J2frozen; requestonlynotSTOPrelease orplatformquotaexpansion, noadditionalbudget-onlymessage.
Old480minnative request remainsconditionalactualuserselection + explicitsingle newnativeengineeringruling. Offlineimageacceptance isnotCADauthority.

END-OF-COMPLETE-R21-B31-MACRO-B-CHANNEL-COMPOSITION-BLOCKED-RECEIPT
'''
(P/'COMPLETE_B31_RECEIPT.md').write_text(text,encoding='utf8')
(P/'README.md').write_text('# B31 Macro B full-cell offline placement — PARTIAL/HOLD, CAD0\n\nRead COMPLETE_B31_RECEIPT.md and GATES.json. Only PASS1 complete. PASS2/3 failures retained, allbudgets exhausted. Two FINAL-named images show PASS1/HOLD, not accepted/nativePCB.176/552/514/107/36+2MP,15400collision0,106keysnoincrease,completeTIA/ROWroletemplates. ROW+7.31/+7.39mm and power+2.545mm vsB22 requireexplicitacceptance. FullCSV/JSON/actualtrace/backups published; noaccountSQLite/thirdpartybulk/credentials.\n',encoding='utf8')
print(json.dumps({'reportSHA256':hashlib.sha256(text.encode()).hexdigest().upper(),'partial2':len(json.loads((P/'PLACEMENT_PASS_2_PARTIAL.json').read_text())['positions']),'partial3':len(json.loads((P/'PLACEMENT_PASS_3_PARTIAL.json').read_text())['positions'])}))
