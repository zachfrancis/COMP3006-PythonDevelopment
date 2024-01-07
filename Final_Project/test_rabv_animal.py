#!/usr/bin/env python3
import unittest
from rabv_animal import AnimalRABVData


class TestAnimalRABVData(unittest.TestCase):
    def test_init(self):
        rdata = AnimalRABVData()
        self.assertEqual(repr(rdata), 'Animal rabies cases, China: 2003 - 2018')


    def test_iterable(self):
        iter(AnimalRABVData())


    def test_cases_per_year(self):
        rdata = AnimalRABVData()
        self.assertEqual(str(rdata.cases_per_year()),'Counter({2008: 20, 2014: 19, 2013: 15, 2011: 14, 2006: 10, 2005: 9, 2010: 9, 2018: 9, 2007: 8, 2009: 8, 2016: 8, 2015: 8, 2004: 8, 2017: 7, 2012: 6, 2003: 1})')

        self.assertTrue(len(rdata.cases_per_year()), 5)

        self.assertTrue(len(rdata.cases_per_year()), 16)

        self.assertNotEqual(len(rdata.cases_per_year()), 20)


    def test_animal_counts(self):
        rdata = AnimalRABVData()
        year_list = ["somewhere", "penguin", 2020, "clade"]
        self.assertNotEqual(str(rdata.animal_counts()), year_list)

        self.assertEqual(rdata.animal_counts(), {'Dog': 93, 'Cattle': 16, 'Pig': 2, 'Sheep': 6, 'Camel': 6, 'Fox': 3, 'Raccoon dog': 3, 'Deer': 1, 'Ferret badger': 22})

        self.assertTrue(len(rdata.animal_counts()), 16)


    def test_data_structures(self):
        rdata = AnimalRABVData()
        self.assertEqual(rdata.data_structures()[0][0], [x for x in range(2003, 2019)])

        self.assertEqual(rdata.data_structures()[0][1], [1, 8, 9, 10, 8, 20, 8, 9, 14, 6, 15, 19, 8, 8, 7, 9])

        self.assertEqual(rdata.data_structures()[1][0], ['Asian/SEA1','Asian/SEA2','Cosmopolitan/ST','Arctic-related/AL2','Cosmopolitan/Other','Cosmopolitan/other','Arctic-related','Asian/SEA5','Indian Subcontinent','Asian/SEA3'])

        self.assertEqual(rdata.data_structures()[1][1], [89, 23, 29, 7, 1, 2, 1, 3, 1, 3])


if __name__ == '__main__':
    unittest.main()