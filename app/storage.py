from typing import Dict

# In-memory store (resets when app restarts)
transaction_feedback: Dict[str, str] = {}   # txn_id -> "fraud"/"legit"

# Running counters
metrics = {
    "fraud_count": 0,
    "legit_count": 0,
    "total": 0
}

def add_feedback(txn_id: str, label: str) -> None:
    """Store feedback and update metrics counters."""
    transaction_feedback[txn_id] = label
    metrics["total"] += 1
    if label == "fraud":
        metrics["fraud_count"] += 1
    elif label == "legit":
        metrics["legit_count"] += 1

def get_metrics() -> Dict[str, float]:
    """Return current metrics plus simple fraud ratio."""
    total = metrics["total"] or 1
    fraud_ratio = metrics["fraud_count"] / total
    legit_ratio = metrics["legit_count"] / total
    return {
        "fraud_count": metrics["fraud_count"],
        "legit_count": metrics["legit_count"],
        "total_feedback": metrics["total"],
        "fraud_ratio": round(fraud_ratio, 3),
        "legit_ratio": round(legit_ratio, 3)
    }
