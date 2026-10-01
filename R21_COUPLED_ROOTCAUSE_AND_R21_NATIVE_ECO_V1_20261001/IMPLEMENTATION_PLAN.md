# R2.1 coupled closure — bounded execution plan

Authority: PRO_COUPLED_RULING_FULL.md and the user's explicit second-stage resume.
Frozen inputs: R2 da6ca87, R2.1 verification c13555a, ngspice47 PSA, original TI models.
P0 45min: verify bench bias against physical R2 topology, RED/GREEN regression, loading-preserving Tian two-port vs series-voltage injection on known fixture and each real amplifier class. No compensation sweep.
P1 85min: full static corner DC/AC/PZ, short partitioned transient at 300us valid edges. Every normal case max180s; full long max1 at480s. Preserve numeric failures; stop on physical gate failure.
P2 35min: direct reset guaranteed bounds, signed fault-current limitations; progress watchdog tests <=32 total.
P3 60min conditional: minimum native ECO ONLY if all five entry gates PASS. Otherwise zero EDA actions.
P4 15min: full report and readable raw evidence to a new fixed public GitHub directory once, concise paired-chat handoff once, immediate history check plus successor monitor before ending.
No PCB/bench/manufacture/procurement/local Git/system changes.
Communication fix: send accepted != history confirmed != assistant replied != decision consumed. Each new submission records nextCheckAtUTC, watcher ID, last error and phase; no blind resending.

Bench bug hypothesis (before fixes): previous coupled generator's RUP90k/RDN10k produces 0.25V, not frozen2.25V. Physical R2 PLAN has RD_TOP10k and nine10k bottom resistors. Old log VCM2.48829/VEXC0.245138 corroborates the error. Old full transient failures remain preserved and cannot characterize intended operating bias.
