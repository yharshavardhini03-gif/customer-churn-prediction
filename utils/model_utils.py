"""
model_utils.py – Model loading, saving, and prediction helpers.
"""
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "churn_model.pkl"


def load_model():
    """Load the trained model from disk."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. Please run train.py first."
        )
    return joblib.load(MODEL_PATH)


def predict(model, X: pd.DataFrame):
    """Return (label, probability) for the given feature DataFrame."""
    prob = model.predict_proba(X)[0][1]
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
