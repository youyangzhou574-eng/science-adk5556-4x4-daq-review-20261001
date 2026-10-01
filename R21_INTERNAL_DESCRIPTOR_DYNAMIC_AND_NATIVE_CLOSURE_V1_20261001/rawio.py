from pathlib import Path
import re
def op_values(path):
 text=Path(path).read_text(encoding='utf-8');assert 'Plotname: Operating Point'in text and 'Flags: real'in text
 defs=[line.split()[1:]for line in text.split('Variables:\n')[1].split('Values:\n')[0].splitlines()if line.strip()];rows=text.split('Values:\n')[1].splitlines();values=[float(rows[0].split()[1])]+[float(x)for x in rows[1:]if x.strip()];assert len(defs)==len(values)
 return {(name[2:-1]if name.startswith('v(')else 'branch:'+name[2:-1]if name.startswith('i(')else name):value for (name,kind),value in zip(defs,values)}
