# C simplification engineering plan and ledger

Spec: PRO_C_RULING_FULL.md; assistant 555cc3cd-2a40-4ec7-903d-7d0c60c7d41b, parent bec194ac-23da-465a-84e5-6e5989620c5b.
Goal: qualify the single-row-driver C candidate before any new PCB work. The proposed 83 count is not a frozen or implemented BOM.
Architecture: one remote-feedback OPA388 and dual mux, four conventional TIAs, existing ADS8684/reference/MCU; integrated 3.3 V power chain. Tech: official source inspection, existing ngspice47 and unedited TI macros, normal JLCEDA CLI when admissible.

## Constraints and rulings
- 360 min total, C0 60 / C1 120 / C2 110 / C3 40 / C4 30. Exact count limits are in EXECUTION_BUDGET.json.
- Ruling: use an isolated new directory, preserve old artifacts, no Git/worktrees/commits or workspace cleanup. Explicit E:\open user instructions override the skill's Git workflow.
- Ruling: inline implementation under the user's continuous authorization and Pro's full C release; no duplicate approval of this already supplied plan.
- Ruling: do the first bounded C2 row-driver screen before C1 CAD mutation. C0 consumes real datasheets; C2 consumes qualified pin/topology inputs. A failed basic screen prevents needless schematic work. Total and phase time/count limits remain unchanged.
- A is fallback reference only. No automatic A or silent restoration of old architecture.
- A STOP is sticky even if counts or time remain. Preserve failed cases; no unlimited diagnostics.
- No native PCB, routing, pour, Gerber, manufacturing, procurement, bench, flashing, installation, local Git writes.

## Tasks and interfaces
- [ ] C0: source pin/power/blank/reference/protection qualification; SOURCE_REGISTER.csv and C0_RECEPTION.md feed the schematic and test cases.
- [ ] C2 early screen: real OPA macro with selected-row drive/sense and four resistive loads; record OP and blank-to-enable TRAN separately. This is a bounded screening fixture, not four-TIA coupled validation.
- [ ] C1, if admissible: one native schematic copy with explicit designator/pin-net change register; actual capture and ERC/PDF within limits.
- [ ] Remaining C2, if not STOP: finite matrix/TIA/settling/power/off checks. No performance or physical qualification inferred from numerical completion.
- [ ] C3 only when electrical gates pass: one offline placement, at most 2 adjustments and 2 images.
- [ ] C4: full success or blocked receipt, evidence and exact spent budget, single fresh-context final review, one normal GitHub delivery and reply owner/next check/monitor.

## Review focus
Blank disconnects the feedback path; unselected-row voltage depends on column feedback; parasitics are unknown bounds rather than measured cable values; LP5912 PG is undefined below VIN=1.6 V; board-off debug injection and actual MLCC effective capacitance must not be inferred from nominal ratings.

## Fresh findings
2026-10-02: original Kim2016 Type III Section 3 explicitly routes output and feedback through separate synchronized switches. Unselected rows return to VREF through column circuits. This agrees at topology level; it does not certify this hardware's blank/recovery dynamics.
2026-10-02: TMUX1109 SCDS406A 2024 has active-high EN; low turns all switches off. PW pins DA8/DB9, S1A4/S1B13, VDD14/VSS3/GND15. New official source 1.
2026-10-02: LP5912 SNVSA77D 2016 integrates PG/reverse protection/discharge, but PG is explicitly undefined for VIN<1.6 V. New official source 2.
2026-10-02: BAT54XY 2026-07-16 is two isolated series diode pairs (four junctions, six pins), suitable for two rail-clamped signal centers; new official source 3, protection candidate 1. Do not substitute a pure ESD device for this path.

## Final phase dispositions
- C0: PARTIAL/HOLD; four sources and two protection candidates consumed. Whole-rail power and low-VIN PG qualification not closed.
- Early C2: completed bounded single-row local screens.
- C1: one isolated baseline copy/capture/audit; no mutation/save/ERC/PDF. C ECO NOT IMPLEMENTED.
- Remaining C2: PARTIAL/HOLD; three full-matrix OP failures, one PZ failure, and explicit step OP branch inconsistency retained. No additional science after STOP.
- C3: NOT ENTERED, zero placement/image.
- C4: full blocked receipt and one fresh-context review completed; single final documentation pass, publication and handoff in progress. No invented cumulative phase times.
- STOP: C_POWER_OUTPUT_CAPACITANCE_AND_LOW_VIN_PG_QUALIFICATION_HOLD at 2026-10-02T19:08:07.597704Z.
- Original reply monitor deleted after full C scope consumed; successor monitor required after this delivery.
