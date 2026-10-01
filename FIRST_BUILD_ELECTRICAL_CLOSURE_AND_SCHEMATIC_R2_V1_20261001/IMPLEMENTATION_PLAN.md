# R2 Electrical Closure and Schematic Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Correct identified electrical defects, implement explicit protection paths, validate the achievable conditions, and deliver an audited R2 native schematic.
**Architecture:** Keep four driven rows and four continuously closed column TIAs; add hardware power/fault qualification and revise feedback and decoupling. Keep reference and signal/fault paths explicit and preserve all V1 evidence.
**Tech Stack:** Windows PowerShell; Python 3.13 numpy/scipy; existing manufacturer models; LCEDA-Pro 4.1.60 official CLI; GitHub REST report publication.
**Spec:** PRO_R2_GATE_FULL.md (assistant 719bc515-52e2-4bf8-a0f4-44abffa0c95c).

## Global Constraints
- E=0.25V; Rf=4.99kΩ; 0.8–8kΩ; 4×4, eight leads; 100 complete frames/s.
- 5V analog, 3.3V digital. No new core amplifier/ADC series without a consolidated change ruling.
- P0/P1/P2/P3/P4 active limits 15/60/90/60/15 minutes; total 240.
- P1 ≤3 revisions, ≤16 primary sources, ≤4 new model packages, ≤6 new protection/monitor function classes, ≤12 new library identities, ≤60 reads/searches.
- P2 DC≤256, AC≤96, normal transients≤96, fault cases≤96, one offline SPI state machine.
- P3 one R2 project, ≤6 pages, ≤3 owned sessions, ≤8 saves, ≤4 actual File captures/full audits, ≤3 ERC/DRC, ≤3 PDF exports with all-page visual QA.
- V1 read-only. R2 works in this independent directory and its dedicated native project.
- No local Git writes, manufacture, procurement, bench power, third-party installation, or system/cache/profile/activation edits.
- Ruling: continuous native execution is already authorized; skill plan-review/commit/worktree suggestions do not override user authorization or the ban on local Git writes. Use artifact copies and a local progress ledger instead.
- Simulation executors are checked once within P0. If unavailable, stop adaptation and preserve model-ready testbenches plus analytical results with corresponding HOLD.

## Review Focus
1. All-800Ω row load with 1kΩ isolation: old 300µs settling counterexample must be reproduced before selecting a replacement.
2. COL hard edge through Cf to output: input sense resistance alone must not be credited as limiting this path.
3. Power loss/reversed sequencing: supply reverse current and digital phantom power need actual paths and bounded evidence.
4. Fixed calibration with asymmetric/changing eight-wire resistance: do not recalibrate per validation case.
5. Native field/NC/network integrity and readable drawing: verify saved/reopened native data and every rendered page.

## Task 0 — freeze inputs and execution conditions
Files: P0_INPUT_AND_EXECUTOR_CHECK.json; V1_INPUT_HASHES.json; R2_WORKING_INPUT.eprj2; EXECUTION_BUDGET.json.
- [x] Verify V1 native exact bytes/SHA and current immutable input-file hashes.
- [x] Check existing SPICE executors and compatibility of the two original OPA4388 models once; record paths/formats, no install.
- [x] Preserve V1 and make one R2 input copy.
Produces: verified input records and simulation availability classification consumed by Tasks 1–2.

## Task 1 — corrected design and protection
Files: R2_CHANGELOG_AND_BASELINE.md; R2_DETAILED_CIRCUIT_AND_PROTECTION.md; R2_PLAN.json; R2_PLANNED_PIN_NET.csv; SOURCE_REQUIREMENTS.json.
- [x] Verify ADS8684 reference and supply decoupling requirements, LDO effective capacitance, OPA output/input limits, and switch power-off behavior using primary sources.
- [x] First write analytical regression checks: old Rs=1k/Rb=10k/Ch=1nF/all800 case must exceed 100µV at 300µs; replacement must meet screening over defined loads.
- [x] Jointly select feedback, isolation, actual hardware monitoring/disabling and reverse-current control. Record every value and all uncompensated fault paths.
- [x] Bind each added native device to an exact manufacturer model, footprint and pin map; otherwise mark a library gap and stop the dependent placement.
- [x] Freeze normal and fault connections before native creation.
Produces: R2 plan and case/model assumptions consumed by Tasks 2–3.

## Task 2 — electrical and timing verification
Files: analytical_validation.py; fixed_calibration_validation.py; spi_state_machine.py; R2_VALIDATION_REPORT.md; cases/results JSON/CSV; model testbenches.
- [x] Reproduce V1 row/TIA/ADC analytical counterexample independently and verify revised candidates.
- [x] Freeze one calibration at declared conditions; validate asymmetric wires and post-calibration contact changes, input bias, thermal noise, standard error and correlated ADC calibration error; use conductance for allocation checks.
- [x] Check all normal endpoints/currents/headroom including added protection drops.
- [x] Execute compatible manufacturer AC/transient/fault models if an executor is available; otherwise deliver precise ready-to-run testbenches and HOLD, not a macro-model PASS.
- [x] Bound all fault current/energy paths including Cf edges, reverse rails and digital injection; check dissipation for 60s analytically and disclose transient/model/physical gaps.
- [x] Run offline state-machine tests for command/return channel, dummy handling, invalid data within 10ms, reset/power sequencing and recovery only after two valid frames.
Produces: PASS/FAIL/unverified matrix, accepted revised parameters and final native input.

## Task 3 — native R2 and cold reopen audits
Files: R2 native eprj2; R2_REVIEW_ONLY.pdf; true exported netlists; connectivity/ERC/visual audit JSON/MD.
- [x] Create one independent R2 working project from the verified V1 copy or same real native components; do not edit the V1 project.
- [x] Place all corrected and new circuits across ≤6 pages; explicit networks and readable feedback routing.
- [x] Capture an actual File netlist and compare every connected pin/NC, cross-page net, exact native device fields and footprint source correspondence.
- [x] Save, close owned session normally, cold reopen, recapture actual File and rerun full integrity checks.
- [x] Obtain actual ERC warning contents/location; preserve unresolved details honestly.
- [x] Export ≤3 PDF versions and render/inspect every page. Fix overlap without hiding required text.
Produces: review-ready editable R2 plus verified persistence and bounded ERC/visual results.

## Task 4 — complete single GitHub delivery
Files: R2_EXECUTION_SUMMARY.json; R2_MANIFEST.json; complete report and readable evidence index; delivery receipt.
- [x] Verify all file hashes and scan for credential-shaped/unrelated private data.
- [x] Publish one new R2 directory/commit in the existing independent circuit repository; retain V1 fixed commit.
- [x] Verify public remote files/important download hashes.
- [x] Send one short internal handoff with directory, fixed commit, summary, complete report and attachment index. No split report, no repeated in-flight send.
- [x] Record actual budget, owned-session closure, all HOLD and next required decision.


Completion grading: checks executed to their stated bounds; macro/whole-board/capacity/ERC/drawing/native metadata/hardware gates HOLD. P4 delivery pending at freeze.
