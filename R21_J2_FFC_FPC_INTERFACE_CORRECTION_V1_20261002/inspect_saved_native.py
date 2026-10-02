from pathlib import Path
import sqlite3,json
P=Path(__file__).parent;p=P/'SCIENCE_ADK5556_4X4_R21_J2_FFC_WORK.eprj2'
c=sqlite3.connect(p.as_uri()+'?mode=ro',uri=True)
for t in ['components','users','sessions']:
 print(t,c.execute('pragma table_info('+t+')').fetchall())
print('nonblankpasswordcount',c.execute("select count(*) from users where password is not null and password <> ''").fetchone()[0])
print('componentkeys',c.execute('select uuid,title,docType,length(source) from components').fetchall())
