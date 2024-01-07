#!/usr/bin/env python3

import unittest

from rabies_analysis import RabiesAnalyzer, RabiesInfo

class TestRabiesInfo(unittest.TestCase):
    """Test class for RabiesInfo"""

    def test_string(self):
        """Test string representation"""
        ri = RabiesInfo('Africa', 'Zambia', 'Y', '13255000', '204', '5000', '2010')
        self.assertEqual(f"{ri}", "RabiesInfo(Zambia, 2010, 13255000, 204, 5000, PEP: True)")

    def test_equal(self):
        """Test if objects are equal"""
        r1 = RabiesInfo('Continent', 'Country', 'Y', '12345678', '20', '5000', '2010')
        r2 = RabiesInfo('Continent', 'Country', 'Y', '12345678', '20', '5000', '2010')
        r3 = RabiesInfo('Different', 'Country', 'Y', '12345678', '20', '5000', '2010')
        r4 = RabiesInfo('Continent', 'Different', 'Y', '12345678', '20', '5000', '2010')
        r5 = RabiesInfo('Continent', 'Country', 'Y', '12345', '20', '5000', '2010')
        r6 = RabiesInfo('Continent', 'Country', 'Y', '12345678', '10', '5000', '2010')
        r7 = RabiesInfo('Continent', 'Country', 'Y', '12345678', '20', '4999', '2010')
        r8 = RabiesInfo('Continent', 'Country', 'Y', '12345678', '20', '5000', '2009')
        r9 = RabiesInfo('Continent', 'Country', 'N', '12345678', '20', '5000', '2010')
        r10 = r1

        self.assertEqual(r1, r2)
        self.assertEqual(r1, r10)
        self.assertNotEqual(r1, r3)
        self.assertNotEqual(r1, r4)
        self.assertNotEqual(r1, r5)
        self.assertNotEqual(r1, r6)
        self.assertNotEqual(r1, r7)
        self.assertNotEqual(r1, r8)
        self.assertNotEqual(r1, r9)

    def test_comparisons(self):
        """Test comparisons between objects"""
        r1 = RabiesInfo('Asia', 'China', 'Y', '12345678', '20', '5000', '2010')
        r2 = RabiesInfo('Asia', 'China', 'Y', '12345678', '20', '5000', '2010')
        r3 = RabiesInfo('Africa', 'Zambia', 'Y', '12345678', '20', '5000', '2010')
        r4 = RabiesInfo('Asia', 'India', 'Y', '12345678', '20', '5000', '2010')
        r5 = RabiesInfo('Asia', 'China', 'Y', '1234', '20', '5000', '2010')

        self.assertTrue(r1 > r3) # Asia > Africa 
        self.assertTrue(r1 < r4) # China < India
        self.assertTrue(r1 > r5) # Population comparison
        self.assertFalse(r1 < r2) # Objects are equal


class TestRabiesAnalyzer(unittest.TestCase):
    """Test class for RabiesAnalyzer"""

    def test_parse_data(self):
        test_file = ['Continent,Country,Cluster,Location,Endemic,pcPop,country_population,Deaths/yr,Exposures/yr,Death rate/ yr,Bite rate/ yr,Year,Incidence,PP,Data source,corrected_Country',
        'Europe,Albania,EasternEurope,countrywide,1,100.00%,"3,169,000",0,0,,,2009-2010,N,N,Rabies Bulletin Europe website: http://www.who-rabies-bulletin.org/Queries/Surveillance.aspx,Albania',
        'Africa,Algeria,NorthAfrica,countrywide,1,100.00%,"35,419,000",23,80000,0.00000065,0.002259,2008,Y,Y,"Dodet B, 2009",Algeria',
        'Americas,Argentina,SouthernCone,countrywide,0,100.00%,"40,666,000",0,37887,0,0.000931663,2009,Y,Y,"REDIPRA XIII, BUENOS AIRES, ARGENTINA-PANAFTOSA/OPS, 2010 / PAN AMERICAN FOOT-AND-MOUTH DISEASE CENTER website: http://ww3.panaftosa.org.br/siepi/Mensais.aspx",Argentina']
        
        test_data = RabiesAnalyzer.parse_data(None, test_file)
        self.assertEqual(test_data[0], RabiesInfo('Africa','Algeria', 'Y', 35419000, 23, 80000, 2008))
        self.assertEqual(test_data[1], RabiesInfo('Americas','Argentina', 'Y', 40666000, 0, 37887, 2009))
        self.assertEqual(test_data[2], RabiesInfo('Europe','Albania', 'N', 3169000, 0, 0, 2009))
        self.assertEqual(test_data[3], RabiesInfo('Europe','Albania', 'N', 3169000, 0, 0, 2010))

if __name__ == "__main__":
    unittest.main()