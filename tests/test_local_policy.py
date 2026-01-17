import unittest
from govsignal.local_connectors import (
    NationalGovernorsAssocConnector, CouncilStateGovernmentsConnector
)

class TestLocalPolicy(unittest.TestCase):
    def test_nga_policy(self):
        res = NationalGovernorsAssocConnector().get_opportunities([])
        self.assertEqual(res[0]["source"], "NGA")
        self.assertTrue("Compacts" in res[0]["description"] or "Compact" in res[0]["title"] or "Compact" in res[0]["description"])

    def test_csg_policy(self):
        res = CouncilStateGovernmentsConnector().get_opportunities([])
        self.assertEqual(res[0]["source"], "CSG")

if __name__ == '__main__':
    unittest.main()
