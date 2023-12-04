# Uruchomienie customowego modelu online z AWS SageMaker

## Opcja 1: AWS SageMaker + FastAPI

**Źródło**: Katarzyna Cepińska https://sii.pl/blog/en/deploying-custom-models-on-aws-sagemaker-using-fastapi/

1. Wytrenuj model.
2. Stwórz endpointy do obsługi modelu.
3. Zapakuj endpointy w kontener Dockera.
4. Wyślij kontener do ECR.
5. Zapisz wytrenowany model na S3.
6. Stwórz wejście modelu do SageMaker z Boto3 i Pythonem. Musisz posiadać rolę z odpowiednimi uprawnieniami, adres kontenera z modelem, adres modelu na s3, nazwę modelu.
7. Zaalokuj zasoby na endpoint.
8. Wystaw i przetestuj model.

## Opcja 2: AWS SageMaker + MLFlow

1. Wytrenuj customowy model używając do tego `MLFlow`, zapisz go jako mlflow.pyfunc

```python
from typing import Dict
from datetime import datetime

import json
import mlflow

from my_custom_model import CustomModel


class CustomModelProd(CustomModel, mlflow.pyfunc.PythonModel):

    def __init__(self, settings: dict):
        CustomModel.__init__(self, **settings)

    def predict(self, context, model_input: Dict) -> Dict:
        """
        Method predicts from data.

        :param context: settings
        :param model_input: (Dict)
        :return: (Dict)
        """

        predictions = self.predict(model_input)
        return predictions
    
    
if __name__ == '__main__':
    dnow = str(datetime.now().timestamp())
    dnow = dnow.replace('.', '_')
    MODEL_PATH = f'temp_model_{dnow}'
    ARTIFACT_PATH = 'model_artifacts'
    mlflow.set_experiment('model')
    with mlflow.start_run(run_name='model-diagnostics') as run:
        # Load data
        training_data = ...

        # Fit model
        mdl = CustomModelProd()
        mdl.fit(training_data)

        try:
            mlflow.pyfunc.save_model(path=MODEL_PATH, python_model=mdl)
        except mlflow.exceptions.MlflowException as mlflowex:
            print(mlflowex)
            pass

        mlflow.end_run()

        # Load model
        loaded_model = mlflow.pyfunc.load_model(model_uri=MODEL_PATH)

        # Check model

        with open('test_data/sample.json', 'rt') as sample_data:
            for line in sample_data:
                with open('test_data/settings_list_wsknn.json', 'rt') as settings:
                    for setting in settings:
                        s_session = json.loads(line)
                        s_session['settings'] = json.loads(setting)
                        prediction = mdl.predict(None, model_input=s_session)
                        print(prediction)

```

2. Stwórz lokalny kontener do testów.

```shell
mlflow sagemaker build-and-push-container --no-push
```

3. Przeprowadź lokalny test wytrenowanego modelu.

```shell
mlflow sagemaker run-local -p 8888 -m [katalog z modelem]
```

Kiedy serwer wystartuje uruchom kod testowy, na przykład:

```python
import json
import requests


if __name__ == '__main__':
    PORT = 8888
    endpoint = "http://localhost:{}/invocations".format(PORT)
    HEADERS = {
        "Content-type": "application/json"
    }
    # Load data
    with open('test_data/sample.json', 'rt') as sample_data:
        for line in sample_data:
            s_session = json.loads(line)
            inp_data = dict(model_input=s_session)
            print(inp_data)
            prediction = requests.post(endpoint,
                                       json=inp_data,
                                       headers=HEADERS)
            print(prediction.text)
            break

```

4. Jeśli wszystko działa poprawnie model będzie deployowany na SageMaker. Przygotuj rolę która ma dostępy do SageMaker, S3 i ECR. Uzupełnij pliki `.aws/config` i `.aws/credentials`.
5. Zbuduj i pchnij kontener z modelem do ECR.

```shell
mlflow sagemaker build-and-push-container --build --push -c [nazwa-obrazu]
```

6. Stwórz bucket na S3 na wytrenowany model.

7. Wystaw model przy pomocy MLFlow:

```shell
mlflow sagemaker deploy -a [nazwa-endpointa] -m [mlflow run name] \
       -e arn:aws:iam::[rola-aws-z-odpowiednimi-dostepami] \
       -i [adres-ecr] \
       --bucket [nazwa-bucketa-na-s3] \
       --region-name [region-deplymentu] \
       --instance-type [rodzaj-modelu] \
       --instance-count [liczba-instancji] \
       --flavor python_function \
       --mode replace
```

8. Przetestuj wystawiony model

```python
import boto3
import json


endpoint = 'nazwa-endpointa-z-parametru-a-sagemaker-deploy'
client = boto3.client('sagemaker-runtime')
test_data = json.dumps({
    {
        "columns":["col1"],
        "data":[[12.8, 0.029, 0.48]]
    }
})

response = client.invoke_endpoint(
    EndpointName=endpoint,
    ContentType='application/json; format=pandas-split',
    Body=test_data)

print(str(json.loads(response['Body'].read())))
```