# Deferred minor — descriptive netlist text encoding

Fresh-context final review found a warm/cold API netlist-string difference at `/components/gge83/props/Description`: the U+FFFD replacement-character position differs. Actual parts, native ATTR and PAD_NET records remain strictly identical. This is descriptive-text integrity, not an electrical connection/net identity change.

Original warm/cold netlist strings are preserved in full captures. No description, native source, or tool was repaired, and no new CAD/test/export was run for this Minor. Do not claim the entire API netlist strings are byte-identical. Full final review is in FINAL_REVIEW.md. It does not block native electrical PCB review readiness.
