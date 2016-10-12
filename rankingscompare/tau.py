from __future__ import division, print_function

"""tau.py - implementing Kendall's tau and AP correlation, a top-weighted
version of Kendalls' Tau.
"""

import itertools
import numpy as np
from utilities import *


def tau_statistics(l1, l2, combinations):
    """Calculates the statistics used to compute the various correlation
    statistics based on Kendall's tau given two lists of numbers, and a list of
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

    Kendall's tau is a rank correlation statisic for conjoint ranked lists that
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

    Kendall's tau is a rank correlation statisic for conjoint ranked lists that
    is not top-weighted, and not appropriate for indefinite lists. It estimates
    a population parameter, the probability of concordance minus the probability
    of discordance. Computation time is O(n^2).
    """
    pairs, concordant, discordant, l1_ties, l2_ties = tau_statistics(l1, l2,
        list(itertools.combinations(range(len(l1)), 2)))
    denominator = np.sqrt((pairs - l1_ties) * (pairs - l2_ties))
    return (concordant - discordant) / denominator


def ap_correlation(l1, l2, symmetric = False, reverse = True):
    """Compute the AP correlation coefficient, proposed by Yilmaz et al. [2008]
    as an alternative version of Kendall's Tau that is top-weighted. Does not
    account for ties!

    AP correlation is not symmetric by default - l2 is the 'definitive'
    ranked list, and l1 is being compared to l1. In other words, f(a, b) is not
    necessarily f(b, a). Setting symmetric to True takes the mean of f(a, b) and
    f(b, a). If symmetric is set to True, it doesn't matter which ranked list is
    l1 and which is l2.
    """
    if symmetric:
        l1_l2 = ap_correlation(l1, l2, False, reverse)
        l2_l1 = ap_correlation(l2, l1, False, reverse)
        return (l1_l2 + l2_l1) / 2
    pos_rank = [[pos, rank] for pos, rank in
                zip(range(0, len(l1)), to_rank(l1, reverse = reverse))]
    l2_ranks = to_rank(l2, reverse = reverse)
    rank_specific_prob_concordants = []  # -- prob concordant for each rank
    for pos, rank in pos_rank:
        Ci = 0
        if rank == 1:  # -- can't be anything ranked higher, so we skip
            continue
        else:
            for subpos, subrank in pos_rank:
                if subrank < rank:
                    if l2_ranks[pos] > l2_ranks[subpos]:
                        Ci += 1
        rank_specific_prob_concordants.append(Ci / (rank - 1))
    prob_concordant = np.mean(rank_specific_prob_concordants)
    return 2 * prob_concordant - 1
