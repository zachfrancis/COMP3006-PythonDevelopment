#!/usr/bin/env python3

import unittest
from blackjack import score, stand

class TestBlackjack(unittest.TestCase):

    def test_score(self):
        test_cases = [
            [[3,12],        (13,0)],
            [[5,5,10],      (20,0)],
            [[11,10,1],     (21,0)],
            [[1,5],         (16,1)],
            [[1,1,5],       (17,1)],
            [[1,1,1,7],     (20,1)],
            [[7,8,10],      (25,0)],
            [[7,1,13,1],    (19,0)],
            [[1,1,1,1,1],   (15,1)],
            [[13,12,11],    (30,0)]
        ]

        for test_case in test_cases:
            with self.subTest():
                self.assertEqual(score(test_case[0]), test_case[1])

    def test_stand(self):
        # True cases
        self.assertTrue(stand(17, True, [1,1,5]))
        self.assertTrue(stand(17, False, [13,7]))
        self.assertTrue(stand(14, True, [1,1,1,1]))

        # False cases
        self.assertFalse(stand(17, False, [1,1,5]))
        self.assertFalse(stand(17, True, [11,4]))
        self.assertFalse(stand(17, True, [1,1]))

if __name__ == '__main__':
    unittest.main()