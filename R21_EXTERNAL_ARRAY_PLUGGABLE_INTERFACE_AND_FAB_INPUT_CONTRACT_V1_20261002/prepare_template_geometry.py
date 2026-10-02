from pathlib import Path
P=Path(__file__).parent;s=(P/'footprint_geometry.js').read_text('utf8').replace("before.includes('268e6597399ebcce_1cca92df09a37573')","before.includes('87b2e6ab0bf2243f')")
s=s.replace("if(!['e10','e11','e12','e13','e14','e15'].includes(id))throw Error('Unexpected footprint outline');","if(!['e10','e11','e12','e13','e14','e15'].includes(id))throw Error('Unexpected original J2 template outline');")
(P/'j2_template_geometry.js').write_text(s,'utf8');print('Original8-pad template is only used byJ2; identical qualified geometry; no explicitsave')
