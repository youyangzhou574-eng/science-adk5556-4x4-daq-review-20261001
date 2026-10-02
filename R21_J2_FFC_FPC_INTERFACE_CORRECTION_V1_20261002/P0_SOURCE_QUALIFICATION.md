# Pro20 J2 FFC source qualification

Default is Pro20 authorized Molex2005290081 with154670229. User confirmed FFC/FPC flip-slot type only; existing cable/pitch not confirmed. No inventory or actual mating claim.

S1 connector exact product page, S2 manufacturer salesdrawing bundle2005290002/2005291002 PSD000 revB2024-05-29, S3 exact cable product page, S4 cable salesdrawing154670001 PSD000 revA2023-04-04. S2 URL names0061 but table explicitly includes2005290081:8circuits,A13.2/B7.0/C11.6mm. Four logical sources reserved; failed transport and duplicate URL forms belong to the same sources, not new technical documents. Local full PDFs/HTML retained only; public own summary+links+hashes.

Visual inspection of original rendered pages: solder pads0.40x1.00mm,1.00mm nonaccumulative pitch; fitting nails2.00x1.30mm. Outer nail edge3.80mm beyond end signal, inner edge1.80mm; nail centre2.80mm beyond endsignal. Signal pad bottom to nail top1.55mm, so nail centre2.70mm toward insertion side. Body A13.2mm, depth5.30mm; closed height1.9±.2mm and opened actuator approximately3.95mm. Right-angle FrontFlip bottom-contact; FFC enters at front, conductors toward PCB. Fitting nails are mechanical solder anchors, no electrical signal assignment; no arbitraryGND.

Cable exact table154670229:8circuits,102±3mm,TypeA same-side contacts,1.00±.05mm pitch,0.30±.05mm stiffened thickness; drawing note explicitly mates with connector series200529. Exposed contact nominal3.5mm. Cable exposure tolerance±.5 differs connector recommended±.3: record vendor confirmation for manufacturing instead of inventing worst-case qualification. Nominal matching and manufacturer's explicit family mating declaration support review ECO; real cable/equipment fit remains untested.

Manufacturer drawing has no numbered pin1 label in the views. Project pin1 convention will be marked on the new footprint and orientation drawing: leftmost rear solder pad in unrotated top view, then1..8 left-to-right; from insertion/front view this reverses. The project does not claim a manufacturer mouldedpin1 mark. Board orientation will make conductor1/ROW0 explicit, not swap row/column nets or assume TypeA guarantees remote numbering.

P0 engineering entry qualified for exact manufacturer-derived10pad SMT footprint (8signals+2mechanical) and bounded local mechanical check. Full connector/cable manufacturing reliability, supplied part verification and user existing cable compatibility remain pending.

Final review limitation: landpattern source remains official-derived, but manufacturer body datum relative to signalpad row is not qualified. Native assembly artwork is illustrative only; neighbor clearance/flip/body gateHOLD. Do not interpret P0 entry as mechanical release.
