import unittest
from govsignal.local_connectors import (
    OhioDevelopmentConnector, MichiganEconomicDevConnector, IndianaEconomicDevConnector
)

class TestLocalMidwest(unittest.TestCase):
    def test_oh_dev(self):
        res = OhioDevelopmentConnector().get_opportunities([])
        self.assertEqual(res[0]["source"], "Ohio Development")
        self.assertIn("Silicon Heartland", res[0]["title"])

    def test_mi_medc(self):
        res = MichiganEconomicDevConnector().get_opportunities([])
        self.assertEqual(res[0]["source"], "Michigan MEDC")
        self.assertIn("Defense", res[0]["title"])

    def test_in_iedc(self):
        res = IndianaEconomicDevConnector().get_opportunities([])
        self.assertEqual(res[0]["source"], "Indiana IEDC")

if __name__ == '__main__':
    unittest.main()

# Refined by GovSignal Automation
