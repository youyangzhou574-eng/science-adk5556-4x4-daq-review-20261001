# One bounded PZ qualification chain

Passive RC transimpedance fixture returned a real Pole-Zero Analysis plot with pole=-500rad/s, matching the independently derived time constant2kΩ×1µF. Fixture qualification PASS.

The single real OPA4388 closed-TIA level was attempted first with coincident current/output ports, then one corrected distinct ADC/tap port. Both obtained actual OP but ngspice aborted PZ with “The input signal is shorted on the way to the output”. pz.raw remained Operating Point, not pole data. Initial wrong coincident-port attempt is preserved, not omitted.

Classification: PZ_TOOL_OR_MODEL_CAPABILITY_LIMIT for this qualified executor/model/port chain; it does not prove every alternative PZ port or every model intrinsically unsupported. Stop this chain here: no4macro/full-network PZ attempts. Per binding ruling, PZ is not a native-entry hard gate. No poles inferred from OP raw or analysis exit0.
