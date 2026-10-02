from pathlib import Path
import sqlite3,json
P=Path(__file__).parent;c=sqlite3.connect((P/'SCIENCE_ADK5556_4X4_R21_J2_FFC_WORK.eprj2').as_uri()+'?mode=ro',uri=True)
for n,s in c.execute("select name,sql from sqlite_master where type='table'"):
 if n in ['documents','files','projects','sheets','components']:
  print(n,s)

print('docs',c.execute('select uuid,title,docType,length(dataStr) from documents').fetchall())
print('projectnames',c.execute('select uuid,name,length(content) from projects').fetchall())
