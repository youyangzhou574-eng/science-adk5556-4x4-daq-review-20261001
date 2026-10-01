"""Ideal-amplifier analytic screening, not a manufacturer macro model."""
import numpy as np
from scipy.signal import residue

def adc_residual(*, rs, rb, ch, conductance, line_cap, sample_time):
    if min(rs, rb, ch, conductance, sample_time) <= 0 or line_cap < 0:
        raise ValueError('positive circuit parameters required')
    tz = ch*(rb+rs)
    tp = ch*(rb+rs+rb*rs*conductance)
    q = ch*rb*rs*line_cap
    row = np.array([q,tp,1.]) if q else np.array([tp,1.])
    den = np.polymul(np.polymul(row,[4990*2.2e-9,1]),[100*10e-9,1])
    scale = 1e-6
    num = np.array([tz/scale,1.])
    den = den/(scale**np.arange(len(den)-1,-1,-1))
    residues,poles,direct = residue(num,np.polymul(den,[1,0]),tol=1e-9)
    remaining = sum(r*np.exp(p*sample_time/scale) for r,p in zip(residues,poles) if abs(p)>1e-12)
    return float(abs(remaining)*.25*4990*conductance/4)

def protected_cf_current_bound(*, delta_v, isolation):
    if isolation <= 0 or not np.isfinite(isolation):
        raise ValueError('the complete Cf output path needs finite positive isolation')
    return abs(delta_v)/isolation
