from typing import List
from pydantic import BaseModel


class RequestModel(BaseModel):
    ds: List
