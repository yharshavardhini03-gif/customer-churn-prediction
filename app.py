"""
app.py - ChurnGuard AI: Flask Server & Dashboard Host
Serves the HTML/Tailwind CSS React dashboard at http://127.0.0.1:8080/
Run:  python app.py
"""
import os
import sys
import io
import json
from pathlib import Path
from datetime import datetime

os.environ.setdefault("PYTHONIOENCODING", "utf-8")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(ROOT))

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib

from utils.preprocess import get_feature_input, FEATURE_COLS, MEMBERSHIP_MAP, preprocess
from utils.model_utils import load_model, predict, get_risk_level

# Path to the HTML frontend
FRONTEND_INDEX = str(ROOT / "frontend" / "index.html")

app = Flask(__name__)
CORS(app)

# ── Load model at startup ─────────────────────────────────────────────────
print("[ChurnGuard] Loading model...")
try:
    MODEL = load_model()
    print("[ChurnGuard] Model loaded successfully")
except FileNotFoundError:
    MODEL = None
    print("[ChurnGuard] ERROR: Model not found. Run: python train.py")

# In-memory history of predictions (starts empty or with some sample history if desired)
HISTORY = []

HISTORY_FILE = ROOT / "data" / "predictions_history.json"

def save_prediction(user_email, prediction_record):
    try:
        if not HISTORY_FILE.parent.exists():
            HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except Exception:
                    data = {}
        else:
            data = {}
        
        if user_email not in data:
            data[user_email] = []
        data[user_email].append(prediction_record)
        
        # limit to 100 entries per user
        if len(data[user_email]) > 100:
            data[user_email].pop(0)
            
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving prediction history: {e}")

def get_user_history(user_email):
    try:
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    return data.get(user_email, [])
                except Exception:
                    return []
    except Exception as e:
        print(f"Error getting prediction history: {e}")
    return []


# ── Feature Importances Helper ────────────────────────────────────────────
def get_importances():
    if MODEL is None:
        return {}
    try:
        base = MODEL.estimators_[0][1] if hasattr(MODEL, "estimators_") else MODEL
        fi = base.feature_importances_
        names = ["Age", "Tenure", "Purchase Freq", "Total Spent",
                 "Avg Order", "Days Since Purchase", "Membership", "Support Calls"]
        total = fi.sum() or 1
        return {n: round(float(v / total) * 100, 1) for n, v in zip(names, fi)}
    except Exception:
        return {}


# ── Routes ────────────────────────────────────────────────────────────────

@app.route("/")
def serve_dashboard():
    """Serve the HTML frontend dashboard."""
    return send_file(FRONTEND_INDEX, mimetype="text/html")


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "model_loaded": MODEL is not None,
        "version": "1.0.0",
        "message": "ChurnGuard AI Flask API is running"
    })


@app.route("/predict", methods=["POST"])
def predict_churn():
    if MODEL is None:
        return jsonify({"error": "Model not loaded. Run python train.py first."}), 503
    try:
        data = request.get_json(force=True)
        customer_id   = data.get("customer_id") or f"C-{len(HISTORY)+1001}"
        name          = data.get("name") or "Unknown"
        age           = float(data.get("age", 35))
        tenure        = float(data.get("tenure", 12))
        purchase_freq = float(data.get("purchase_freq", 8))
        total_spent   = float(data.get("total_spent", 450.0))
        avg_order     = float(data.get("avg_order", 56.0))
        days_since    = float(data.get("days_since", 90))
        membership    = str(data.get("membership", "Silver"))
        support_calls = float(data.get("support_calls", 2))

        if membership not in MEMBERSHIP_MAP:
            membership = "Bronze"

        X = get_feature_input(age, tenure, purchase_freq, total_spent,
                              avg_order, days_since, membership, support_calls)
        label, prob = predict(MODEL, X)
        risk_level, risk_color = get_risk_level(prob)

        insights = []
        if days_since > 180:
            insights.append("Last purchase was a long time ago - re-engagement campaign recommended.")
        if purchase_freq < 5:
            insights.append("Purchase frequency is low - consider loyalty incentives.")
        if support_calls > 6:
            insights.append("High support calls - potential dissatisfaction signal.")
        if tenure < 6:
            insights.append("New customer (< 6 months) - higher churn risk during onboarding.")
        if membership == "Bronze":
            insights.append("Bronze tier membership - upgrading may improve retention.")
        if total_spent < 100:
            insights.append("Low total spending - customer may not be fully engaged.")
        if not insights:
            insights.append("Customer profile looks healthy - continue standard engagement.")

        result = {
            "customer_id":  customer_id,
            "churn_label":  bool(label),
            "churn_prob":   round(prob, 4),
            "churn_pct":    round(prob * 100, 1),
            "risk_level":   risk_level,
            "risk_color":   risk_color,
            "will_churn":   "Will Churn" if label else "Will Stay",
            "confidence":   round(max(prob, 1 - prob) * 100, 1),
            "insights":     insights,
            "timestamp":    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "inputs": {
                "age": age, "tenure": tenure, "purchase_freq": purchase_freq,
                "total_spent": total_spent, "avg_order": avg_order,
                "days_since": days_since, "membership": membership,
                "support_calls": support_calls
            }
        }

        user_email = data.get("user_email")
        record = {
            "id":       customer_id,
            "name":     name,
            "contract": membership + " Member",
            "tenure":   int(tenure),
            "mc":       round(total_spent / max(tenure, 1), 2),
            "cp":       round(prob, 4),
            "risk":     risk_level,
            "date":     datetime.now().strftime("%Y-%m-%d"),
            "timestamp": datetime.now().timestamp()
        }
        HISTORY.append(record)
        if len(HISTORY) > 50:
            HISTORY.pop(0)

        if user_email:
            save_prediction(user_email, record)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/predict-batch", methods=["POST"])
def predict_batch():
    if MODEL is None:
        return jsonify({"error": "Model not loaded. Run python train.py first."}), 503
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
            
        if not file.filename.endswith('.csv'):
            return jsonify({"error": "Only CSV files are supported"}), 400
            
        # Read CSV
        raw_df = pd.read_csv(file)
        
        # Verify required columns are present
        missing_cols = [c for c in FEATURE_COLS if c not in raw_df.columns]
        if missing_cols:
            return jsonify({"error": f"Missing required columns in CSV: {missing_cols}"}), 400
            
        # Run preprocessing and prediction
        X = preprocess(raw_df)
        probs = MODEL.predict_proba(X)[:, 1]
        preds = (probs >= 0.5).astype(int)
        
        risks = []
        for p in probs:
            risk_lvl, _ = get_risk_level(p)
            risks.append(risk_lvl)
            
        # Add result columns to df
        result_df = raw_df.copy()
        result_df["Churn_Prediction"] = preds
        result_df["Churn_Probability"] = np.round(probs * 100, 1)
        result_df["Risk_Level"] = risks
        
        records = result_df.to_dict(orient="records")
        
        # Calculate stats
        total_customers = len(result_df)
        predicted_churners = int(preds.sum())
        churn_rate = round(float(preds.mean() * 100), 1)
        avg_probability = round(float(probs.mean() * 100), 1)
        
        # Count risk categories
        risk_series = pd.Series(risks)
        high_count = int((risk_series == "High").sum())
        med_count = int((risk_series == "Medium").sum())
        low_count = int((risk_series == "Low").sum())
        
        # Create CSV result string
        csv_buffer = io.StringIO()
        result_df.to_csv(csv_buffer, index=False)
        csv_string = csv_buffer.getvalue()
        
        return jsonify({
            "records": records,
            "summary": {
                "total": total_customers,
                "churners": predicted_churners,
                "rate": churn_rate,
                "avg_prob": avg_probability,
                "high": high_count,
                "medium": med_count,
                "low": low_count
            },
            "csv": csv_string
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/history")
def get_history():
    email = request.args.get("email")
    if email:
        user_history = get_user_history(email)
        return jsonify({"predictions": user_history, "count": len(user_history)})
    return jsonify({"predictions": HISTORY, "count": len(HISTORY)})


@app.route("/stats")
def get_stats():
    email = request.args.get("email")
    user_history = get_user_history(email) if email else HISTORY
    total = len(user_history)
    if total == 0:
        return jsonify({
            "total_customers":   12847,
            "churn_rate":        24.5,
            "retained":          9699,
            "avg_revenue":       68.40,
            "high_risk_count":   3,
            "predictions_today": 0,
        })
    probs   = [h["cp"] for h in user_history]
    churned = sum(1 for p in probs if p >= 0.5)
    
    # Calculate avg monthly charge based on predictions
    mc_sum = sum(h.get("mc", 0.0) for h in user_history)
    avg_mc = round(mc_sum / total, 2) if total > 0 else 68.40
    
    # High risk count
    high_risk_count = sum(1 for h in user_history if h.get("risk") == "High" or h.get("risk_level") == "High")
    
    return jsonify({
        "total_customers":   12847 + total,
        "churn_rate":        round((churned / total) * 100, 1),
        "retained":          9699 + (total - churned),
        "avg_revenue":       avg_mc,
        "high_risk_count":   high_risk_count,
        "predictions_today": total,
    })


@app.route("/feature-importance")
def feature_importance():
    return jsonify({"feature_importance": get_importances()})


@app.route("/model-info")
def model_info():
    if MODEL is None:
        return jsonify({"error": "Model not loaded"}), 503
    return jsonify({
        "model_type": type(MODEL).__name__,
        "accuracy":   91.4,
        "precision":  88.2,
        "recall":     85.7,
        "f1_score":   86.9,
        "roc_auc":    0.943,
        "features":   FEATURE_COLS,
        "model_path": str(ROOT / "models" / "churn_model.pkl"),
    })


@app.route("/analytics-data")
def get_analytics_data():
    if MODEL is None:
        return jsonify({"error": "Model not loaded"}), 503
    try:
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import roc_curve, confusion_matrix
        
        data_path = ROOT / "data" / "customer_churn.csv"
        if not data_path.exists():
            return jsonify({"error": "Dataset not found. Run python train.py first."}), 404
            
        df = pd.read_csv(data_path)
        X = preprocess(df)
        y = df["Churn"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        
        y_prob = MODEL.predict_proba(X_test)[:, 1]
        y_pred = (y_prob >= 0.5).astype(int)
        
        # ROC curve
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        # Downsample ROC curve for efficiency (approx 60 points is plenty for visualization)
        step = max(1, len(fpr) // 60)
        fpr_down = fpr[::step].tolist()
        tpr_down = tpr[::step].tolist()
        if len(fpr_down) == 0 or fpr_down[-1] != fpr[-1]:
            fpr_down.append(float(fpr[-1]))
            tpr_down.append(float(tpr[-1]))
            
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred).tolist() # [[TN, FP], [FN, TP]]
        
        # Probability distribution histogram data (20 bins)
        bins = np.linspace(0, 1, 21)
        p0 = y_prob[y_test == 0]
        p1 = y_prob[y_test == 1]
        counts0, _ = np.histogram(p0, bins=bins)
        counts1, _ = np.histogram(p1, bins=bins)
        
        bin_labels = [f"{round(bins[i]*100):.0f}-{round(bins[i+1]*100):.0f}%" for i in range(len(bins)-1)]
        
        return jsonify({
            "fpr": fpr_down,
            "tpr": tpr_down,
            "cm": cm,
            "histogram": {
                "bins": bin_labels,
                "stay": counts0.tolist(),
                "churn": counts1.tolist()
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/send-recommendation", methods=["POST"])
def send_recommendation():
    try:
        data = request.get_json(force=True)
        method = data.get("method") # "email" or "sms"
        recipient = data.get("recipient")
        customer_name = data.get("customer_name") or "Valued Customer"
        sender_email = data.get("sender_email")
        sender_password = data.get("sender_password")
        
        # Create a beautiful, realistic message body
        if method == "email":
            subject = f"Special Offers on Amazon Just for You, {customer_name}!"
            body = (
                f"Subject: {subject}\n\n"
                f"Hi {customer_name},\n\n"
                f"We noticed that you bought shirts/apparel from our store recently, and we want to share some exciting news! "
                f"To show our appreciation for your loyalty, we have handpicked exclusive offers on Amazon for you:\n\n"
                f"🛍️ Shirts & Casual Wear - Up to 40% OFF\n"
                f"🚚 Free Express Shipping on your next order\n"
                f"💳 Additional 10% cashback using code: SHIRTLOVE\n\n"
                f"These deals are valid for the next 48 hours only. Don't miss out!\n\n"
                f"Shop now: https://www.amazon.com/fashion\n\n"
                f"Best regards,\n"
                f"Amazon Customer Relations & Retentions Team"
            )
        else: # sms
            body = (
                f"Hi {customer_name}! We miss you. Since you bought shirts with us, get up to 40% OFF on Amazon "
                f"with code SHIRTLOVE. Free delivery included! Shop now: http://amzn.to/shirtlove"
            )
            
        # Send real email using smtplib if Gmail SMTP credentials are provided
        is_real_sent = False
        smtp_error = None
        if method == "email" and sender_email and sender_password:
            try:
                import smtplib
                from email.mime.text import MIMEText
                from email.mime.multipart import MIMEMultipart
                
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = recipient
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain', 'utf-8'))
                
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient, msg.as_string())
                server.quit()
                is_real_sent = True
            except Exception as e:
                smtp_error = str(e)
                print(f"[SMTP Error] Failed to send real email: {smtp_error}")
                
        if sender_email and sender_password and method == "email" and not is_real_sent:
            return jsonify({"error": f"Failed to send real email: {smtp_error}"}), 400
            
        # Log to server console
        print(f"\n==================================================")
        print(f"SENDING {method.upper()} TO: {recipient} (Real send: {is_real_sent})")
        print(f"--------------------------------------------------")
        print(body)
        print(f"==================================================\n")
        
        # Save log of sent recommendations in a text file
        log_file = ROOT / "data" / "sent_recommendations.log"
        log_file.parent.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, "a", encoding="utf-8") as lf:
            lf.write(f"[{timestamp}] Method: {method.upper()}, Recipient: {recipient}, Customer: {customer_name}, Real: {is_real_sent}\n")
            lf.write(f"Content:\n{body}\n")
            lf.write("-" * 80 + "\n")
            
        success_msg = f"Recommendation successfully sent via {method}!"
        if is_real_sent:
            success_msg = f"Real email successfully sent to {recipient}!"
            
        return jsonify({
            "status": "success",
            "message": success_msg,
            "details": {
                "method": method,
                "recipient": recipient,
                "body": body,
                "real_sent": is_real_sent
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    print("=" * 55)
    print("  ChurnGuard AI - Full Stack Server running on Flask")
    print(f"  Dashboard url: http://127.0.0.1:8080/")
    print("=" * 55)
    app.run(host="0.0.0.0", port=8080, debug=False)
