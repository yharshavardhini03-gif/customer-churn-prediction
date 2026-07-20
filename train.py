"""
train.py – Train a Random Forest / XGBoost ensemble and save to models/churn_model.pkl
Run:  python train.py
"""
import sys
import os
from pathlib import Path

# Ensure the project root is on the path when run from any directory
sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.metrics import (
    classification_report, roc_auc_score, confusion_matrix, ConfusionMatrixDisplay
)
from sklearn.preprocessing import StandardScaler

try:
    from xgboost import XGBClassifier
    XGB_AVAILABLE = True
except ImportError:
    XGB_AVAILABLE = False
    print("[WARN] xgboost not installed – using Random Forest only.")

from utils.preprocess import preprocess, FEATURE_COLS

# ── Paths ──────────────────────────────────────────────────────────────────
DATA_PATH  = Path(__file__).parent / "data" / "customer_churn.csv"
MODEL_PATH = Path(__file__).parent / "models" / "churn_model.pkl"

# ── Generate dataset if it doesn't exist ──────────────────────────────────
if not DATA_PATH.exists():
    print("[INFO] Dataset not found – generating synthetic data …")
    exec(open(Path(__file__).parent / "data" / "generate_data.py").read())
    import shutil
    shutil.move("customer_churn.csv", str(DATA_PATH))

# ── Load & preprocess ─────────────────────────────────────────────────────
df  = pd.read_csv(DATA_PATH)
X   = preprocess(df)
y   = df["Churn"]

print(f"[INFO] Dataset: {len(df)} rows | Churn rate: {y.mean()*100:.1f}%")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ── Build model ───────────────────────────────────────────────────────────
rf = RandomForestClassifier(
    n_estimators=300,
    max_depth=8,
    min_samples_leaf=5,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1,
)

if XGB_AVAILABLE:
    xgb = XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric="logloss",
        random_state=42,
        n_jobs=-1,
    )
    model = VotingClassifier(
        estimators=[("rf", rf), ("xgb", xgb)],
        voting="soft",
        weights=[1, 1.5],
    )
    print("[INFO] Training RF + XGBoost VotingClassifier …")
else:
    model = rf
    print("[INFO] Training RandomForestClassifier …")

model.fit(X_train, y_train)

# ── Evaluate ──────────────────────────────────────────────────────────────
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print("\n--- Classification Report ---")
print(classification_report(y_test, y_pred, target_names=["Stay", "Churn"]))
print(f"ROC-AUC : {roc_auc_score(y_test, y_prob):.4f}")

# Cross-validation
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(model, X, y, cv=cv, scoring="roc_auc", n_jobs=-1)
print(f"CV ROC-AUC : {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

# ── Save ──────────────────────────────────────────────────────────────────
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(model, MODEL_PATH)
print(f"\n[OK] Model saved -> {MODEL_PATH}")
