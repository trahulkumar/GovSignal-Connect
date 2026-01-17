import unittest
from govsignal.local_connectors import (
    CaliforniaGoBizConnector, ArizonaCommerceConnector, WashingtonCommerceConnector
)

class TestLocalWest(unittest.TestCase):
    def test_ca_gobiz(self):
        connector = CaliforniaGoBizConnector()
        res = connector.get_opportunities([])
        self.assertEqual(res[0]["source"], "CA GO-Biz")
        self.assertIn("Semiconductor", res[0]["title"])

    def test_az_commerce(self):
        connector = ArizonaCommerceConnector()
        res = connector.get_opportunities([])
        self.assertEqual(res[0]["source"], "AZ Commerce")
    
    def test_wa_commerce(self):
        connector = WashingtonCommerceConnector()
        res = connector.get_opportunities([])
        self.assertEqual(res[0]["source"], "WA Commerce")
        self.assertIn("Aerospace", res[0]["title"])

if __name__ == '__main__':
    unittest.main()

# Refined by GovSignal Automation
