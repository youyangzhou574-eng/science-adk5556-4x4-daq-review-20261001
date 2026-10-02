from pathlib import Path
p=Path(__file__).parent
f=p/'COMPLETE_ROUTING_RECEIPT.md';s=f.read_text('utf8')
s=s.replace('最终原生source相对warm净增17个LINE图元（原生连接处自动分段）','最终原生source相对warm净增17个LINE图元；15桥均可对应created IDs，另外两条L1/6mil/0.1mil的VCM与TIA1短线来源未独立确认，不推断自动分段')
s=s.replace('原生 filled path 的 ARC 以≤8°采样用于显示/几何检查','原生filled path的ARC按目标约8°采样用于显示/几何检查，实际最大9.997384°')
f.write_text(s,'utf8')
f=p/'REVIEW_DRAWING_ADDENDUM.md';s=f.read_text('utf8').replace('原生源净增17LINE，','原生源净增17LINE；另两条L1/6mil/0.1mil的VCM/TIA1短线来源未独立确认（137f992f55430857、21f945bfa3a6372f），');f.write_text(s,'utf8')
f=p/'README.md';s=f.read_text('utf8')+'\nFINAL PNG必须同时阅读[图面说明纠正](REVIEW_DRAWING_ADDENDUM.md)：ARC标题≤8°应为实际最大约10°。最终多出两条0.1mil短线来源未独立确认；核验门保持HOLD。\n';f.write_text(s,'utf8')
print('Documentation-only two minor corrections; no re-export or native mutation')
