from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.schemas import ScoreRequest, ScoreResponse
from app.decision_engine import decide_transaction, explain_risk, simulate_impossible_travel
from app.demo_page import get_demo_html  # we'll update demo_page next

app = FastAPI(
    title="Adaptive Fraud Defense",
    description="Real-time fraud scoring with adaptive friction, privacy protection, and collaborative intelligence sharing.",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    return {"status": "online"}

@app.post("/score", response_model=ScoreResponse)
def score_txn(payload: ScoreRequest):
    """
    General scoring route. Not used in final 30s story, but still works.
    """
    decision_payload = decide_transaction(payload)
    return decision_payload

@app.get("/risk_tier")
def get_risk_tier(score: float):
    """
    Helper to translate a numeric score into LOW/MEDIUM/HIGH and required action.
    """
    return explain_risk(score)

@app.get("/scenario_impossible_travel")
def scenario_impossible_travel():
    """
    High-risk scenario:
    - Location jump NY -> Madrid in 5 minutes.
    - High risk score => BLOCK.
    - Includes customer messaging, ops view, privacy story,
      and collaboration story.
    """
    return simulate_impossible_travel()

@app.get("/demo", response_class=HTMLResponse)
def demo_ui():
    """
    We'll update this next:
    A single-button dashboard that calls /scenario_impossible_travel
    and renders all the sections we care about for judging.
    """
    return get_demo_html()
