# B3 pinout-driven placement review draft

Start with COMPLETE_B3_RECEIPT.md and B22_vs_B3.png. This new layout has all176parts and all19macro anchors changed, but U3/U14 pad-proxy collision blocks acceptance. No native PCB or routed copper exists in this package.

- B3_NO_COPPER.png / B3_PINOUT_AND_SIGNAL_FLOW.png: two other quota-limited review images, not fabrication documents.
- PLACEMENT_B3.csv / ALL_552_PIN_MAP_B3.csv / PIN_FUNCTION_GRAPH.csv: complete readable positions/pins/nets.
- FULL_GEOMETRY_AND_IDENTITY_AUDIT.json / KEY_PIN_DISTANCE_B3.csv / OLD_BLOCK_RIGID_REUSE_AUDIT.json: all176 geometry,106keypairs,6familyrigidreuse.
- MACRO_A/B/SELECTION and PLACEMENT_PASS_1/2/3 logs: actual failures and construction; no fourth pass.
- REFERENCE_CASE_RULES.md / OFFICIAL_SOURCE_REGISTER.json: verified official reference rules and original URL/SHA. Third-party bulk files stay local, not included in public ZIP.
- PRO_B3_RULING_FULL.md / PLAN_AND_LEDGER.md / GATES.json / EXECUTION_BUDGET.json / FINAL_REVIEW.md / REVIEW_DISPOSITION.md: scope, budget and review lifecycle.

Historical initialization/construction/render scripts are evidence, not one-click rerun recipes: budgets are closed and exhausted. Do not reset or execute them from this review artifact.
