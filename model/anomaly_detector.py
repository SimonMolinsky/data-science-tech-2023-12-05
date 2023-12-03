from typing import Dict

import numpy as np
import json


class AnomalyDetector:
    def __init__(self):
        self.n_std = None
        self.mean_train = None
        self.std_train = None
        self.lower_limit = None
        self.upper_limit = None
        self.trained = False

    def fit(self, ds, n_std=1.5):
        """
        Function detects 1st and 3rd quartile from a dataset, and estimates limits for anomaly detection
        using formula ``QUART(ds) +/- n_std * STD(ds)``,
        where + is used for values above the 3rd quartile, and - for values below the 1st quartile.

        Parameters
        ----------
        ds : array-like
            List or array with values.

        n_std : float
            Number of standard deviations from quartile to assign value as an anomaly.
        """
        std_train = np.std(ds)
        lower_limit = np.quantile(ds, q=0.25) - (std_train * n_std)
        upper_limit = np.quantile(ds, q=0.75) + (std_train * n_std)
        self.n_std = n_std
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.std_train = std_train
        self.mean_train = np.mean(ds)
        self.trained = True

    def predict(self, ds):
        """
        Function returns indexes of points that are outliers and their absolute number of standard deviations
        from the mean of a training dataset.

        Parameters
        ----------
        ds : array-like
            List or array with values.

        Returns
        -------
        anomalies : Dict
            ``{index: (value, number of std's from the mean of training dataset)}``
        """

        ds = np.array(ds).flatten()
        mask = (ds > self.upper_limit) | (ds < self.lower_limit)
        anomalies = {
            idx: (value, self._number_of_stds(value))
            for idx, value in enumerate(ds)
            if mask[idx]
        }
        return anomalies

    def _number_of_stds(self, value):
        diff = np.abs(self.mean_train - value)
        no_stds = diff / self.std_train
        return no_stds


def save_model(model: AnomalyDetector, storage_path: str):
    """
    Function saves model for further usage.

    Parameters
    ----------
    model : AnomalyDetector

    storage_path : str

    Returns
    -------
    storage_path : str

    Raises
    ------
    AttributeError
        Model is not trained!
    """
    if model.trained:
        with open(storage_path, "w") as model_output:
            json.dump(model.__dict__, model_output)
    else:
        raise AttributeError("Model is not trained, cannot save!")


def load_model(storage_path: str) -> AnomalyDetector:
    """
    Function loads model.

    Parameters
    ----------
    storage_path : str

    Returns
    -------
    : AnomalyDetector
        Trained model.
    """
    model = AnomalyDetector()
    with open(storage_path, "r") as model_input:
        data = json.load(model_input)

    model.__dict__.update(data)
    return model
