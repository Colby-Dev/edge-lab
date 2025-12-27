from pydantic import BaseModel
from typing import List, Dict

class ParlayLeg(BaseModel):
    label: str
    probability: float 
    odds_decimal: float

class ParlayRequest(BaseModel):
    legs: List[ParlayLeg]

class SaveParlayRequest(BaseModel):
    legs: List[Dict]
    total_probability: float
    total_odds: float
    expected_value: float
    risk_adjusted_return: float

