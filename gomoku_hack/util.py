import numpy as np


def array_nan_equal(a, b):
    return ((a == b) | (np.isnan(a) & np.isnan(b))).all()