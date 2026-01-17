import unittest
from govsignal.scout import ProcurementScout
from .mocks import MockScout
import logging

logging.disable(logging.CRITICAL)

class TestSchema(unittest.TestCase):
    def test_signal_structure(self):
        scout = MockScout()
        mock_data = {"title": "Test Opp", "url": "http://test.com", "source_name": "Test Source"}
        signal = scout._generate_signal(mock_data, "Semiconductors", 0.85)
        
        self.assertIn("signal_id", signal)
        self.assertIn("timestamp", signal)
        self.assertEqual(signal["source"], "Test Source")
        self.assertEqual(signal["demand_probability"], 0.85)
        self.assertEqual(signal["erp_action_recommendation"], "release_capital_hold")

    def test_action_thresholds(self):
        scout = MockScout()
        mock_data = {"source_name": "Test"}
        
        # Monitor case
        sig1 = scout._generate_signal(mock_data, "Test", 0.3)
        self.assertEqual(sig1["erp_action_recommendation"], "monitor")
        
        # Review case
        sig2 = scout._generate_signal(mock_data, "Test", 0.6)
        self.assertEqual(sig2["erp_action_recommendation"], "flag_for_review")
        
        # Action case
        sig3 = scout._generate_signal(mock_data, "Test", 0.8)
        self.assertEqual(sig3["erp_action_recommendation"], "release_capital_hold")

if __name__ == '__main__':
    unittest.main()
