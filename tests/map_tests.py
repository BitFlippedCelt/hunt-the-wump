__author__ = 'petastream'

import unittest
from game.map import Map


class TestMap(unittest.TestCase):
    def setUp(self):
        self.map = Map()

    def test_generate(self):
        self.map.generate()


if __name__ == "__main__":
    unittest.main()