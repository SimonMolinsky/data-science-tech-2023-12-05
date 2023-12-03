from typing import List, Dict
from api_functions.detector.anomaly_detector import load_model


def predict(model_path: str, data: List) -> Dict:
    """
    Function predicts anomalies.

    Parameters
    ----------
    model_path : str

    data : List

    Returns
    -------
    : Dict
    """
    model = load_model(model_path)
    predictions = model.predict(data)
    return predictions
