# Retained failures and execution control

1. importChanges returnedtrue but actual PCB remainedempty in a fresh read. No repeat import.
2. First20-part command exceeded Windows command line limit WinError206; no child started. Reduced payload to existing deviceUUID/libraryUUID associations; no installation/account change.
3. Initial audit accessed undefined API manufacturerId and compared original globalUUID to automatically remapped localUUID. Corrected audit to resolved exactMPN device name/footprint name plus all actualpad numbering/nets; first error proof retained. Library identity is not a new manufacturer qualification.
4. Board-outline straight line method rejected layer11. All176 placement moves had happened, but no outline/save in that invocation; created one closed officialpolyline outline and explicitly saved, then verified actual positions.
5. Native autoRouting for20 criticalnets timed out49.75s, may stillrun. Onefreshread found0 lines/1 outline; closed only ownheadlesssession officially before restart, did not rerun autoRouting. No unrelatedprocess killed.
6. Bounded local ordinaryL1 path pass saved93 actual lines +L2GND boundary. NativeDRC reported2 clearance failures5.9mil; static initial assumption thesewerevertical failed before mutation. Readactualdiagonal coordinates, changedonly2 segments by0.6mil in bothaxes, finalnativeDRC0clearance. Final453 detailed errors retained.
7. NetlistComparison107 entries with emptyPCB members; filled176originaluniqueIDs, officialexplicitJLCNetlist update returnedtrue but didnotresolve comparison. DeprecateddefaultgetNetlist call timedout49.75s; closed onlyowned session; switchedonce to known actualFileexport+explicitJLC interface. No API/SDK internals, cache/DB/profile or UI research.
8. Stop at realPCBnetlist/complete-routing blocker. Fournewheadlesssessions were officiallyclosed. No Gerber/order/PCBmanufacture/bench; no science or simulation.

This package does not fulfill a fullyrouted firstPCB. It delivers a verifiable floorplan/localroutes and precise remaininggate for a single engineering decision. No old schematic/scientific package reopened.
