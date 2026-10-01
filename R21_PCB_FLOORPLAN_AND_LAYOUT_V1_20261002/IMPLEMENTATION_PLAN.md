# R2.1 PCB first review design

User authorized four-layer lab rectangle; no confirmed enclosure/holes. Accepted schematic fbb7c0ed5f322f078583fadbdb353efe835e4c01 is immutable.

1. Audit 176 component symbols/physical pads and all 514 connected pins / 36 NC from official native PCB import.
2. Create 4-layer review PCB, J2→ROW/TIA→ADC analog area, references/decoupling local, MCU/SPI opposite side, input/protection separate. Plan practical clearance/width/stackup, no AGND/DGND slit.
3. Place devices and locally route feedback/decoupling before remaining board connections; retain L2 continuous GND, L3 power/slow digital. No automatic placement.
4. Actual net/pad/DRC connectivity verification, cold reopen, native review exports and readable layer renders. Report unresolved DRC/unrouted precisely; no manufacture release.
5. One fresh-context whole-package review, bounded fix pass; full GitHub new directory/fixed commit once plus successor reply monitor.

Ruling: use dedicated new PCB workfile, not Git worktree/checkpoint; user forbids local Git writes and schematic baseline changes. Retain all evidence, no cleanup.
Ruling: static helper scripts receive only meaningful structural checks; do not initiate new scientific tests or tool research. Official CLI document use is limited to the needed PCB operations.
