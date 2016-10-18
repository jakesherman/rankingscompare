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


def spearman_rho(l1, l2, reverse = True, ranks = False):
    """Compute Spearman's rho, effectively Pearson's correlation on the ranks
    themselves. It is a non-parametric measure of rank correlation that assesses
    the monotonic relationship between two variables.

    Parameters
    ----------
    l1: list
        a list of values
    l2: list
        a list of values
    reverse: bool (default is True)
        whether to rank values in descending order (True) or ascending order
        (False)
    ranks: bool (default is False)
        Are l1 and l2 lists of values, or ranks? False indicates that these are
        lists of values, True indicates that the lists contain ranks.

    Returns
    -------
    Spearman's rho : float in [-1, 1]
    """
    if not ranks:
        l1, l2 = to_rank(l1, reverse = reverse), to_rank(l2, reverse = reverse)
    return pearson_r(l1, l2)


def _spearman_rho(l1, l2, reverse = True):
    """Not for export, just using to validate the results of the spearman_rho
    function. _spearman_rho only works if all n ranks are distinct integers.
    """
    assert len(l1) == len(l2), 'list inputs must be paired aka of = length!'
    l1, l2 = to_rank(l1, reverse = reverse), to_rank(l2, reverse = reverse)
    term = np.sum([np.power(xi - yi, 2) for xi, yi in zip(l1, l2)])
    return 1 - ((6 * term) / (len(l1) * (np.power(len(l1), 2) - 1)))


def spearman_footrule(l1, l2, reverse = True, ranks = False):
    """Compute Spearman's Footrule (Fr), the Manhatten distance between the
    ranks themselves. Only works on conjoint data, and is not top-weighted. A
    major weakness is that it only takes into account relative rankings.

    Parameters
    ----------
    l1: list
        a list of values
    l2: list
        a list of values
    reverse: bool (default is True)
        whether to rank values in descending order (True) or ascending order
        (False)
    ranks: bool (default is False)
        Are l1 and l2 lists of values, or ranks? False indicates that these are
        lists of values, True indicates that the lists contain ranks.

    Returns
    -------
    Spearman's footrule : int in [0, 0.5Z^2 if even, 0.5(Z + 1)(Z - 1) if odd]
    """
    assert len(l1) == len(l2), 'list inputs must be paired aka of = length!'
    if not ranks:
        l1, l2 = to_rank(l1, reverse = reverse), to_rank(l2, reverse = reverse)
    return int(np.sum([np.absolute(xi - yi) for xi, yi in zip(l1, l2)]))


def normalized_spearman_footrule(l1, l2, reverse = True, ranks = False,
    sim = False):
    """Normalized version of Spearman's Footrule (NFr) that divides the value of
    Spearman's Footrul by the maximum possible value, resulting in a value in
    the domain of [0, 1]. Described in Aguillo et al. [2010].

    Parameters
    ----------
    l1: list
        a list of values
    l2: list
        a list of values
    reverse: bool (default is True)
        whether to rank values in descending order (True) or ascending order
        (False)
    ranks: bool (default is False)
        Are l1 and l2 lists of values, or ranks? False indicates that these are
        lists of values, True indicates that the lists contain ranks.
    sim: bool (default is False)
        By default, NFr is returned, which is akin to a distance measure. If we
        are instead interested in a distance measure, setting sim = True outputs
        F, where F = 1 - NFr (where 1 indicates complete similarity instead of
        0).

    Returns
    -------
    Spearman's normalized footrule : float in [0, 1]
    """
    Z = len(l1)
    if even(Z):
        max_sf = 0.5 * np.power(Z, 2)
    else:
        max_sf = 0.5 * (Z + 1) * (Z - 1)
    NFr = spearman_footrule(l1, l2, reverse, ranks) / max_sf
    if sim:
        return 1 - NFr  # -- F = 1 - NFr
    else:
        return NFr
