from science import ROOT
def emit(name,lines):(ROOT/'cases'/(name+'.cir')).write_text('\n'.join(lines)+'\n',encoding='ascii')
