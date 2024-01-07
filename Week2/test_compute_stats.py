import unittest
from compute_stats2 import compute_stats

# Run tests with python3 -m unittest -v test_compute_stats.p

class TestComputeStates(unittest.TestCase):

    # Test empty list as input
    def test_empty_list(self):
        ret = compute_stats(list())
        self.assertTupleEqual(ret,(None, None, None, None))

    # Test list with even number of values as input
    def test_even_list(self):
        test_list = [2, 3, 4, 5, 6, 7]
        expected_result = (2, 7, 4.5, 4.5)
        ret = compute_stats(test_list)
        self.assertTupleEqual(ret, expected_result)

    # Test list with odd number of values as input
    def test_odd_list(self):
        test_list = [3, 5, 9, 15, 21]
        expected_result = (3, 21, 10.6, 9)
        ret = compute_stats(test_list)
        self.assertTupleEqual(ret, expected_result)

    # Test list with only a single entry
    def test_single_entry_list(self):
        test_list = [1]
        expected_result = (1, 1, 1, 1)
        ret = compute_stats(test_list)
        self.assertTupleEqual(ret, expected_result)

    # Test list with non-numeric entry
    def test_nonnumeric_list(self):
        test_list = [1,2,"three",4]
        with self.assertRaises(TypeError):
            compute_stats(test_list)
