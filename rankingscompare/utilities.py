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
