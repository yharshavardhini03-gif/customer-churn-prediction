"""
visualization.py – Plotly chart builders for the Streamlit app.
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


BRAND_COLORS = {
    "primary": "#6C63FF",
    "danger": "#e74c3c",
    "warning": "#f39c12",
    "success": "#2ecc71",
    "bg": "#0E1117",
    "card": "#1A1F2C",
    "text": "#FAFAFA",
}


def plot_feature_importance(model, feature_names: list) -> go.Figure:
    """Horizontal bar chart of feature importances from a tree-based model."""
    importances = model.feature_importances_
    idx = np.argsort(importances)
    fig = go.Figure(
        go.Bar(
            x=importances[idx],
            y=[feature_names[i] for i in idx],
            orientation="h",
            marker=dict(
                color=importances[idx],
                colorscale="Purples",
                showscale=False,
            ),
            text=[f"{v:.3f}" for v in importances[idx]],
            textposition="outside",
        )
    )
    fig.update_layout(
        title="Feature Importance",
        xaxis_title="Importance Score",
        yaxis_title="",
        plot_bgcolor=BRAND_COLORS["card"],
        paper_bgcolor=BRAND_COLORS["card"],
        font=dict(color=BRAND_COLORS["text"], size=13),
        height=380,
        margin=dict(l=10, r=40, t=50, b=10),
    )
    return fig


def plot_churn_gauge(prob: float) -> go.Figure:
    """Gauge chart showing churn probability."""
    color = (
        BRAND_COLORS["danger"] if prob >= 0.75
        else BRAND_COLORS["warning"] if prob >= 0.45
        else BRAND_COLORS["success"]
    )
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=round(prob * 100, 1),
            delta={"reference": 50, "valueformat": ".1f"},
            number={"suffix": "%", "font": {"size": 40, "color": color}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "white"},
                "bar": {"color": color, "thickness": 0.25},
                "bgcolor": BRAND_COLORS["card"],
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 45], "color": "#1e3a2f"},
                    {"range": [45, 75], "color": "#3b2e0f"},
                    {"range": [75, 100], "color": "#3b1010"},
                ],
                "threshold": {
                    "line": {"color": color, "width": 4},
                    "thickness": 0.75,
                    "value": prob * 100,
                },
            },
            title={"text": "Churn Probability", "font": {"size": 16}},
        )
    )
    fig.update_layout(
        paper_bgcolor=BRAND_COLORS["card"],
        font=dict(color="white"),
        height=280,
        margin=dict(l=20, r=20, t=40, b=10),
    )
    return fig


def plot_shap_bar(shap_values, feature_names: list, feature_row) -> go.Figure:
    """Horizontal bar chart of SHAP values for a single prediction."""
    vals = shap_values[0]
    colors = [BRAND_COLORS["danger"] if v > 0 else BRAND_COLORS["success"] for v in vals]
    idx = np.argsort(np.abs(vals))
    fig = go.Figure(
        go.Bar(
            x=vals[idx],
            y=[feature_names[i] for i in idx],
            orientation="h",
            marker_color=[colors[i] for i in idx],
            text=[f"{vals[i]:+.3f}" for i in idx],
            textposition="outside",
        )
    )
    fig.update_layout(
        title="SHAP – Explainability (red = pushes toward churn)",
        xaxis_title="SHAP Value",
        plot_bgcolor=BRAND_COLORS["card"],
        paper_bgcolor=BRAND_COLORS["card"],
        font=dict(color=BRAND_COLORS["text"], size=13),
        height=380,
        margin=dict(l=10, r=60, t=50, b=10),
    )
    return fig


def plot_batch_churn_distribution(df: pd.DataFrame) -> go.Figure:
    """Pie chart of churn vs non-churn for batch predictions."""
    counts = df["Churn_Prediction"].value_counts()
    labels = ["Will Churn" if c == 1 else "Will Stay" for c in counts.index]
    colors = [BRAND_COLORS["danger"] if c == 1 else BRAND_COLORS["success"] for c in counts.index]
    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=counts.values,
            hole=0.5,
            marker=dict(colors=colors),
        )
    )
    fig.update_layout(
        title="Batch Prediction Distribution",
        paper_bgcolor=BRAND_COLORS["card"],
        font=dict(color=BRAND_COLORS["text"]),
        height=300,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


def plot_analytics_histogram(df: pd.DataFrame, col: str, title: str) -> go.Figure:
    fig = px.histogram(
        df, x=col, color="Churn",
        barmode="overlay",
        title=title,
        color_discrete_map={0: BRAND_COLORS["success"], 1: BRAND_COLORS["danger"]},
        opacity=0.75,
    )
    fig.update_layout(
        plot_bgcolor=BRAND_COLORS["card"],
        paper_bgcolor=BRAND_COLORS["card"],
        font=dict(color=BRAND_COLORS["text"]),
        height=300,
        legend_title="Churn",
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig
