from pathlib import Path
P=Path(__file__).parent
for n in('capture_routing.js','drc_routing.js'):
 t=(P/n).read_text('utf8').replace('315433ef1f45b1184319722b4f2939c77ef021639b42a2c9559dabe747dba45a','6c25a449ce9ab470f4c1db4bd85120e6cad325b0f291f573b07c6aaa4d353ee1')
 (P/n).write_text(t,'utf8')
print('Guards set to actual GUI-observed isolated project UUID; PCBUUID retained from frozen source pending GUI activation')
