# Copyright (C) 2024 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher
# created: Wed Sep 18 2024


import numpy as np


def find_bin_thresholds(x, n_bins=4, lower_cut=None, upper_cut=None):
    """
    Find the bin threshold when splitting the data into equally populated bins.
    Lower and upper cuts can be defined which are then used as an additional bin
    between -inf and lower cut and upper cut and inf.
    This can e.g. be used to have a bin which you exclude from the analysis.

    :param x: data to bin
    :param n_bins: number of bins
    :param lower_cut: lower cut
    :param upper_cut: upper cut
    :return: bin thresholds
    """
    if lower_cut is None:
        select = np.ones(len(x), dtype=bool)
    else:
        select = x > lower_cut
    if upper_cut is not None:
        select &= x < upper_cut
    x = x[select]

    n_objects = len(x)
    n_objects_per_bin = n_objects // n_bins

    x_sorted = np.sort(x)
    bin_thresholds = [x_sorted[i * n_objects_per_bin] for i in range(1, n_bins)]
    if lower_cut is not None:
        lower_thresholds = [-np.inf, lower_cut]
    else:
        lower_thresholds = [-np.inf]
    if upper_cut is not None:
        upper_thresholds = [upper_cut, np.inf]
    else:
        upper_thresholds = [np.inf]
    return lower_thresholds + bin_thresholds + upper_thresholds
