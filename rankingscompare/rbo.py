from __future__ import division, print_function

"""rbo.py - implementing Rank-Biased Overlap, proposed by Webber et al. [2010],
and related functions.
"""

import itertools
import numpy as np
from utilities import *


def average_overlap(items1, items2, k = None):
    """Compute the average overlap (AO )between two ranked lists of items. Items
    must be in rank order, starting at 1. [k] is the depth to go down to when
    computing the AO - the maximum is the max of the lengths of the two lists,
    the min is 1.

    Proposed simultaneously by Fagin et al. [2003] and Wu and Crestani [2003],
    it is called the 'intersection metric' and 'average accuracy' by those
    authors, respectively. This is a similarity score between two sets of ranked
    items, not a correlation coeffcient like Kendall's tau or Spearman's rho.
    It works with non-conjoint data, on indefinite lists, and is top-weighted.
    The AO score is contained in the interval [0, 1].
    """
    if k is None:
        k = max([len(items1), len(items2)])
    assert k > 0 and k <= max([len(items1), len(items2)]), 'k is out of bounds!'
    agreements = []
    for i in range(1, k + 1):
        items1_set, items2_set = set(items1[:i]), set(items2[:i])
        agreement = len(items1_set.intersection(items2_set)) / i
        agreements.append(agreement)
    return np.mean(agreements)
