from __future__ import division, print_function

"""tau.py - rank correlation metrics that basically measure the probability of
concordance minus the probability of discordance.
"""

import itertools
import numpy as np
from utilities import *
from warnings import warn


def tau_stats(l1, l2):
    """Calculates the statistics used to compute the various correlation
    statistics based on Kendall's tau given two lists of numbers, and a list of
    tuples, which each tuple consisting of a pair of indexes that can be used to
    index either l1 or l2. Computing these is O(n^2).
    """
    assert len(l1) == len(l2), 'l1 and l2 must be paired data w/ equal length'
    combinations = list(itertools.combinations(range(len(l1)), 2))
    n, concordant, discordant, l1_ties, l2_ties = len(l1), 0, 0, 0, 0
    pairs, m = len(combinations), min([len(set(l1)), len(set(l2))])
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
    return pairs, concordant, discordant, l1_ties, l2_ties, m


def tau_a(l1, l2):
    """tau-a, which does not account for ties. Inputs are two equal
    length lists with matching pairs at each index.

    Kendall's tau is a rank correlation statisic for conjoint ranked lists that
    is not top-weighted, and not appropriate for indefinite lists. It estimates
    a population parameter, the proability of concordance minus the probability
    of discordance.

    Parameters
    ----------
    l1: list
        a list of values
    l2: list
        a list of values

    Returns
    -------
    Kendall's tau-a: float in [-1, 1]
    """
    pairs, concordant, discordant, l1_ties, l2_ties, m = tau_stats(l1, l2)
    if l1_ties + l2_ties > 0:
        warn('tau-a does not adjust for ties')
    return (concordant - discordant) / pairs


def tau_b(l1, l2):
    """tau-b, which accounts for ties. Most suitable for square tables.

    Kendall's tau is a rank correlation statisic for conjoint ranked lists that
    is not top-weighted, and not appropriate for indefinite lists. It estimates
    a population parameter, the probability of concordance minus the probability
    of discordance.

    Parameters
    ----------
    l1: list
        a list of values
    l2: list
        a list of values

    Returns
    -------
    Kendall's tau-b: float in [-1, 1]
    """
    pairs, concordant, discordant, l1_ties, l2_ties, m = tau_stats(l1, l2)
    denominator = np.sqrt((pairs - l1_ties) * (pairs - l2_ties))
    return (concordant - discordant) / denominator


def tau_c(l1, l2):
    """tau-c, optimized for larger, rectangular tables. No adjustment for ties.
    """
    pairs, concordant, discordant, l1_ties, l2_ties, m = tau_stats(l1, l2)
    if l1_ties + l2_ties > 0:
        warn('tau-c does not adjust for ties')
    denominator = (2 * m) / (np.power(len(l1), 2) * (m - 1))
    return (concordant - discordant) / denominator


def gamma(l1, l2):
    """Goodman - Kruskal Gamma (G), very similar to Kendall's tau. Gamma is the
    difference in concordant pairs and discordant pairs as a percentage of all
    possible pairs, ignoring ties.

    Reference: http://www.unesco.org/webworld/idams/advguide/Chapt4_2.htm

    Parameters
    ----------
    l1: list
        a list of values
    l2: list
        a list of values

    Returns
    -------
    Goodman - Kruskal Gamma: float in [-1, 1]
    """
    pairs, concordant, discordant, l1_ties, l2_ties, m = tau_stats(l1, l2)
    return (concordant - discordant) / (concordant + discordant)


def sommers_d(l1, l2, dependent = 'symmetric'):
    """Somers' D, a measure of ordinal association between l1 and l2. Similar to
    Kendall's tau and the Gamma statistic.

    Ref: https://stats.stackexchange.com/questions/18112

    Parameters
    ----------
    l1: list
        a list of values
    l2: list
        a list of values
    dependent: str (default is symmetric)
        Decides whether to make the l1 variable dependent, the l2 variable
        dependent, or being symmetric and taking the arithmetic mean of having
        each variable be dependent.
    Returns
    -------
    Sommers' D: float in [-1, 1]
    """
    pairs, concordant, discordant, l1_ties, l2_ties, m = tau_stats(l1, l2)
    if dependent == 'symmetric':
        return (sommers_d(l1, l2, 'l1') + sommers_d(l1, l2, 'l2')) / 2
    denominators = {
        'l1': concordant + discordant + l1_ties,
        'l2': concordant + discordant + l2_ties
    }
    return (concordant - discordant) / denominators[dependent]


def ap_correlation(l1, l2, symmetric = False, reverse = True):
    """The AP correlation coefficient, proposed by Yilmaz et al. [2008] as an
    alternative version of Kendall's Tau that is top-weighted. Does not account
    for ties! Implementation is O(n^2), until Knight's algorithm is implemented.

    Parameters
    ----------
    l1: list
        a list of values
    l2: list
        a list of values
    symmetric: bool (default is False)
        AP correlation is not symmetric by default - l2 is the 'definitive'
        ranked list, and l1 is being compared to l1. In other words, f(a, b) is
        not necessarily f(b, a). Setting symmetric to True takes the mean of
        f(a, b) and f(b, a). If symmetric is set to True, it doesn't matter
        which ranked list is l1 and which is l2.
    reverse: bool (default is True)
        rank values in descending order (True) or ascending order (False)

    Returns
    -------
    AP correlation: float in [-1, 1]
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
