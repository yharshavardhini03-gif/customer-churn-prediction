"""
Script to generate synthetic customer churn dataset.
Run this once to create customer_churn.csv
"""
import pandas as pd
import numpy as np

np.random.seed(42)
n = 2000

membership = np.random.choice(['Bronze', 'Silver', 'Gold'], size=n, p=[0.5, 0.35, 0.15])
age = np.random.randint(18, 75, size=n)
tenure = np.random.randint(1, 60, size=n)
support_calls = np.random.randint(0, 15, size=n)
purchase_frequency = np.random.randint(1, 30, size=n)
days_since_last = np.random.randint(1, 365, size=n)
total_spent = np.round(np.random.exponential(scale=500, size=n) + 50, 2)
avg_order_value = np.round(total_spent / purchase_frequency, 2)

# Churn logic
churn_prob = (
    0.3 * (support_calls > 7).astype(int) +
    0.25 * (days_since_last > 200).astype(int) +
    0.2 * (tenure < 6).astype(int) +
    0.15 * (purchase_frequency < 5).astype(int) +
    0.1 * (np.array([m == 'Bronze' for m in membership])).astype(int)
)
churn_prob = np.clip(churn_prob + np.random.normal(0, 0.1, n), 0, 1)
churn = (churn_prob > 0.35).astype(int)

df = pd.DataFrame({
    'Age': age,
    'Tenure_Months': tenure,
    'Purchase_Frequency': purchase_frequency,
    'Total_Amount_Spent': total_spent,
    'Avg_Order_Value': avg_order_value,
    'Days_Since_Last_Purchase': days_since_last,
    'Membership': membership,
    'Support_Calls': support_calls,
    'Churn': churn
})

df.to_csv('customer_churn.csv', index=False)
print(f"Dataset created: {len(df)} rows, Churn rate: {df['Churn'].mean()*100:.1f}%")
