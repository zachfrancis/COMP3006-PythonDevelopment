#!/usr/bin/env python3

import unittest
from xml.etree.ElementTree import tostring

from autompg2 import AutoMPG, AutoMPGData

class TestAutoMPG(unittest.TestCase):
    """Test AutoMPG class functionality"""

    def test_string_representation(self):
        car = AutoMPG('Toyota', 'Corolla', 1971, 31.0)
        self.assertEqual(f"{car}", "AutoMPG('Toyota','Corolla','1971','31.0')")

    def test_equals(self):
        car1 = AutoMPG('Toyota', 'Corolla', 1971, 31.0)
        car2 = AutoMPG('Toyota', 'Corolla', 1971, 31.0)
        self.assertEqual(car1, car2)

        car1 = AutoMPG('Toyota', 'Corolla', 1971, 31.0)
        car2 = AutoMPG('Honda', 'Civic', 1992, 38.0)
        self.assertNotEqual(car1, car2)

        car1 = AutoMPG('Toyota', 'Corolla', 1971, 31.0)
        car2 = AutoMPG('Toyota', 'Corolla', 1971, 32.0)
        self.assertNotEqual(car1, car2)

        car1 = AutoMPG('Toyota', 'Corolla', 1971, 31.0)
        car2 = AutoMPG('Toyota', 'Corolla', 1981, 31.0)
        self.assertNotEqual(car1, car2)

    def test_comparison(self):
        car1 = AutoMPG('Toyota', 'Corolla', 1971, 31.0)
        car2 = AutoMPG('Toyota', 'Corolla', 1971, 31.0)
        self.assertFalse(car1 > car2)

        car1 = AutoMPG('Toyota', 'Corolla', 1971, 31.0)
        car2 = AutoMPG('Honda', 'Civic', 1992, 38.0)
        self.assertTrue(car1 > car2)

        car1 = AutoMPG('Toyota', 'Corolla', 1971, 31.0)
        car2 = AutoMPG('Toyota', 'Corolla', 1971, 32.0)
        self.assertTrue(car1 < car2)

        car1 = AutoMPG('Toyota', 'Corolla', 1981, 31.0)
        car2 = AutoMPG('Toyota', 'Corolla', 1971, 31.0)
        self.assertFalse(car1 < car2)


class TestAutoMPGData(unittest.TestCase):
    """Test AutoMPGData class functionality"""
    
    def test_parse_data(self):
        autoData = ['14.0   8   350.0      165.0      4209.      12.0   71  1     "chevrolet impala"']
        ret = AutoMPGData._parse_data(None, autoData)
        self.assertEqual(ret, [AutoMPG('chevrolet','impala',1971,14.0)])

        autoData = ['24.0   4   90.00      75.00      2108.      15.5   74  2        "fiat 128"',
                    '40.9   4   85.00      ?          1835.      17.3   80  2        "renault lecar deluxe"',
                    '24.0   4   113.0      95.00      2372.      15.0   70  3        "toyota corona mark ii"',
                    '26.0   4   108.0      93.00      2391.      15.5   74  3        "subaru"']
        ret = AutoMPGData._parse_data(None, autoData)
        self.assertEqual(ret, [AutoMPG('fiat', '128', 1974, 24.0),
                               AutoMPG('renault','lecar deluxe', 1980, 40.9),
                               AutoMPG('toyota','corona mark ii', 1970, 24.0),
                               AutoMPG('subaru','', 1974, 26.0)])


if __name__ == '__main__':
    unittest.main()