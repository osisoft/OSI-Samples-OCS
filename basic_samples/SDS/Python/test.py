"""This script tests the SDS Python sample script"""

import unittest
from .program import main


class SDSPythonSample(unittest.TestCase):
    """Tests for the SDS Python sample"""

    @classmethod
    def test_main(cls):
        """Tests the SDS Python main sample script"""
        main(True)


if __name__ == "__main__":
    unittest.main()
