import json
import os

from dotenv import load_dotenv
from fastapi.testclient import TestClient

from vps.api import app

client = TestClient(app)
load_dotenv('../.env')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')


def test_post_conn():
    content = json.dumps({
        'ds': [101, -66.4, 3, 1]
    })
    response = client.post("/predict",
                           content=content,
                           headers={"CustomAccessToken": ACCESS_TOKEN})
    print(response)
    assert response.status_code == 201
