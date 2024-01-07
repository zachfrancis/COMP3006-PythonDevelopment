#!/usr/bin/env python3

import unittest
from blackjack3 import Hand, Strategy

class TestBlackjack(unittest.TestCase):

    def test_hand_score(self):
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
                h = Hand(test_case['hand'])
                self.assertEqual(h.total, test_case['total'])
                self.assertEqual(h.soft_ace_count, test_case['soft_aces'])

    def test_strategy_stand_true(self):
        s = Strategy(17, True)
        self.assertTrue(s.stand(Hand([1,1,5])))

        s = Strategy(17, False)
        self.assertTrue(s.stand(Hand([13,7])))

        s = Strategy(14, True)
        self.assertTrue(s.stand(Hand([1,1,1,1])))

    def test_strategy_stand_false(self):
        s = Strategy(17, False)
        self.assertFalse(s.stand(Hand([1,1,5])))
        
        s = Strategy(17, True)
        self.assertFalse(s.stand(Hand([11,4])))

        s = Strategy(17, True)
        self.assertFalse(s.stand(Hand([1,1])))


if __name__ == '__main__':
    unittest.main()