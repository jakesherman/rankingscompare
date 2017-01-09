from __future__ import division, print_function

"""Implementing Knight's algorithm to replace the tau_stats function. Instead
of running in O(n^2), we will be able to get concordances, discordances, ties,
etc. in O(n log n) time.
"""

import numpy as np
from utilities import *


################################################################################
# Knight's algorithm for computing tau-a, b, c, etc.
################################################################################


def merge(B, C):
    """Merge sorted arrays B and C into a new sorted array D. O(len(B + C)),
    also report the number of inversions that have occured thus far.
    """
    D, discordances_at_column, rows_remaining = [], 0, len(B)
    concordances, discordances, ties = len(B) * len(C), 0, 0
    while len(B) > 0 and len(C) > 0:
        first_B, first_C = B[0], C[0]
        if first_B <= first_C:
            D.append(B.pop(0))
            discordances += discordances_at_column
            rows_remaining -= 1
            if first_B == first_C:
                ties += 1
        else:
            D.append(C.pop(0))
            discordances_at_column += 1
    if B:
        D.extend(B)
        discordances += discordances_at_column * rows_remaining
    elif C:
        D.extend(C)
    concordances = concordances - discordances - ties
    return D, concordances, discordances, ties


def mergesort_tau(array):
    """Iterative implementation of the merge sort algorithm, which takes
    O(n log n) time, that also counts the number of concordances, discordances,
    and ties in an array (where the correct order is ascending order). Returns
    a tuple of concordances, discordances, and ties.
    """
    sorted_array = [[item] for item in array]
    i, n = 0, len(sorted_array)
    total_concordances, total_discordances, total_ties = 0, 0, 0
    while n > 1:
        while i < (n // 2):
            sorted_array[i], concordances, discordances, ties = merge(
                sorted_array[i], sorted_array.pop(i + 1))
            i += 1
            total_concordances += concordances
            total_discordances += discordances
            total_ties += ties
        i, n = 0, len(sorted_array)
    return total_concordances, total_discordances, total_ties


def knights_algorithm(X, Y):
    """Modified merge sort algorithm that computes the number of concordances,
    discordances, and ties between two numeric variables in O(n log n) time, as
    opposed to the naive method of iterating over all combinations of size 2
    between the two variables, which takes O(n^2) time.
    """
    sorted_by_X = sorted([(x, y) for x, y in zip(X, Y)])



################################################################################
# Knight's algorithm for computing AP correlation, tau-h (Vigna 2014), etc.
################################################################################
