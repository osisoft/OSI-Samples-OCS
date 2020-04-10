import unittest
from .program import main


class AuthPKCEPythonSample(unittest.TestCase):
    def test_main(self):
        main(True)


if __name__ == '__main__':
    unittest.main()
