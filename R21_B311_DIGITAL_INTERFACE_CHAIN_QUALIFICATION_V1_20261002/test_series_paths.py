import unittest
from digital_chain import series_paths
class InterfacePaths(unittest.TestCase):
 def setUp(self):
  self.pads=[{'ref':r,'pad':p,'net':n,'xy':xy} for r,p,n,xy in [('U7','24','SWDIO',(0,0)),('R_J3_3','2','SWDIO',(8,0)),('R_J3_3','1','SWDIO_EXT',(9,0)),('J3','3','SWDIO_EXT',(10,0))]]
 def test_crosses_renamed_net_through_both_series_pads(self):
  paths=series_paths(self.pads,['U7'],['J3'],['R_J3_3'])
  self.assertEqual(len(paths),1);self.assertEqual(paths[0]['orderedNodes'],['U7.24','R_J3_3.2','R_J3_3.1','J3.3'])
  self.assertEqual(paths[0]['wireLengthMm'],9);self.assertEqual(paths[0]['functionalLengthWithResistorSpanMm'],10)
 def test_missing_ext_pin_must_not_invent_path(self):
  self.pads.pop(2);self.assertEqual(series_paths(self.pads,['U7'],['J3'],['R_J3_3']),[])
 def test_open_nc_must_not_join_empty_net(self):
  for p in self.pads:p['net']=''
  self.assertEqual(series_paths(self.pads,['U7'],['J3'],['R_J3_3']),[])
if __name__=='__main__':unittest.main()
