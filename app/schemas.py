from pydantic import BaseModel
from typing import List

class ScoreRequest(BaseModel):
    txn_id: str
    card_id: str
    amount: float
    currency: str
    merchant_id: str
    mcc: str
    device_id: str
    ip: str
    ts: str  # ISO timestamp string for now; we can tighten later

class ScoreResponse(BaseModel):
    decision: str            # "allow" | "step_up" | "deny"
    score: float             # risk score 0.0 - 1.0
    reasons: List[str]       # why we made that decision
    model_version: str
    latency_ms: int
