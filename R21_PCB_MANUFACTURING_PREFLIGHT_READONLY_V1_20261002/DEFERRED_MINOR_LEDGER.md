# Deferred minors — single final review
Critical0 / Important0 / Minor3. All three remain visible, no second review/CAD/scientific rerun and no polishing of tools. FINAL_REVIEW.md is unchanged reviewer record.

1. PGOOD text mentions R_RST.2; actual access CSV/green plot index7 is R_J3_5.2. Both are proven PGOOD in the frozen pad table. For the delivered plotted candidate use **R_J3_5.2**, not the prose alias. This is a reference consistency minor, not a different net or release.
2. ASSEMBLY_GEOMETRY_SUMMARY.nativeDrill20PTH also contains U6 zero-width SMD hole records. Count only positive native hole widths on through-hole pads; actual header PTH=20. Do not use this raw array length as manufacturing drill count or generate drills from it.
3. OVAL geometry is plotted/compared by a rectangle envelope in the helper. Consequently screenshots are approximate and local mask/body screens do not establish true rounded-land contours, Gerber or fab DFM. Main small-mask bridge results concerned U5/U9/U10 RECT/POLYGON, not U7 OVAL. Exact raw footprint PAD definitions are retained for authoritative future export.
