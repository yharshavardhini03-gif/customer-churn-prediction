"""
model_utils.py – Lightweight model loading and prediction helpers.
"""
import json
import math
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "churn_model.json"
DEFAULT_MODEL = {
    "intercept": -2.2,
    "weights": {
        "Age": -0.012,
        "Tenure_Months": -0.025,
        "Purchase_Frequency": -0.018,
        "Total_Amount_Spent": -0.0012,
        "Avg_Order_Value": -0.001,
        "Days_Since_Last_Purchase": 0.008,
        "Membership": 0.22,
        "Support_Calls": 0.16,
    },
}


def load_model():
    """Load the lightweight model from disk, falling back to built-in defaults."""
    if MODEL_PATH.exists():
        with MODEL_PATH.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    return DEFAULT_MODEL


def predict(model, X):
    """Return (label, probability) for the given feature dictionary."""
    if isinstance(X, dict):
        features = X
    else:
        features = X[0] if isinstance(X, list) and X else {}

    intercept = float(model.get("intercept", DEFAULT_MODEL["intercept"]))
    weights = model.get("weights", DEFAULT_MODEL["weights"])
    score = intercept
    for key, weight in weights.items():
        value = features.get(key, 0)
        score += float(weight) * float(value)
    prob = 1 / (1 + math.exp(-score))
    label = int(prob >= 0.5)
    return label, float(prob)


def get_risk_level(prob: float) -> tuple[str, str]:
    """Map probability to human-readable risk level and colour hex."""
    if prob >= 0.75:
        return "High", "#e74c3c"
    elif prob >= 0.45:
        return "Medium", "#f39c12"
    else:
        return "Low", "#2ecc71"
