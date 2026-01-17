import unittest
import os
import yaml
import tempfile
from govsignal.scout import ProcurementScout
import logging

logging.disable(logging.CRITICAL)

class TestIntegration(unittest.TestCase):
    def test_full_cycle(self):
        # Setup a comprehensive config
        config_data = {
            "surveillance_targets": {
                "Semiconductors": {
                    "related_asset": "Asset1",
                    "keywords": ["chip", "tax credit", "grant"]
                }
            },
            "enabled_local_sources": ["CA_GO_BIZ", "TX_TEF"]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as tmp:
            yaml.dump(config_data, tmp)
            tmp_path = tmp.name
            
        try:
            scout = ProcurementScout(tmp_path)
            # Run the actual logic (mock connectors will return data)
            signals = scout.run()
            
            self.assertIsInstance(signals, list)
            # We expect results because the mock connectors return relevant data 
            # (e.g. CA GO-Biz returns a semi tax credit match)
            # However, keywords matching logic must actually hit.
            # CA GO-Biz mock: "Tax credits available for semiconductor manufacturing..."
            # Keywords: "chip", "tax credit", "grant" -> "tax credit" match!
            
            # Note: _calculate_probability logic converts text to lower.
            # "Tax credits" -> "tax credit" substring match?
            # "Tax credits" contains "tax credit"? Yes.
            
            match_found = False
            for s in signals:
                if s["source"] == "CA GO-Biz":
                    match_found = True
                    break
            
            self.assertTrue(match_found, "Expected signal from CA GO-Biz")
            
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

if __name__ == '__main__':
    unittest.main()
