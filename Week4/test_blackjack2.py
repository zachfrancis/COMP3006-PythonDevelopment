#!/usr/bin/env python3

import unittest
from blackjack2 import score, stand

class TestBlackjack(unittest.TestCase):

    def test_score(self):
        test_cases = [
            {'hand' : [3,12],      'total': 13, 'soft_aces' : 0},
            {'hand' : [5,5,10],    'total': 20, 'soft_aces' : 0},
            {'hand' : [11,10,1],   'total': 21, 'soft_aces' : 0},
            {'hand' : [1,5],       'total': 16, 'soft_aces' : 1},
            {'hand' : [1,1,5],     'total': 17, 'soft_aces' : 1},
            {'hand' : [1,1,1,7],   'total': 20, 'soft_aces' : 1},
            {'hand' : [7,8,10],    'total': 25, 'soft_aces' : 0},
            {'hand' : [7,1,13,1],  'total': 19, 'soft_aces' : 0},
            {'hand' : [1,1,1,1,1], 'total': 15, 'soft_aces' : 1},
            {'hand' : [13,12,11],  'total': 30, 'soft_aces' : 0},
        ]

        for test_case in test_cases:
            with self.subTest():
                s = score(test_case['hand'])
                self.assertEqual(s.total, test_case['total'])
                self.assertEqual(s.soft_ace_count, test_case['soft_aces'])

    def test_stand_true(self):
        ret = stand(17, True, [1,1,5])
        self.assertTrue(ret.stand)
        self.assertEqual(ret.total, 17)

        ret = stand(17, False, [13, 7])
        self.assertTrue(ret.stand)
        self.assertEqual(ret.total, 17)

        ret = stand(14, True, [1,1,1,1])
        self.assertTrue(ret.stand)
        self.assertEqual(ret.total, 14)

    def test_stand_false(self):
        ret = stand(17, False, [1,1,5])
        self.assertFalse(ret.stand)
        self.assertEqual(ret.total, 17)

        ret = stand(17, True, [11,4])
        self.assertFalse(ret.stand)
        self.assertEqual(ret.total, 14)

        ret = stand(17, True, [1,1])
        self.assertFalse(ret.stand)
        self.assertEqual(ret.total, 12)

if __name__ == '__main__':
    unittest.main()