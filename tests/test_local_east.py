import unittest
from govsignal.local_connectors import (
    NewYorkEmpireStateConnector, MassLifeSciencesConnector, VirginiaEconomicDevConnector,
    PennCommunityDevConnector, PortAuthorityNYNJConnector
)

class TestLocalEast(unittest.TestCase):
    def test_ny_esd(self):
        self.assertEqual(NewYorkEmpireStateConnector().get_opportunities([])[0]["source"], "NY ESD")

    def test_mass_life(self):
        self.assertEqual(MassLifeSciencesConnector().get_opportunities([])[0]["source"], "Mass Life Sciences")
    
    def test_va_edp(self):
        self.assertEqual(VirginiaEconomicDevConnector().get_opportunities([])[0]["source"], "VEDP")

    def test_pa_dced(self):
        self.assertEqual(PennCommunityDevConnector().get_opportunities([])[0]["source"], "PA DCED")
        
    def test_panynj(self):
        self.assertEqual(PortAuthorityNYNJConnector().get_opportunities([])[0]["source"], "PA NYNJ")

if __name__ == '__main__':
    unittest.main()
