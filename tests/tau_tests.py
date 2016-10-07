import numpy as np
import random
import rankingscompare as rc
from scipy.stats import kendalltau
import unittest


def generate_test_case(max_length = 10):
    """Generate random lists of numbers of maximum length [max_length] to use
    in testing. Return a tuple of list1, list2.
    """
    numbers = range(1, random.sample(range(2, max_length + 1), 1)[0] + 1)
    a = random.sample(numbers, len(numbers))
    b = random.sample(numbers, len(numbers))
    return a, b


def approx_equal(num1, num2, significant = 2):
    """Are two numbers approximately equal?
    """
    try:
        np.testing.assert_approx_equal(num1, num2, significant = significant)
        return True
    except AssertionError:
        return False


def same_kendall_tau_values():
    """Compares the results of my Kendall Tau implemention with the scipy
    implementation to make sure that my results are correct for some test cases.
    """
    successes = 0
    for test_case in [func() for func in [generate_test_case] * 100]:
        mykt, scipykt = rc.kendall_tau(*test_case), kendalltau(*test_case)[0]
        if not approx_equal(mykt, scipykt):
            print 'Different values (my, scipy): {0} != {1}'.format(
                mykt, scipykt)
            print '> Number of successes: {0}'.format(str(successes))
            return False
        successes += 1
    return True


class TauTestCase(unittest.TestCase):
    """Tests for the functions in tau.py
    """

    a, b, c = [1, 2, 3, 4, 5], [2, 1, 3, 4, 5], [1, 2, 3, 5, 4]
    d, e = [5, 4, 3, 2, 1], [2, 3, 4, 5, 6]

    # Test for non-negativity, should be 1
    def test_kendall_tau_1(self):
        self.assertTrue(rc.kendall_tau(self.a, self.a) == 1.0)

    # Complete opposite, should be -1
    def test_kendall_tau_2(self):
        self.assertTrue(rc.kendall_tau(self.a, self.d) == -1.0)

    # Should both be 0.8
    def test_kendall_tau_3(self):
        self.assertTrue((rc.kendall_tau(self.a, self.b) == 0.8 and
        rc.kendall_tau(self.a, self.c) == 0.8))

    # Should raise an AssertionError for non-conjoint lists
    def test_kendall_tau_4(self):
        self.assertRaises(AssertionError, rc.kendall_tau, self.a, self.e)

    # Should raise an AssertionError for non-unique lists
    def test_kendall_tau_5(self):
        self.assertRaises(AssertionError, rc.kendall_tau, [1, 1, 2], [1, 2, 2])

    # Agreement between myself and scipy
    def test_same_kendall_tau_values(self):
        self.assertTrue(same_kendall_tau_values())


if __name__ == '__main__':
    unittest.main()
