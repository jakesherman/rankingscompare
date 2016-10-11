from __future__ import division, print_function

"""tau.py - implementing Kendall's Tau and AP correlation, a top-weighted
version of Kendalls' Tau.
"""

import itertools
import numpy as np
from utilities import *


def tau_a(l1, l2):
    """Kendall's Tau between two lists of numbers. Kendall's Tau, a rank
    correlation statisic for conjoint ranked lists that is not top-weighted, and
    not appropriate for indefinite lists. Assumes no ties.

    Estimates a population parameter, the proability of concordance minus the
    probability of discordance. Complexity is O(n^2).

    Parameters
    ----------
    l1 : list
        List of numbers.
    l2 : list
        List of numbers.

    Returns
    -------
    Rank correlation in the set [-1, 1]
    """
    assert len(l1) == len(l2), 'l1 and l2 must be paired data w/ equal length'
    n, concordant = len(l1), 0
    pairs = choose(n, 2)
    for combo in itertools.combinations(range(0, n), 2):
        xi, yi, xj, yj = l1[combo[0]], l2[combo[0]], l1[combo[1]], l2[combo[1]]
        l1_sign, l2_sign = sign(xi - xj), sign(yi - yj)
        ties = l1_sign == 0 or l2_sign == 0
        if ties:
            raise Exception('No ties allowed in tau_a!')
        concordant += l1_sign == l2_sign
    return 2 * (concordant / pairs) - 1


def tau_statistics(l1, l2, combinations):
    """Calculates the statistics used to compute the various correlation
    statistics based on Kendall's Tau.
    """
    assert len(l1) == len(l2), 'l1 and l2 must be paired data w/ equal length'
    n, concordant, discordant, l1_ties, l2_ties = len(l1), 0, 0, 0, 0
    pairs = len(combinations)
    for combo in combinations:
        xi, yi, xj, yj = l1[combo[0]], l2[combo[0]], l1[combo[1]], l2[combo[1]]
        l1_sign, l2_sign = sign(xi - xj), sign(yi - yj)
        if not ties:
            concordant += l1_sign == l2_sign
            discordant += not concordant
        else:
            l1_ties += l1_sign == 0
            l2_ties += l2_sign == 0
    return pairs, concordant, discordant, l1_ties, l2_ties


def ap_correlation_combinations(l1, greater_is_better = True):
    """Creates a list of combination tuples that are valid in AP correlation.
    If i = 1, 2, ... n and j = 1, 2, ..., n then only consider combinations
    starting at i = 2 only where j > i (higher rank).
    """
    pairs = []
    for i in enumerate(l1):
        if i == 1:
            continue
        for j in enumerate(l1):
            if (greater_is_better and j>i) or (not greater_is_better and j<i):
                pairs.append((i, j))
    return pairs


def ap_correlation(l1, l2, symmetric = False, reverse = True):
    """Compute the AP correlation coefficient, proposed by Yilmaz et al. [2008]
    as an alternative version of Kendall's Tau that is top-weighted.

    Parameters
    ----------
    l1 : list
        List of items in rank order (position 0 corresponds to rank 1, etc.).
        The list to be compared against the definitive list (see info for the
        symmetric argument).
    l2 : list
        List of items in rank order (position 0 corresponds to rank 1, etc.).
        The 'definitive' ranked list (see info for the symmetric argument).
    symmetric : bool (default is False)
        AP correlation is not symmetric by default - l2 is the 'definitive'
        ranked list, and l1 is being compared to l1. in other words,
        ap_correlation(a, b) != ap_correlation(b, a). Setting symmetric to True
        takes the mean of ap_correlation(a, b) and ap_correlation(b, a). If
        symmetric is set to True, it doesn't matter which ranked list is l1 and
        which is l2.

    Returns
    -------
    Rank correlation in the set [-1, 1]
    """
    assert unique(l1) and unique(l2), 'items in lists are not unique!'
    assert conjoint(l1, l2), 'l1 and l2 are not conjoint ranked lists!'
    if symmetric:
        a_b = ap_correlation(l1, l2, False, reverse)
        b_a = ap_correlation(l2, l1, False, reverse)
        return (a_b + b_a) / 2

    # Loop through every item ranked below 1 in l1, check to see if all pairs
    # with items of 'higher' (rank 1 > rank 2) in l1 are concordant with l2.
    l1, l2 = to_rank(l1, reverse = reverse), to_rank(l2, reverse = reverse)
    sum_percent_concordant = 0
    for i, item in enumerate(l1, start = 1):
        if i == 1:
            continue
        concordant_pairs = 0
        for j, higher_ranked_item in enumerate(l1, start = 1):
            if j == i:
                break
            concordant_pairs += l2.index(higher_ranked_item) < l2.index(item)
        sum_percent_concordant += concordant_pairs / (i - 1)  # % concordant
    prob_concordant = sum_percent_concordant / (len(l1) - 1)
    return 2 * prob_concordant - 1
