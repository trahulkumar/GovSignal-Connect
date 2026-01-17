import unittest
from govsignal.connectors import SamGovConnector

class TestSamConnector(unittest.TestCase):
    def test_get_opportunities(self):
        connector = SamGovConnector()
        results = connector.get_opportunities(["defense"])
        
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        
        item = results[0]
        self.assertIn("noticeId", item)
        self.assertIn("solicitationNumber", item)
        self.assertIn("description", item)

if __name__ == '__main__':
    unittest.main()

# Refined by GovSignal Automation
