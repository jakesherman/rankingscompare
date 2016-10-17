from __future__ import division, print_function

"""spearman.py - the classic Spearman's rho and Spearman's Footrule.
"""

import itertools
import numpy as np
from utilities import *


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
    assert len(l1) == len(l2), 'list inputs must be paired aka of = length!'
    return covariance(l1, l2) / (std_dev(l1) * std_dev(l2))


def spearman_rho(l1, l2, reverse = True):
    """Compute Spearman's rho, effectively Pearson's correlation on the ranks
    themselves. This is the quintessential rank correlation measurement.
    """
    l1, l2 = to_rank(l1, reverse = reverse), to_rank(l2, reverse = reverse)
    return pearson_r(l1, l2)


def spearman_footrule(l1, l2, reverse = True):
    """Compute Spearman's Footrule (Fr), the Manhatten distance between the
    ranks themselves. Only works on conjoint data, and is not top-weighted. A
    major weakness is that it only takes into account relative rankings.
    """
    assert len(l1) == len(l2), 'list inputs must be paired aka of = length!'
    l1, l2 = to_rank(l1, reverse = reverse), to_rank(l2, reverse = reverse)
    return np.sum([np.absolute(xi - yi) for xi, yi in zip(l1, l2)])


def normalized_spearman_footrule(l1, l2, reverse = True, sim = False):
    """Normalized version of Spearman's Footrule (NFr) that divides the value of
    Spearman's Footrul by the maximum possible value, resulting in a value in
    the domain of [0, 1]. Described in Aguillo et al. [2010].

    By default, NFr is returned, which is akin to a distance measure. If we are
    instead interested in a distance measure, setting sim = True outputs F,
    where F = 1 - NFr (where 1 indicates complete similarity instead of 0).
    """
    Z = len(l1)
    if even(Z):
        max_sf = 0.5 * np.power(Z, 2)
    else:
        max_sf = 0.5 * (Z + 1) * (Z - 1)
    NFr = spearman_footrule(l1, l2, reverse) / max_sf
    if sim:
        return 1 - NFr  # -- F = 1 - NFr
    else:
        return NFr
