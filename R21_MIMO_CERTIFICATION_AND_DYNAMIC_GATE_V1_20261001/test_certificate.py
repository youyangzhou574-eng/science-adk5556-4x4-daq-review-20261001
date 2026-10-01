import unittest,numpy as np
try:
 from certificate_contract import internal_certificate,reference_contract,block_reference
except ImportError:
 internal_certificate=reference_contract=block_reference=None

class Certificates(unittest.TestCase):
 def test_report_fixture_scope_and_float_evidence(self):
  from pathlib import Path
  import json
  root=Path(__file__).resolve().parent;text=(root/'COMPLETE_CERTIFICATION_RECEIPT.md').read_text(encoding='utf-8')
  section=text.split('### 1.')[1].split('### 2.')[0]
  self.assertNotIn('QZ/LU',section);self.assertIn('LU/logdet',section)
  value=json.loads((root/'HIDDEN_INTERNAL_MODE_COUNTEREXAMPLE.json').read_text(encoding='utf-8'))['maxObservedDifference']
  self.assertGreater(value,0);self.assertIn('1.57e−16',text);self.assertNotIn('839冻结频点的两个端口响应差0',text)
 def test_infinite_generalized_values_are_retained_and_not_finite_pass(self):
  import certificate_contract as mod
  self.assertTrue(callable(getattr(mod,'spectrum_comparison',None)),'spectrum_comparison missing')
  r=mod.spectrum_comparison(np.array([1+0j,np.inf+0j]),np.array([1+0j,np.inf+0j]))
  self.assertEqual(r['infiniteCountA'],1);self.assertFalse(r['fullFiniteQualified']);self.assertEqual(r['finiteMatchedDifference'],0.)
 def test_nearest_frequency_is_not_exact_required_point(self):
  import certificate_contract as mod
  self.assertTrue(callable(getattr(mod,'frequency_coverage',None)),'frequency_coverage missing')
  r=mod.frequency_coverage(np.array([.01,.10004664,1.000933,10.013998]))
  self.assertFalse(r['allRequiredExact']);self.assertTrue(r['points'][0]['exact'])
 def test_hidden_unstable_mode_is_not_port_certificate(self):
  self.assertTrue(callable(internal_certificate),'internal_certificate missing')
  a=np.diag([-1.,1.]);b=np.array([[1.],[0.]]);c=np.array([[1.,0.]])
  r=internal_certificate(a,b,c)
  self.assertFalse(r['internallyStable']);self.assertEqual(r['hiddenRHPCount'],1);self.assertFalse(r['portResponseCertifiesInternalStability'])
 def test_reference_zero_not_same_as_no_RHP_poles(self):
  self.assertTrue(callable(reference_contract),'reference_contract missing')
  r=reference_contract(referencePoles=[],referenceZeros=[1.],internalCertificate=False)
  self.assertFalse(r['defaultZeroWindingSufficient']);self.assertEqual(r['referenceRHPZeros'],1)
 def test_partition_source_and_all_rows(self):
  self.assertTrue(callable(block_reference),'block_reference missing')
  g=np.arange(100).reshape(10,10).astype(complex);z=block_reference(g)
  for ids in ([2,3,4,5],[6,7,8,9],[0,1]):np.testing.assert_equal(z[np.ix_(ids,ids)],g[np.ix_(ids,ids)])
  self.assertEqual(np.count_nonzero(z),35) # 36 retained entries, g[0,0] itself is zero
 def test_incomplete_internal_reference_cannot_pass(self):
  self.assertTrue(callable(reference_contract),'reference_contract missing')
  r=reference_contract(referencePoles=[-1.],referenceZeros=[-2.],internalCertificate=False)
  self.assertFalse(r['defaultZeroWindingSufficient'])

if __name__=='__main__':unittest.main()
