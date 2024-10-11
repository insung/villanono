import unittest

from util import read_divisions


class TestDivisions(unittest.TestCase):
    def test_read_division(self):
        sigudong = read_divisions()

        self.assertTrue("서울특별시" in sigudong)
        self.assertTrue("영등포구" in sigudong["서울특별시"])
        self.assertTrue("면목동" in sigudong["서울특별시"]["중랑구"])
