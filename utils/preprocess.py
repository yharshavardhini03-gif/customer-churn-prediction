"""
preprocess.py – Feature engineering & data preparation utilities.
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder


FEATURE_COLS = [
    'Age',
    'Tenure_Months',
    'Purchase_Frequency',
    'Total_Amount_Spent',
    'Avg_Order_Value',
    'Days_Since_Last_Purchase',
    'Membership',
    'Support_Calls',
]

MEMBERSHIP_MAP = {'Bronze': 0, 'Silver': 1, 'Gold': 2}


def encode_membership(df: pd.DataFrame) -> pd.DataFrame:
    """Encode membership tier as ordinal integer."""
    df = df.copy()
    df['Membership'] = df['Membership'].map(MEMBERSHIP_MAP)
    return df


def preprocess(df: pd.DataFrame, feature_cols=None) -> pd.DataFrame:
    """Run full preprocessing pipeline."""
    if feature_cols is None:
        feature_cols = FEATURE_COLS
    df = df[feature_cols].copy()
    df = encode_membership(df)
    return df


def get_feature_input(
    age, tenure, purchase_freq, total_spent, avg_order_val, days_since, membership, support_calls
) -> pd.DataFrame:
    """Build a single-row DataFrame from user inputs."""
    data = {
        'Age': [age],
        'Tenure_Months': [tenure],
        'Purchase_Frequency': [purchase_freq],
        'Total_Amount_Spent': [total_spent],
        'Avg_Order_Value': [avg_order_val],
        'Days_Since_Last_Purchase': [days_since],
        'Membership': [membership],
        'Support_Calls': [support_calls],
    }
    df = pd.DataFrame(data)
    return preprocess(df)
