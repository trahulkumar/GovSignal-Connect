import unittest
import yaml
import os
from govsignal.scout import ProcurementScout
import tempfile
import logging

logging.disable(logging.CRITICAL)

class TestConfig(unittest.TestCase):
    def test_load_valid_config(self):
        # Create temp config file
        config_data = {
            "surveillance_targets": {"Test": {}},
            "enabled_local_sources": ["CA_GO_BIZ"]
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as tmp:
            yaml.dump(config_data, tmp)
            tmp_path = tmp.name
        
        try:
            scout = ProcurementScout(tmp_path)
            self.assertIn("Test", scout.targets)
            self.assertEqual(len(scout.active_local_connectors), 1)
        finally:
            os.remove(tmp_path)

    def test_load_invalid_config(self):
        with self.assertRaises(Exception):
            ProcurementScout("non_existent_file.yaml")

    def test_unknown_source(self):
        config_data = {
            "surveillance_targets": {},
            "enabled_local_sources": ["INVALID_SOURCE_KEY"]
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as tmp:
            yaml.dump(config_data, tmp)
            tmp_path = tmp.name
            
        try:
            scout = ProcurementScout(tmp_path)
            # Should not crash, but have 0 active connectors
            self.assertEqual(len(scout.active_local_connectors), 0)
        finally:
            os.remove(tmp_path)

if __name__ == '__main__':
    unittest.main()
