import logging
import os
import uvicorn

from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Depends
from fastapi.security import APIKeyHeader

from api_functions.run import predict
from api_functions.request import RequestModel
from api_functions.response import ResponseModel

load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_HEADER_NAME = os.getenv("ACCESS_TOKEN_HEADER_NAME")
MODEL_DIR = os.getenv("MODEL_DIR")

# Set logging
LOGGING_DIR = os.getenv("LOGGING_DIR")
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL")
LOGGING_FORMAT = os.getenv("LOGGING_FORMAT")


app = FastAPI(docs_url=None, redoc_url=None)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
api_key_header = APIKeyHeader(name=ACCESS_TOKEN_HEADER_NAME)


@app.post("/predict", response_model=ResponseModel, status_code=200)
async def detector(item: RequestModel, token: str = Depends(api_key_header)):
    logging.info("New request coming!")
    if token != ACCESS_TOKEN:
        return {"error": "Invalid Access Token"}
    else:
        # unpack and use model
        predictions = predict(model_path=os.getenv("MODEL_DIR"), data=item.ds)
        logging.info("Predictions made successfully!")
        return ResponseModel(anomalies=predictions)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
