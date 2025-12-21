from pydantic import BaseModel
from typing import List

class ParlayLeg(BaseModel):
    label: str
    probability: float 
    odds_decimal: float

class ParlayRequest(BaseModel):
    legs: List[ParlayLeg]