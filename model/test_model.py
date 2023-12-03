from typing import Dict

from anomaly_detector import AnomalyDetector, save_model, load_model

DATASET = [1, 2, 3, 0, 51, 52, 7, 3, 6]

adt = AnomalyDetector()
adt.fit(DATASET)
predicted = adt.predict(DATASET)
assert set(predicted.keys()) == {4, 5}
assert isinstance(predicted, Dict)

save_model(model=adt, storage_path='saved_model.json')

model = load_model('saved_model.json')
assert model.__dict__
