"""utilities.py
"""

import numpy as np


def unique(list):
    """True if every element in a list is unique, False otherwise.
    """
    return len(list) == len(set(list))


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

    Returns
    -------
    a list of floats corresponding to the ranks of the items in [list]
    """
    assert (all([isinstance(item, float) for item in mylist]) or
    all([isinstance(item, int) for item in mylist])), \
        'list must be a list of floats or integers!'
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
            pass
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
