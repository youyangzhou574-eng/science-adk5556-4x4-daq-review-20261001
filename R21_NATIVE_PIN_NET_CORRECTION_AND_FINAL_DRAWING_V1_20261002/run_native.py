import sys,json,pathlib,subprocess
from budget import charge
P=pathlib.Path(__file__).resolve().parent
kind,label=sys.argv[1:3]
args=sys.argv[3:]
if kind!='read': charge(kind,label)
subprocess.run([sys.executable,'-X','utf8','-B',str(P/'cli_call.py'),label,*args],check=True,timeout=60)
