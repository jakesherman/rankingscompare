import functools
import numpy as np
import random
import rankingscompare as rc
from scipy.stats import kendalltau
import unittest


def generate_test_case(max_length = 100, ties = False):
    """Generate random lists of numbers of maximum length [max_length] to use
    in testing. Return a tuple of list1, list2.
    """
    list_length = random.sample(range(2, max_length + 1), 1)[0]
    if ties:
        a = np.random.choice(list_length, list_length)
        b = np.random.choice(list_length, list_length)
    else:
        a = random.sample(range(list_length), list_length)
        b = random.sample(range(list_length), list_length)
    return a, b


generate_test_case_ties = functools.partial(generate_test_case, ties = True)


def approx_equal(num1, num2, significant = 2):
    """Are two numbers approximately equal?
    """
    try:
        np.testing.assert_approx_equal(num1, num2, significant = significant)
        return True
    except AssertionError:
        return False


def test_rank_func(func1, func2, test_func, num_tests = 100):
    """Test that func1 equals func2 for [num_tests] tests, using the function
    test_func to generate two equal length arrays of numbers to use. func1 and
    func2 must accept two arguments: l1 and l2, two equal-length lists of nums.
    """
    successes = 0
    for test_case in [func() for func in [test_func] * num_tests]:
        func1val, func2val = func1(*test_case), func2(*test_case)
        if not approx_equal(func1val, func2val):
            print 'Different values (func1, func2): {0} != {1}'.format(
                func1val, func2val)
            print '> Number of successes: {0}'.format(str(successes))
            return False
        successes += 1
    return True


def scipy_kendalltau(*args, **kwargs):
    """Return just the correlation, not a tuple of that and the p-value.
    """
    return kendalltau(*args, **kwargs)[0]


class TauTestCases(unittest.TestCase):
    """Tests for the functions in tau.py
    """

    a, b, c = [1, 2, 3, 4, 5], [2, 1, 3, 4, 5], [1, 2, 3, 5, 4]
    d, e = [5, 4, 3, 2, 1], [2, 3, 4, 5, 6]

    # Test for non-negativity, should be 1
    def test_tau_a_1(self):
        self.assertTrue(rc.tau_a(self.a, self.a) == 1.0)

    # Complete opposite, should be -1
    def test_tau_a_2(self):
        self.assertTrue(rc.tau_a(self.a, self.d) == -1.0)

    # Random example, should both be 0.8
    def test_tau_a_3(self):
        self.assertTrue((rc.tau_a(self.a, self.b) == 0.8 and
        rc.tau_a(self.a, self.c) == 0.8))

    # Agreement w/ scipy's kendalltau function and tau_a, so NO TIES
    def test_same_tau_a_values(self):
        self.assertTrue(test_rank_func(rc.tau_a, scipy_kendalltau,
            generate_test_case))


if __name__ == '__main__':
    unittest.main()
