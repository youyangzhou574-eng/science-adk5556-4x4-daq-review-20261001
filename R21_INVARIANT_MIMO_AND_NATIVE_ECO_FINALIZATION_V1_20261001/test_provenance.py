import unittest,json
from pathlib import Path
class ProvenanceTests(unittest.TestCase):
 def test_tia_loaded_scope_not_direct_series_shunt_pass(self):
  rows=json.loads((Path(__file__).parent/'FULL_NETWORK_SCHUR_TIAN_CROSSCHECK.json').read_text());t=next(x for x in rows if x['target']==6)
  self.assertEqual(t['measurementMethod'],'LOADED_TWO_PORT_VOLTAGE_COLUMNS')
  self.assertFalse(t['directSeriesShuntQualified']);self.assertTrue(t['PASS']);self.assertEqual(t['PASSscope'],'LOADED_2PORT_VS_SCHUR_ONLY')
  self.assertEqual(t['sourceCases'],['tian_TIA0_loaded_p0','tian_TIA0_loaded_p1'])
  self.assertEqual(t['status'],'LOADED_2PORT_SCHUR_CROSSCHECK_PASS_DIRECT_TIAN_HOLD')
if __name__=='__main__':unittest.main()
