# PCB routing closure — approved ruling 12

Authority: PRO_ROUTING_CLOSURE_RULING_FULL.md, assistant 14bc7e77-00c2-40ce-b159-48872af1092b.

Use the dedicated copied project. No local Git writes. Preserve all inputs and unsuccessful evidence.

1. P0 (120 min): inspect existing pad/trace geometry; engineer selected short TIA, ROW and reference connections on L1. Preserve pin nets and physical identities. Check native DRC after a meaningful analog stage.
2. P1 (120 min): connect remaining ordinary signals with controlled explicit paths and layer transitions. SCLK stays outside the analog/input/reference region. No full-board autorouter.
3. P2 (45 min): direct wider supply paths, continuous L2 GND and local ground returns/stitching. No split ground.
4. P3 (45 min): detailed native DRC classification, full pad/identity comparison and cold reopen. Retain violations and do not change rules to hide them.
5. P4 (30 min): native review artifact, readable copper views and auditable receipt. Publish new project directory and immutable GitHub commit; one internal handoff with successor reply owner and monitor.

Hard limits: 3 sessions, 12 saves, 4 capture/audits, 4 DRC, 2 review exports; 360 min total. No import, schematic changes, simulations, procurement, manufacture or powerup. STOP for a required frozen-input change or unexplained netlist error/topology short. Existing unconnected copper is work remaining, not a net assignment defect.

For CAD edits the verification is actual native DRC and warm/cold connectivity, rather than artificial tests mirroring ordinary geometry edits. One independent final review follows actual deliverables.
