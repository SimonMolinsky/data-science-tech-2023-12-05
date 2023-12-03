from typing import Dict
from pydantic import BaseModel


class ResponseModel(BaseModel):
    anomalies: Dict
