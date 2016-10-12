from __future__ import division, print_function

"""spearman.py - the classic Spearman's rho ranking correlation coefficient,
which is just Pearson's product-moment correlation coefficient on the ranks
themselves.
"""

import itertools
import numpy as np
from utilities import conjoint, to_rank, unique


def variance(l1, bessel_correction = True):
    """Variance of a list or array of numbers.
    """
    l1 = np.array(l1)
    return np.sum(np.square(l1 - np.mean(l1))) / (len(l1) - bessel_correction)


def std_dev(l1):
    """Standard deviation of a list or array of numbers.
    """
    return np.sqrt(variance(l1))


def covariance(l1, l2, bessel_correction = True):
    """Covariance of two lists or arrays of numbers.
    """
    l1, l2 = np.array(l1), np.array(l2)
    assert len(l1) == len(l2), 'lists/arrays must be of same length!'
    product_sum = np.sum((l1 - np.mean(l1)) * (l2 - np.mean(l2)))
    return product_sum / (len(l1) - bessel_correction)


def pearson_r(l1, l2):
    """Compute Pearson's product-moment correlation coefficient on two lists or
    arrays of numbers.
    """
    return covariance(l1, l2) / (std_dev(l1) * std_dev(l2))


def spearman_rho(l1, l2, reverse = True):
    """Compute Spearman's rho, effectively Pearson's correlation on the ranks
    themselves. This is the quintessential rank correlation measurement.
    """
    l1, l2 = to_rank(l1, reverse = reverse), to_rank(l2, reverse = reverse)
    return pearson_r(l1, l2)


def spearman_footrule(l1, l2, reverse = True):
    """Compute Spearman's Footrule, the Manhatten distance between the ranks
    themselves.
    """
    l1, l2 = to_rank(l1, reverse = reverse), to_rank(l2, reverse = reverse)
    return np.sum([np.absolute(xi - yi) for xi, yi in zip(l1, l2)])
