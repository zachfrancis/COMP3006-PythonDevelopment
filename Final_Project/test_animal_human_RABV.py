#!/usr/bin/env python3
import unittest
from animal_human_RABV import MergeRABVData


class TestAnimalRABVData(unittest.TestCase):
    def test_init(self):
        mdata = MergeRABVData()
        self.assertEqual(len(mdata.adata), 159)


    def test_dict_structure(self):
        mdata = MergeRABVData()
        self.assertEqual(mdata.dict_structure('cow'), {2003: 0, 2004:0, 2005: 0, 2006: 0, 2007: 0, 2008: 0, 2009: 0, 2010: 0, 2011: 0})

        self.assertEqual(mdata.dict_structure('Ferret badger'), {2003: 0, 2004: 0, 2005: 0, 2006: 0, 2007: 0, 2008: 5, 2009: 1, 2010: 2, 2011: 2})


    def test_location(self):
        mdata = MergeRABVData()
        self.assertEqual(mdata.location(), {'China': 167, 'Russia': 35, 'Cambodia': 11, 'Indonesia': 11, 'Mongolia': 9, 'Kazakhstan': 7, 'Afghanistan': 6, 'India': 6, 'South Korea': 6, '': 5, 'Laos': 4, 'Nepal': 4, 'Philippines': 4, 'Thailand': 4, 'Myanmar': 3, 'USA': 3, '\ufeffCountry': 1, 'Bhutan': 1, 'Brazil': 1, 'Iran': 1, 'Iraq': 1, 'Israel': 1, 'Japan': 1, 'Madagascar': 1, 'Mexico': 1, 'Morocco': 1, 'Pakistan': 1, 'Sri Lanka': 1, 'Tajikistan': 1, 'Tanzania': 1, 'Turkey': 1, 'Vietnam': 1, 'China (CN)': 1})
        

if __name__ == '__main__':
    unittest.main()