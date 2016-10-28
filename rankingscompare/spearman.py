from __future__ import division, print_function

"""spearman.py - the classic Spearman's rho and Spearman's Footrule.
"""

import itertools
import numpy as np
from utilities import *


def variance(l1, bessel_correction = True):
    """Variance of a list or array of numbers.
    """
    l1 = np.array(l1)
    return sum(np.square(l1 - np.mean(l1))) / (len(l1) - bessel_correction)


def std_dev(l1):
    """Standard deviation of a list or array of numbers.
    """
    return np.sqrt(variance(l1))


def covariance(l1, l2, bessel_correction = True):
    """Covariance of two lists or arrays of numbers.
    """
    l1, l2 = np.array(l1), np.array(l2)
    assert len(l1) == len(l2), 'lists/arrays must be of same length!'
    product_sum = sum((l1 - np.mean(l1)) * (l2 - np.mean(l2)))
    return product_sum / (len(l1) - bessel_correction)


def pearson_r(X, Y):
    """Pearson's product-moment correlation coefficient, which measures the
    linear association between two continuous random variables. If the two
    variables are bivariate normal, this measure provides an exhaustive
    description of the association.

    If the two continous random variables do not follow a bivariate normal
    distribution, OR contain outliers, Spearman's rho may be a more appropriate
    correlation coefficient. If two random variables are not continous and
    instead are ordinal, Pearson's correlation is not appropriate.

    Parameters
    ----------
    X : list of floats/ints
        first continous random variable
    X : list of floats/ints
        second continous random variable

    Returns
    -------
    Pearson's correlation in [-1, 1], a float
    """
    assert len(X) == len(Y), 'list inputs must be paired aka of = length!'
    return covariance(X, Y) / (std_dev(X) * std_dev(Y))


def spearman_rho(X, Y, reverse = True, ranks = False):
    """Spearman's rho, which is Pearson's correlation on the ranks of two random
    variables instead of their values (or, directly on inputted ranks if the
    values are not known - see the ranks = True argument).

    Spearman's correlation is a non-parametric measure of rank correlation that
    assesses the monotonic relationship between two variables. Oberservations
    with large moments (outliers) are better handled by Spearman's correlation
    than Pearson's correlation.

    Parameters
    ----------
    X : list of floats/ints
        first continous random variable
    X : list of floats/ints
        second continous random variable
    reverse : bool (default is True)
        whether to rank values in descending order (True) or ascending order
    ranks : bool (default is False)
        Are X and Y lists of values, or ranks? False indicates that these are
        lists of values, True indicates that the lists contain ranks.

    Returns
    -------
    Spearman's rho : float in [-1, 1]
    """
    if not ranks:
        X, Y = to_rank(X, reverse = reverse), to_rank(Y, reverse = reverse)
    return pearson_r(X, Y)


def top_down_correlation(X, Y, reverse = True, ranks = False):
    """Top-down correlation coefficient introduced by Iman and Conover [1987],
    that is essentially Spearman's rho, but on Savage scores instead of ranks.
    Instead of giving equal importance to all ranks, the top-down correlation
    coefficient is top-heavy, emphasizing higher ranks.

    Savage scores were introduced by Savage [1956], where the function
    Savage(rank, rank_vector) is the sum of the rank reciprocals from the
    inputted rank to the lowest rank in the rank vector. Ex. if we have a rank
    vector [1, 2, 3, 4], and we want to know the savage score of the second
    element, rank 2, we would sum 1/2, 1/3 and 1/4.

    Parameters
    ----------
    X : list of floats/ints
        first continous random variable
    X : list of floats/ints
        second continous random variable
    reverse : bool (default is True)
        whether to rank values in descending order (True) or ascending order
    ranks : bool (default is False)
        Are X and Y lists of values, or ranks? False indicates that these are
        lists of values, True indicates that the lists contain ranks.

    Returns
    -------
    Spearman's rho : float in [-1, 1]
    """
    assert len(X) == len(Y), 'list inputs must be paired aka of = length!'
    if not ranks:
        X, Y = to_rank(X, reverse = reverse), to_rank(Y, reverse = reverse)
    X, Y = to_savage_scores(X), to_savage_scores(Y)
    return pearson_r(X, Y)


def spearman_footrule(X, Y, reverse = True, ranks = False, measure = 'raw'):
    """Spearman's Footrule (Fr), the Manhatten distance between the ranks of two
    random variables. Not top-weighted. A major weakness is that it only takes
    into account relative rankings.

    Parameters
    ----------
    X : list of floats/ints
        first continous random variable
    X : list of floats/ints
        second continous random variable
    reverse : bool (default is True)
        whether to rank values in descending order (True) or ascending order
    ranks : bool (default is False)
        Are X and Y lists of values, or ranks? False indicates that these are
        lists of values, True indicates that the lists contain ranks.
    measure : str (default is raw)
        raw -> the raw Manhatten distance between ranks
        distance -> normalizes the raw output into a distance metric by dividing
            the raw Manhatten distance by the maximum possible raw Manhatten
            distance
        similarity -> 1 - distance, get a similarity score instead of a distance
            metric

    Returns
    -------
    Spearman's footrule : int in [0, 0.5Z^2 if even, 0.5(Z + 1)(Z - 1) if odd]
    """
    assert measure in ['raw', 'distance', 'similarity'], 'incorrect metric'
    assert len(X) == len(Y), 'list inputs must be paired aka of = length!'
    if measure != 'raw':
        max_df = 0.5 * (len(X) ** 2 - odd(len(X)))
        NFr = spearman_footrule(X, Y, reverse, ranks, 'raw') / max_sf
        return {'distance': NFr, 'similarity': 1 - NFr}[measure]
    else:
        if not ranks:
            X, Y = to_rank(X, reverse = reverse), to_rank(Y, reverse = reverse)
        return int(sum([np.absolute(xi - yi) for xi, yi in zip(X, Y)]))
