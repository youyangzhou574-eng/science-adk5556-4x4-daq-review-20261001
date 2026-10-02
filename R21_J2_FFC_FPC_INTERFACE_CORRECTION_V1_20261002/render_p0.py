from pathlib import Path
import pypdfium2 as pdfium,json
P=Path(__file__).parent;D=P/'sources_local_only';out=[]
for fn,indices in [('S2_connector_drawing.pdf',[2,3,4]),('S4_cable_drawing.pdf',[0])]:
 doc=pdfium.PdfDocument(D/fn)
 for i in indices:
  pg=doc[i];dest=D/(fn[:-4]+f'_PAGE{i+1}.png');pg.render(scale=2.5).to_pil().save(dest);out.append({'pdf':fn,'page':i+1,'image':dest.name,'text':pg.get_textpage().get_text_range()})
(D/'DRAWING_TEXT_LOCAL_ONLY.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),'utf8');print(json.dumps([{'image':r['image']} for r in out]))
