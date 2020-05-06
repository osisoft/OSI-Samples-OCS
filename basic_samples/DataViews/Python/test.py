"""This script tests the Data Views Python sample script"""

import unittest
from .program import main


class DataViewsPythonSampleTests(unittest.TestCase):
    """Tests for the Data Views Python sample"""

    @classmethod
    def test_main(cls):
        """Tests the Data Views Python main sample script"""
        main(True)


if __name__ == '__main__':
    unittest.main()
