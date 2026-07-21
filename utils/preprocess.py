"""
preprocess.py – Lightweight feature engineering utilities for deployment.
"""

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


def encode_membership(value):
    """Encode membership tier as an ordinal integer."""
    return MEMBERSHIP_MAP.get(value, 0)


def preprocess(data, feature_cols=None):
    """Run a lightweight preprocessing pipeline on a row or a list of rows."""
    if feature_cols is None:
        feature_cols = FEATURE_COLS

    if isinstance(data, dict):
        row = {}
        for col in feature_cols:
            if col == 'Membership':
                row[col] = encode_membership(data.get(col, 'Bronze'))
            else:
                row[col] = float(data.get(col, 0))
        return row

    if isinstance(data, list):
        return [preprocess(item, feature_cols=feature_cols) for item in data]

    raise TypeError('Expected a dict or list of dicts')


def get_feature_input(
    age, tenure, purchase_freq, total_spent, avg_order_val, days_since, membership, support_calls
):
    """Build a single-row feature dictionary from user inputs."""
    data = {
        'Age': age,
        'Tenure_Months': tenure,
        'Purchase_Frequency': purchase_freq,
        'Total_Amount_Spent': total_spent,
        'Avg_Order_Value': avg_order_val,
        'Days_Since_Last_Purchase': days_since,
        'Membership': membership,
        'Support_Calls': support_calls,
    }
    return preprocess(data)
