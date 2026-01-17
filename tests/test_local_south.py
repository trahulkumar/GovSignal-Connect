import unittest
from govsignal.local_connectors import (
    TexasEnterpriseFundConnector, FloridaDefenseConnector, GeorgiaEconomicDevConnector,
    NorthCarolinaBiotechConnector, CityOfHuntsvilleConnector
)

class TestLocalSouth(unittest.TestCase):
    def test_tx_tef(self):
        self.assertEqual(TexasEnterpriseFundConnector().get_opportunities([])[0]["source"], "Texas TEF")

    def test_fl_defense(self):
        self.assertEqual(FloridaDefenseConnector().get_opportunities([])[0]["source"], "Florida Defense TF")

    def test_ga_eco(self):
        self.assertEqual(GeorgiaEconomicDevConnector().get_opportunities([])[0]["source"], "Georgia Eco Dev")
        
    def test_nc_biotech(self):
        self.assertEqual(NorthCarolinaBiotechConnector().get_opportunities([])[0]["source"], "NC Biotech")

    def test_huntsville(self):
        self.assertEqual(CityOfHuntsvilleConnector().get_opportunities([])[0]["source"], "City of Huntsville")

if __name__ == '__main__':
    unittest.main()

# Refined by GovSignal Automation
