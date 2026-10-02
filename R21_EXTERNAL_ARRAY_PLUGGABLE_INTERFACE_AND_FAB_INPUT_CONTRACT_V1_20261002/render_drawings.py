from pathlib import Path
import pypdfium2 as pdfium,json
P=Path(__file__).parent; D=P/'sources';rs=[]
for fn,indices in [('171856_DRAWING_B2_MIRROR.pdf',[0,1]),('2695_DRAWING_A3_BUNDLE_MIRROR.pdf',[4,5])]:
 doc=pdfium.PdfDocument(D/fn)
 for i in indices:
  pg=doc[i];out=D/(fn[:-4]+f'_PAGE{i+1}.png');pg.render(scale=2).to_pil().save(out);rs.append({'pdf':fn,'page':i+1,'PNG':out.name,'text':pg.get_textpage().get_text_range()})
(P/'DRAWING_TEXT_LOCAL_ONLY.json').write_text(json.dumps(rs,ensure_ascii=False,indent=2),'utf8'); print(json.dumps([{'PNG':r['PNG'],'page':r['page']} for r in rs]))
