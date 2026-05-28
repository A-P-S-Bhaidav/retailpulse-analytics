"""Forecast Dashboard -- Prophet, LSTM, and Ensemble predictions."""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")


def load_data():
    prophet_ready = pd.read_csv(os.path.join(DATA_DIR, "prophet_ready.csv"), parse_dates=["ds"])
    forecast_30d = pd.read_csv(os.path.join(DATA_DIR, "prophet_forecast_30d.csv"), parse_dates=["ds"])
    forecast_full = pd.read_csv(os.path.join(DATA_DIR, "prophet_forecast_full.csv"), parse_dates=["ds"])
    lstm_pred = pd.read_csv(os.path.join(DATA_DIR, "lstm_predictions.csv"), parse_dates=["ds"])
    ensemble = pd.read_csv(os.path.join(DATA_DIR, "ensemble_predictions.csv"), parse_dates=["ds"])
    comparison = pd.read_csv(os.path.join(DATA_DIR, "model_comparison.csv"))
    return prophet_ready, forecast_30d, forecast_full, lstm_pred, ensemble, comparison


def render():
    st.header("Forecast Dashboard")
    prophet_ready, forecast_30d, forecast_full, lstm_pred, ensemble, comparison = load_data()

    # KPIs
    avg_forecast = forecast_30d["yhat"].mean()
    max_forecast = forecast_30d["yhat"].max()
    best_model = comparison.iloc[0]["Model"] if len(comparison) > 0 else "N/A"
    best_mape = comparison.iloc[0]["MAPE (%)"] if len(comparison) > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("30-Day Avg Forecast", f"£{avg_forecast:,.0f}")
    col2.metric("30-Day Peak", f"£{max_forecast:,.0f}")
    col3.metric("Best Model", best_model)
    col4.metric("Best MAPE", f"{best_mape:.1f}%")

    st.divider()

    # Historical + Forecast
    st.subheader("Historical Revenue + 30-Day Forecast")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=prophet_ready["ds"], y=prophet_ready["y"],
                             mode="lines", name="Historical",
                             line=dict(color="#2c3e50", width=1.5)))
    fig.add_trace(go.Scatter(x=forecast_30d["ds"], y=forecast_30d["yhat"],
                             mode="lines+markers", name="Forecast",
                             line=dict(color="#e74c3c", width=2.5)))
    fig.add_trace(go.Scatter(
        x=pd.concat([forecast_30d["ds"], forecast_30d["ds"][::-1]]),
        y=pd.concat([forecast_30d["yhat_upper"], forecast_30d["yhat_lower"][::-1]]),
        fill="toself", fillcolor="rgba(231, 76, 60, 0.1)",
        line=dict(color="rgba(255,255,255,0)"), name="Confidence Interval",
    ))
    fig.update_layout(height=450, template="plotly_white",
                      xaxis_title="Date", yaxis_title="Revenue (GBP)")
    st.plotly_chart(fig, use_container_width=True)

    # Model comparison
    left, right = st.columns(2)
    with left:
        st.subheader("Model Performance Comparison")
        st.dataframe(comparison.style.highlight_min(subset=["MAPE (%)"], color="#d4edda"),
                     use_container_width=True)

    with right:
        st.subheader("MAPE by Model")
        fig2 = px.bar(comparison.sort_values("MAPE (%)"), x="MAPE (%)", y="Model",
                      orientation="h", color="MAPE (%)",
                      color_continuous_scale="RdYlGn_r")
        fig2.update_layout(height=350, template="plotly_white", showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    # Ensemble detail
    st.subheader("Test Set -- All Model Predictions")
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=ensemble["ds"], y=ensemble["actual"],
                              mode="lines+markers", name="Actual",
                              line=dict(color="#2c3e50", width=2)))
    if "prophet_predicted" in ensemble.columns:
        fig3.add_trace(go.Scatter(x=ensemble["ds"], y=ensemble["prophet_predicted"],
                                  mode="lines", name="Prophet",
                                  line=dict(color="#3498db", width=1.5, dash="dash")))
    if "lstm_predicted" in ensemble.columns:
        fig3.add_trace(go.Scatter(x=ensemble["ds"], y=ensemble["lstm_predicted"],
                                  mode="lines", name="LSTM",
                                  line=dict(color="#e74c3c", width=1.5, dash="dash")))
    if "optimal_blend" in ensemble.columns:
        fig3.add_trace(go.Scatter(x=ensemble["ds"], y=ensemble["optimal_blend"],
                                  mode="lines", name="Hybrid Ensemble",
                                  line=dict(color="#27ae60", width=2.5)))
    fig3.update_layout(height=400, template="plotly_white",
                       xaxis_title="Date", yaxis_title="Revenue (GBP)")
    st.plotly_chart(fig3, use_container_width=True)

    # 30-day forecast table
    st.subheader("30-Day Forecast Details")
    display_fc = forecast_30d.copy()
    display_fc["ds"] = display_fc["ds"].dt.strftime("%Y-%m-%d")
    display_fc.columns = ["Date", "Forecast", "Lower Bound", "Upper Bound"]
    for c in ["Forecast", "Lower Bound", "Upper Bound"]:
        display_fc[c] = display_fc[c].apply(lambda x: f"£{x:,.0f}")
    st.dataframe(display_fc, use_container_width=True)
