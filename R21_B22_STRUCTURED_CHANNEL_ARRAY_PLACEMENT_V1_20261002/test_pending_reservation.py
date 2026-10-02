import structured_placement as s
import json
# A small real-geometry regression; no candidate stage or placement budget is started.
# A future noncritical resistor must not occupy an unprocessed critical decoupling site.
r='R_CS_PU'; q='C_ADCD'; pose=tuple(s.old[q])
result=s.valid({r:pose})
expected=result is None
print(json.dumps({'test':'unprocessed_critical_site_reserved','pass':expected,'candidateRef':r,'futureCriticalRef':q}))
assert expected, 'Sequential template placement lost future critical-pad feasibility'
