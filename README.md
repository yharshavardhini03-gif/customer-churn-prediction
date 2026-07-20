# Customer Churn Prediction 📊

> An AI-powered customer churn prediction dashboard built with **Flask**, **HTML/Tailwind CSS**, **Scikit-learn**, and **XGBoost**.

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Train the model (auto-generates synthetic dataset)
python train.py

# 3. Launch the Flask server and frontend dashboard
python app.py
```

Then open **http://localhost:8080** in your browser.

---

## 📂 Project Structure

```
customer-churn-prediction/
│
├── app.py                   # Main Flask server (serves frontend & prediction endpoints)
├── train.py                 # ML training pipeline (RF + XGBoost ensemble)
├── requirements.txt
├── README.md
│
├── data/
│   ├── generate_data.py     # Synthetic dataset generator (2,000 customers)
│   └── customer_churn.csv   # Generated training data
│
├── models/
│   └── churn_model.pkl      # Trained model (auto-created by train.py)
│
├── utils/
│   ├── preprocess.py        # Feature engineering helpers
│   ├── model_utils.py       # Model load / predict / risk-level helpers
│   └── visualization.py     # Plotly chart builders (kept for offline use)
│
└── frontend/
    └── index.html           # React + Tailwind CSS dashboard (served by app.py)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5 · Tailwind CSS · React (CDN) · Chart.js |
| Backend | Python · Flask · Flask-CORS |
| ML | Scikit-learn · XGBoost |
| Explainability | SHAP |
| Data | Pandas · NumPy |
| Storage | Joblib |

---

## ✨ Features

- 🔮 **Single Prediction** — enter customer details and get an instant churn probability with a gauge chart
- 📂 **Batch Prediction** — upload a CSV of customers, score all of them in real-time, view KPIs / distributions, and download the results CSV
- 📈 **Model Performance & Analytics** — interactive ROC curve, confusion matrix grid, probability histogram, and feature importances
- 🕑 **Prediction History** — log of all predictions made in the session
- 💡 **AI Insights** — actionable text recommendations for each customer based on features
- 🧑‍💼 **Customer Search** — search and filter customer history by risk levels

---

## 📊 Model Details

- **Algorithm**: VotingClassifier (Random Forest + XGBoost, soft voting)
- **Features**: Age, Tenure, Purchase Frequency, Total Spent, Avg Order Value, Days Since Last Purchase, Membership, Support Calls
- **Evaluation**: 5-fold stratified cross-validation (ROC-AUC)
- **Training data**: 2,000 synthetically generated customers

---

## 📜 License

MIT — free to use, modify, and distribute.
