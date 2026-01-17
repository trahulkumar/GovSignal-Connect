import unittest
from govsignal.scout import ProcurementScout
from .mocks import MockScout
import logging

# Disable logging for tests
logging.disable(logging.CRITICAL)

class TestScoring(unittest.TestCase):
    def setUp(self):
        pass

    def test_scoring_algorithm(self):
        scout = MockScout()
        keywords = ["chip", "wafer"]
        
        # Test 1: No match
        score = scout._calculate_probability("banana apple", keywords)
        self.assertEqual(score, 0.1)
        
        # Test 2: One match
        score = scout._calculate_probability("This is a silicon wafer facility.", keywords)
        # 0.4 + 0.2 = 0.6
        self.assertAlmostEqual(score, 0.6)
        
        # Test 3: Two matches
        score = scout._calculate_probability("Chip and wafer processing.", keywords)
        # 0.4 + 0.4 = 0.8
        self.assertAlmostEqual(score, 0.8)
        
        # Test 4: Cap
        score = scout._calculate_probability("chip wafer chip wafer chip wafer", keywords)
        self.assertEqual(score, 0.95)

if __name__ == '__main__':
    unittest.main()
