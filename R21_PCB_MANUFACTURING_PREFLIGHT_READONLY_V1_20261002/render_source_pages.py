import pathlib,pypdfium2,json
p=pathlib.Path(__file__).parent
for name,page in [("LM73100",50),("TPS3890",25),("ADS8684",66),("BAT54S",5)]:
 pdf=pypdfium2.PdfDocument(p/"sources"/(name+".pdf"))
 pg=pdf[page-1];im=pg.render(scale=1.5).to_pil();im.save(p/"sources"/(name+"_PACKAGE_PAGE"+str(page)+".png"));print(name,page)

