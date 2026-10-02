import unittest
from diode_polarity_guard import valid
class Guard(unittest.TestCase):
 def test_actual_catalog_cathode(self):self.assertTrue(valid('1','C'))
 def test_reject_reversed(self):self.assertFalse(valid('1','A'));self.assertFalse(valid('2','C'))
 def test_explicit_labels(self):self.assertTrue(valid('1','Cathode'));self.assertTrue(valid('2','A'))
if __name__=='__main__':unittest.main()
