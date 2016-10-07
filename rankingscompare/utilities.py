"""utilities.py
"""


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
    ranks, num_ties = [], 0
    for pos, (item, i) in enumerate(data):
        if num_ties > 0:
            if ties == 'notallowed':
                raise Exception('Ties not allowed!')
            ranks.append(pos + 1 - num_ties)
        else:
            ranks.append(pos + 1)
        try:
            if item == data[pos + 1][0]:
                num_ties += 1
            else:
                num_ties = 0
        except:
            pass
    return ranks
