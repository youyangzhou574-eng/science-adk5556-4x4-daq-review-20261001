# J2 manufacturer-source qualification (R17)

User requirement: single row, 8 positions, removable cable plug; not eight wires soldered directly to board.

Selected header: Molex 1718560008 (171856-0008), vertical KK254 friction lock. Housing: 22012087 / 22-01-2087, 2695-8R. The manufacturer-authored exact-housing product sheet explicitly lists 171856/171857 as mating series; customer drawing 26950000-SD A3 table includes 22-01-2087. It has a friction ramp but no RP polarizing ribs: do not promise fully keyed/impossible reverse insertion.

The same reserved manufacturer customer drawing identities were retrieved from public distributor mirrors after official-host timeouts. No fifth independent engineering source was added. Header file: SD-171856-0001, first page B2 and continuation table B1 (2018), not claimed current B3. Housing drawing 26950000-SD A3, sheets 1/2 and 2/2 in pages 5/6 of a 5-position product bundle; only the shared drawing and its explicit 8-position table are used, not that bundle's 5-position product specifications. Both drawings rendered and visually inspected locally.

Header: 8 pins, 2.54 mm pitch, 17.78 mm pin span; 20.17 mm body length. Drawing side view: 6.35 mm body width with pin centre 3.10 mm from lock side and 3.25 mm from opposite side. Recommended finished plated PCB hole 1.14 +/-0.05 mm. Header group 171856-0002/-0012 includes exact 0008 with no void: 12.95 mm overall pin, 7.44 mm mating length, 2.34 mm PCB tail. Manufacturer drawing does not prescribe copper pad diameter/courtyard: those are explicit board-design choices, not manufacturer dimensions.

Housing: 8 positions, 17.78 +/-0.13 mm span, 20.88 mm length, 4.82 mm cross-section width, 12.7 mm housing height; minimum pin insertion depth 6.4 mm. Series 2759/6459/41572 and later 4809/8088 terminals are permitted, 22-30 AWG and maximum 1.57 mm insulation diameter per shared drawing. Exact terminal MPN remains PENDING actual AWG/insulation; Pro's terminal examples have not been independently qualified here.

Critical numbering note: header circuit 1 may or may not align with mating housing circuit 1. Harness pin order must trace actual mating contacts to PCB pin 1 (ROW0), never blindly assume molded numbers align. Actual PCB pin1 has the square pad at coordinates x196.9/y1185.4mil, the lower end in the current top-view orientation (EDA positive y is upward). Do not confuse the coordinate ordering with the visual upper end. Nets1..8 remain ROW0,ROW1,ROW2,ROW3,COL0,COL1,COL2,COL3. User's existing unspecified cable compatibility remains unverified; this is a new explicit matched standard.

Current Molex product pages say Limited Information Available; do not inherit the ruling's unverified current Active claim or promise availability/manufacturing release. Procurement/manufacture/power-up remain zero.

Official URLs: https://www.molex.com/en-us/products/part-detail/1718560008 ; https://www.molex.com/en-us/products/part-detail/22012087 . Mirror provenance and SHA in DRAWING_MIRROR_FETCH.json. Full third-party hosted drawings/extracts retained locally; public delivery provides source links, bounded dimension notes and source hashes; full mirrored PDFs, full-page PNGs and bulk extracts remain local only.
