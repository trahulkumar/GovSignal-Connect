import unittest
from govsignal.local_connectors import (
    CityOfAustinConnector, CityOfBostonConnector
)

class TestLocalCities(unittest.TestCase):
    def test_austin(self):
        res = CityOfAustinConnector().get_opportunities([])
        self.assertEqual(res[0]["source"], "City of Austin")
        self.assertIn("Smart City", res[0]["title"])

    def test_boston(self):
        res = CityOfBostonConnector().get_opportunities([])
        self.assertEqual(res[0]["source"], "City of Boston")
        self.assertIn("Life Sciences", res[0]["title"])

if __name__ == '__main__':
    unittest.main()
