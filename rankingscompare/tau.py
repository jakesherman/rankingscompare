from __future__ import division, print_function

"""tau.py - implementing Kendall's Tau and AP correlation, a top-weighted
version of Kendalls' Tau.
"""

import itertools
import numpy as np
from utilities import *


def tau_statistics(l1, l2, combinations):
    """Calculates the statistics used to compute the various correlation
    statistics based on Kendall's Tau given two lists of numbers, and a list of
    tuples, which each tuple consisting of a pair of indexes that can be used to
    index either l1 or l2.
    """
    assert len(l1) == len(l2), 'l1 and l2 must be paired data w/ equal length'
    n, concordant, discordant, l1_ties, l2_ties = len(l1), 0, 0, 0, 0
    pairs = len(combinations)
    for combo in combinations:
        xi, yi, xj, yj = l1[combo[0]], l2[combo[0]], l1[combo[1]], l2[combo[1]]
        l1_sign, l2_sign = sign(xi - xj), sign(yi - yj)
        ties = l1_sign == 0 or l2_sign == 0
        if not ties:
            concordant += l1_sign == l2_sign
            discordant += l1_sign != l2_sign
        else:
            l1_ties += l1_sign == 0
            l2_ties += l2_sign == 0
    return pairs, concordant, discordant, l1_ties, l2_ties


def tau_a(l1, l2):
    """Compute tau-a, which does not account for ties. Inputs are two equal
    length lists with matching pairs at each index.

    Kendall's Tau is a rank correlation statisic for conjoint ranked lists that
    is not top-weighted, and not appropriate for indefinite lists. It estimates
    a population parameter, the proability of concordance minus the probability
    of discordance. Computation time is O(n^2).
    """
    pairs, concordant, discordant, l1_ties, l2_ties = tau_statistics(l1, l2,
        list(itertools.combinations(range(len(l1)), 2)))
    if l1_ties + l2_ties > 0:
        raise Exception('No ties are allowed in tau_a!')
    return (concordant - discordant) / pairs


def tau_b(l1, l2):
    """Compute tau-b, which accounts for ties. Inputs are two equal
    length lists with matching pairs at each index.

    Kendall's Tau is a rank correlation statisic for conjoint ranked lists that
    is not top-weighted, and not appropriate for indefinite lists. It estimates
    a population parameter, the probability of concordance minus the probability
    of discordance. Computation time is O(n^2).
    """
    pairs, concordant, discordant, l1_ties, l2_ties = tau_statistics(l1, l2,
        list(itertools.combinations(range(len(l1)), 2)))
    denominator = np.sqrt((pairs - l1_ties) * (pairs - l2_ties))
    return (concordant - discordant) / denominator


def ap_correlation_combinations(l1, greater_is_better = True):
    """Creates a list of combination tuples that are valid in AP correlation.
    If i = 1, 2, ... n and j = 1, 2, ..., n then only consider combinations
    starting at i = 2 only where j > i (higher rank).
    """
    rank_pairs = []
    data = sorted([[rank, i] for i, rank in enumerate(
        to_rank(l1, 'notallowed'))])
    ranks = [rank_i[0] for rank_i in data]
    for i in ranks:
        if i == 1:
            continue
        for j in ranks:
            if i == j:
                continue
            elif j < i:
                rank_pairs.append((i, j))
    rank_to_i = dict(data)
    for rank1, rank2 in rank_pairs:
        pairs.append((rank_to_i[rank1], rank_to_i[rank2]))
    return pairs


def ap_correlation(l1, l2, symmetric = False, greater_is_better = True):
    """Compute the AP correlation coefficient, proposed by Yilmaz et al. [2008]
    as an alternative version of Kendall's Tau that is top-weighted. Does not
    account for ties!

    AP correlation is not symmetric by default - l2 is the 'definitive'
    ranked list, and l1 is being compared to l1. In other words,
    ap_correlation(a, b) != ap_correlation(b, a). Setting symmetric to True
    takes the mean of ap_correlation(a, b) and ap_correlation(b, a). If
    symmetric is set to True, it doesn't matter which ranked list is l1 and
    which is l2.
    """
    if symmetric:
        a_b = ap_correlation(l1, l2, False, greater_is_better)
        b_a = ap_correlation(l2, l1, False, greater_is_better)
        return (a_b + b_a) / 2
    pairs, concordant, discordant, l1_ties, l2_ties = tau_statistics(l1, l2,
        ap_correlation_combinations(l1, greater_is_better))
    if l1_ties + l2_ties > 0:
        raise Exception('No ties are allowed in ap_correlation')
    return (concordant - discordant) / pairs
