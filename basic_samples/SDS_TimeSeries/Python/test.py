"""This script tests the SDS Time Series Python sample script"""

import unittest
from .program import main


class SDSTimeSeriesPythonSampleTests(unittest.TestCase):
    """Tests for the SDS Time Series Python sample"""

    @classmethod
    def test_main(cls):
        """Tests the SDS Time Series Python main sample script"""
        main(True)


if __name__ == "__main__":
    unittest.main()
