from __future__ import division, print_function

"""tau.py - implementing Kendall's Tau and AP correlation, a top-weighted
version of Kendalls' Tau.
"""

import itertools
import numpy as np
from utilities import conjoint, unique


def kendall_tau(l1, l2):
    """Computes Kendall's Tau between two ranked lists. Kendall's Tau, a rank
    correlation metric for conjoint ranked lists that is not top-weighted, and
    not appropriate for indefinite lists. Assumes no ties.

    Parameters
    ----------
    l1 : list
        List of items in rank order (position 0 corresponds to rank 1, etc.)
    l2 : list
        List of items in rank order (position 0 corresponds to rank 1, etc.)

    Returns
    -------
    Rank correlation in the set [-1, 1]
    """
    assert unique(l1) and unique(l2), 'items in lists are not unique!'
    assert conjoint(l1, l2), 'l1 and l2 are not conjoint ranked lists!'
    num_pairs, num_concordant_pairs = 0, 0
    for combo in itertools.combinations(l1, 2):
        num_pairs += 1
        higher_ranked_l1 = l1.index(combo[0]) < l1.index(combo[1])
        higher_ranked_l2 = l2.index(combo[0]) < l2.index(combo[1])
        num_concordant_pairs += higher_ranked_l1 == higher_ranked_l2
    prob_concordant = num_concordant_pairs / num_pairs
    return 2 * prob_concordant - 1


def ap_correlation(l1, l2, symmetric = False):
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

    # Loop through every item ranked below 1 in l1, check to see if all pairs
    # with items of 'higher' (rank 1 > rank 2) in l1 are concordant with l2.
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
