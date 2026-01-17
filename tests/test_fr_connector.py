import unittest
from govsignal.connectors import FederalRegisterConnector

class TestFRConnector(unittest.TestCase):
    def test_get_documents(self):
        connector = FederalRegisterConnector()
        results = connector.get_documents(["chips"])
        
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        
        item = results[0]
        self.assertIn("document_number", item)
        self.assertIn("abstract", item)
        self.assertEqual(item["type"], "Notice of Funding Opportunity")

if __name__ == '__main__':
    unittest.main()

# Refined by GovSignal Automation
