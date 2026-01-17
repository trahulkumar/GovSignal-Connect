import unittest
import os
import sys

def run_tests():
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern="test_*.py")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result

if __name__ == "__main__":
    result = run_tests()
    sys.exit(0 if result.wasSuccessful() else 1)

# Refined by GovSignal Automation
