"""utilities.py
"""

import math
import numpy as np


def unique(list):
    """True if every element in a list is unique, False otherwise.
    """
    return len(list) == len(set(list))


def ties(list):
    """True if there are going to be ties in a list of values to be converted to
    ranks, or ranks.
    """
    return not unique(list)


def conjoint(l1, l2):
    """True if l1 and l2 are conjoint, False otherwise.
    """
    return len(set(l1) - set(l2)) == 0 and len(set(l2) - set(l1)) == 0


def to_rank(mylist, ties = 'midrank', reverse = True):
    """Create a list of ranks corresponding to a list of integers or floats.

    Parameters
    ----------
    list : list
        List of floats or integers
    ties : str
        How to deal with ties. Options are
        midrank -> mean of the positions that ties are occupying
        same -> repeat the highest (rank 1 > rank 2) position of the ties
        notallowed -> ties aren't allowed, raise an exception if there are ties
    reverse : bool
        If True, higher numbers correspond to higher ranks (aka 1, 2, ...) and
        lower numbers correspond to lower ranks (ex. 15, 14, ...). If False,
        the opposite happens.

    Returns
    -------
    a list of floats corresponding to the ranks of the items in [list]
    """
    assert all([isinstance(item, float) or isinstance(item, int)
                for item in mylist]), 'list must be a list of floats or ints!'
    assert ties in ['midrank', 'same', 'notallowed'], 'incorrect ties method'
    data = sorted([[item, i] for i, item in enumerate(mylist)],
        reverse = reverse)
    ranks = []
    current_ties, ties_end = [], False
    for pos, (item, i) in enumerate(data):
        try:
            if item == data[pos + 1][0]:
                current_ties.append(pos + 1)
            else:
                if current_ties:
                    ties_end = True
        except:
            if current_ties:
                ties_end = True
        if len(current_ties) > 0 and ties_end:
            if ties == 'notallowed':
                raise Exception('No ties allowed!')
            current_ties.append(pos + 1)
            if ties == 'midrank':
                ranks += [np.mean(current_ties)] * len(current_ties)
            else:
                ranks += [min(current_ties)] * len(current_ties)
            current_ties, ties_end = [], False
        elif not current_ties:
            ranks.append(pos + 1)
    return [rank for i, rank in sorted(
        zip([item_i[1] for item_i in data], ranks))]


def sign(num):
    """Sign function - is a number positive, negative, or 0?
    """
    return num and (1, -1)[num < 0]


def choose(n, k):
    """n choose k
    """
    return math.factorial(n) / (math.factorial(k) * math.factorial(n - k))


def even(num):
    """True if a number if even, False if odd.
    """
    return not num % 2
