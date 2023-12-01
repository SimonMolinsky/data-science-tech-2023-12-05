from typing import Dict

import numpy as np
import joblib


class AnomalyDetector:
    pass


def transform(arr: np.ndarray, return_std=True) -> Dict:
    """
    Model returns mean and standard deviation of a dataset.

    Parameters
    ----------
    arr : numpy array
        Values to transform.

    return_std : bool, default = True
        Return standard deviation.

    Returns
    -------
    : Dict
        Dictionary with mean, median, and standard deviation of the array.

    Examples
    --------
    >>> from numpy import arange
    >>>
    >>>
    >>> myarr = arange(0, 5)
    >>> transformed = transform(myarr)
    >>> print(transformed['mean'], transformed['median'], f"{transformed['std']:.2f}")
    2.0 2.0 1.41

    """

    d = dict()
    d['mean'] = np.mean(arr)
    d['median'] = np.median(arr)
    d['std'] = np.std(arr)
    return d
