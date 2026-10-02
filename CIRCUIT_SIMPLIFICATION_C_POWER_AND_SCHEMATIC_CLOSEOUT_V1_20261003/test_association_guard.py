import unittest
from association_guard import validate_creation_id
class AssociationTests(unittest.TestCase):
 def test_imported_id_must_not_be_created(self):
  with self.assertRaises(ValueError):validate_creation_id({'ref':'J1','association':{'uuid':'bac146b35b35db45'}})
 def test_catalog_id_is_allowed(self):
  self.assertTrue(validate_creation_id({'ref':'J1','association':{'uuid':'eab4a8150b6d4918927e38d645cd50f2'}}))
 def test_inherited_j2_does_not_recreate(self):
  self.assertTrue(validate_creation_id({'ref':'J2','association':{'uuid':'1234567890abcdef'}}))
 def test_nonhex_catalog_id_rejected(self):
  with self.assertRaises(ValueError):validate_creation_id({'ref':'U8','association':{'uuid':'g'*32}})
if __name__=='__main__':unittest.main()
