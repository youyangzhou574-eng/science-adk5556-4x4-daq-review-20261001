# Manufacturer-model benches — NOT EXECUTED

Retained TI OPA4388 PSpice model (five terminals IN+ IN- VCC VEE OUT), unmodified. P0 did not confirm an installed compatible executor. These files have not been parsed or run by SPICE and are not guaranteed portable. No substitute ideal-opamp simulation is reported as macro-model validation.

The coupled 4×4 all800 bench includes four driven rows, four TIAs, 1k row/TIA isolation, row4.99k/100p, TIA4.99k/2.2n, 10k sense, 100R/10n ADC filters and1n line capacitance. It omits lead resistance; 0–0.1ohm lead sweeps, 8000ohm endpoints, temperature/model corners, VCM/VEXC actual buffers, ADC sampling kickback and reference/current protection models must be added by the eventual executor. It does not model TMUX1134, ADS8684, TPS3890, LM73100 or the installed BAT54S clamps. Therefore it is an amplifier/transient starting bench, not a full protected-board bench.

The two AC benches preserve real feedback loading and introduce one floating series source. With the injected-source equation Vminus=Vfeedback+Vtest, the return ratio is L=-Vfeedback/Vminus in a single-loop interpretation; confirm this against the closed-loop transfer before extracting PM/GM. Report all0dB crossings. Coupled row/VCM/TIA loops require multiloop checks. Nominal PM>=60deg; cornersPM>=45deg andGM>=10dB. These values are acceptance criteria, never results here.

Fault/rail/thermal models are unavailable: use FAULT_CASES.json as a33-case bounded list, not a claim that the listed cases ran. Model ESD clamps do not prove real continuous-fault ratings or PCB thermal safety.
