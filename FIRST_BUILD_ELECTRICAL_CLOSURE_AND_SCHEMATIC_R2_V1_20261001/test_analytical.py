import unittest

class AnalyticalRegression(unittest.TestCase):
    def test_old_row_compensation_reproduces_review_counterexample(self):
        from analytical_validation import adc_residual
        r = adc_residual(rs=1000, rb=10000, ch=1e-9, conductance=4/800, line_cap=0, sample_time=300e-6)
        self.assertAlmostEqual(r, 0.01159, delta=0.00003)
        self.assertGreater(r, 100e-6)

    def test_revised_row_candidate_screens_both_load_endpoints(self):
        from analytical_validation import adc_residual
        for g in (4/800, 4/8000):
            for cl in (0, 1e-9):
                self.assertLess(adc_residual(rs=1000, rb=4990, ch=100e-12, conductance=g, line_cap=cl, sample_time=300e-6), 100e-6)

    def test_zero_capacitive_feedthrough_current_not_used_as_fault_bound(self):
        from analytical_validation import protected_cf_current_bound
        self.assertAlmostEqual(protected_cf_current_bound(delta_v=5.25, isolation=1000), 0.00525)
        with self.assertRaises(ValueError):
            protected_cf_current_bound(delta_v=5.25, isolation=0)

if __name__ == '__main__':
    unittest.main()
