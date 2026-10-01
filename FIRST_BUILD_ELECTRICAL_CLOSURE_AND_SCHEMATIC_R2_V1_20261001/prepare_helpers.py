import pathlib
p=pathlib.Path(__file__).resolve().parent;v=p.parent/'FIRST_BUILD_DETAILED_DESIGN_AND_NATIVE_SCHEMATIC_V1'
s=(v/'parse_all_library.py').read_text(encoding='utf-8')
for a,b in [('ALL_LIBRARY_FILE.json','NEW_LIBRARY_FILE.json'),('ALL_LIBRARY.elibz2','NEW_LIBRARY.elibz2'),("p/'all_library'","p/'new_library'"),('ALL_SELECTED_DEVICES.json','NEW_SELECTED_DEVICES.json'),('ALL_LIBRARY_PARSED.json','NEW_LIBRARY_PARSED.json')]:s=s.replace(a,b)
s=s.replace('NEW_LIBRARY_FILE.json','NEW_LIBRARY_FILE_REV2.json')
s=s.replace("source=next(out.glob('*.elibu')).read_text(encoding='utf-8')","source=z.read(next(n for n in z.namelist() if n.endswith('.elibu'))).decode('utf-8')")
(p/'parse_new_library.py').write_text(s,encoding='utf-8')
