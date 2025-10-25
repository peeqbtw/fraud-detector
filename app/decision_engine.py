import time
from random import random
from app.schemas import ScoreRequest, ScoreResponse

# Adaptive friction thresholds (based on hackathon framing):
# 0.00–0.30  -> PASS (low friction)
# 0.31–0.70  -> CHALLENGE (micro-friction like Face ID / one-tap confirm)
# 0.71–1.00  -> BLOCK (deny or manual review)
T_LOW_MAX = 0.30
T_MEDIUM_MAX = 0.70

MODEL_VERSION = "v1.0-dev"

def classify_risk(score: float) -> dict:
    """
    Convert numeric fraud score into a tier, a color, and what the user experiences.
    """
    if score <= T_LOW_MAX:
        return {
            "tier": "LOW",
            "color": "green",
            "user_experience": "Approved instantly. No extra steps.",
            "auth_action": "PASS"
        }
    elif score <= T_MEDIUM_MAX:
        return {
            "tier": "MEDIUM",
            "color": "yellow",
            "user_experience": "Quick Face ID / tap to confirm. Minimal friction.",
            "auth_action": "CHALLENGE"
        }
    else:
        return {
            "tier": "HIGH",
            "color": "red",
            "user_experience": "Transaction blocked instantly to protect the account.",
            "auth_action": "BLOCK"
        }

def decide_transaction(req: ScoreRequest) -> ScoreResponse:
    """
    This powers /score. Still mock-scoring with random(), but structured like
    a real-time AI model returning a fraud probability in [0,1].
    """
    start = time.time()

    raw_score = random()  # placeholder for ML risk score
    risk_info = classify_risk(raw_score)

    if risk_info["auth_action"] == "PASS":
        decision = "allow"
        reasons = ["low_risk_baseline"]
    elif risk_info["auth_action"] == "CHALLENGE":
        decision = "step_up"
        reasons = ["behavior_change_detected"]
    else:
        decision = "deny"
        reasons = ["high_risk_pattern"]

    latency_ms = int((time.time() - start) * 1000)

    return ScoreResponse(
        decision=decision,
        score=round(raw_score, 2),
        reasons=reasons,
        model_version=MODEL_VERSION,
        latency_ms=latency_ms
    )

def simulate_impossible_travel():
    """
    Scripted high-risk 'impossible travel' scenario for the live demo.

    Narrative:
    - Card used in New York.
    - 5 minutes later, an attempt from Madrid on a different device.
    - Physically impossible. We treat it as account takeover.

    This single response is designed to satisfy ALL hackathon deliverables:
      - Technical Architecture: AI score & decision logic (BLOCK).
      - Privacy Framework: anonymized behavioral signals, encrypted at rest.
      - Risk-Tiered Journeys: high-risk -> instant block (no OTP).
      - Collaboration Blueprint: we share a fraud signature, not PII.
      - Customer Education Plan: clear reassurance message to the user.
    """

    score = 0.91  # very high risk -> BLOCK
    risk_info = classify_risk(score)

    # 1. Customer-facing education / reassurance
    customer_message = (
        "We blocked a suspicious charge from Madrid that happened 5 minutes "
        "after a purchase in New York. No money left your account. Your card is safe."
    )

    # 2. Fraud operations / investigator view
    ops_view = (
        "Impossible travel detected: new device + new location (ES) within 5 minutes "
        "of prior txn in US. Pattern consistent with account takeover."
    )

    # 3. Privacy + compliance posture
    privacy_info = (
        "No raw card number or PII is stored. Only encrypted behavioral signals "
        "(device fingerprint, geo anomaly) are logged for model defense. "
        "This supports GDPR/CCPA obligations."
    )

    # 4. Collaboration / intelligence sharing
    collaboration_note = (
        "This fraud signature (impossible_travel + device_mismatch) is shared "
        "with partner institutions as an anonymized threat signal to improve "
        "collective defense without exposing personal data."
    )

    return {
        # Core risk/decision
        "score": round(score, 2),
        "decision": "deny",                    # BLOCK
        "auth_action": risk_info["auth_action"],
        "risk_tier": risk_info["tier"],        # HIGH
        "risk_color": risk_info["color"],      # red
        "user_experience": risk_info["user_experience"],

        # Customer Education Plan
        "customer_message": customer_message,

        # Fraud Ops / Compliance view
        "ops_view": ops_view,

        # Privacy Framework
        "privacy_info": privacy_info,

        # Collaboration Blueprint
        "collaboration_note": collaboration_note,

        # telemetry
        "model_version": MODEL_VERSION,
        "latency_ms": 2
    }

def explain_risk(score: float):
    """
    Helper: translate any numeric score to tier/color and UX language.
    """
    risk_info = classify_risk(score)
    return {
        "risk_tier": risk_info["tier"],
        "risk_color": risk_info["color"],
        "user_experience": risk_info["user_experience"],
        "auth_action": risk_info["auth_action"]
    }
