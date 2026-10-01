# R21 invariant MIMO — method qualification HOLD

[Complete Chinese receipt](COMPLETE_INVARIANT_RECEIPT.md) · [Ruling](PRO_INVARIANT_RULING_FULL.md) · [Budget](EXECUTION_BUDGET.json) · [Gates](GATES.json)

52 actual SPICE processes /104 OP+AC analyses;9 numerical diagnostics incl5 offline; normal switchingtransient0, two optran DCinitialization cases, native0. Method/HOLD; no physical instability or stable verdict.

- [All cases and failed analyses](CASE_EXECUTION_INDEX.csv), original cases/results/models alongside96 percase readableCSV.
- [Three analytical fixtures](FIXTURE_QUALIFICATION.json), [N1 object scope proof](N1_OBJECT_CONTRACT_PROOF.json).
- [Initial repeatedcolumn fail](ACTUAL_REPEATED_COLUMNS.json), [Full actual-column fallback scope](EXTENDED_MEASUREMENT_PLAN.json).
- [Open Gc CSV](results/openGc_MATRIX.csv), [Closed Gc CSV](results/closedGc_MATRIX.csv), [Lowfreq/QZ/fixedscales](LOW_FREQUENCY_QZ_AND_SCALING.json).
- [Fullnetwork scalarcrosscheck scoped sources](FULL_NETWORK_SCHUR_TIAN_CROSSCHECK.json): TIA loaded2port PASS does not certify failed direct series/shunt Tian.
- [Finite-axis determinant proxy](DETERMINANT_PROXY_SUMMARY.json), [all proxy curves CSV](results/DETERMINANT_FINITE_AXIS_PROXY.csv): zero proxy is not a certified fullRHP contour.
- [Condition plot](plots/GC_CONDITION_ALL_FREQUENCIES.png), [Scalar scope plot](plots/SCALAR_CROSSCHECK_SCOPES.png), [Proxy phase plot](plots/FINITE_AXIS_PROXY_NOT_CERTIFICATE.png).

Reference G0/internal poles/true RHP contour and low-frequency forward spectrum unqualified; no native or bench release. Source SHAmanifest and ZIP added at publication; individual evidence files remain readable.
