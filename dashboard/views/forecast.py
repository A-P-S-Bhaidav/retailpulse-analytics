"""RetailPulse — Demand Forecasting."""

import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from views.design import C, LAYOUT, kpi_card, page_header, section_title

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")


def render():
    page_header("3", "Demand Forecasting",
                "Hybrid Prophet + LSTM ensemble — 30-day revenue outlook with confidence bands.")

    prophet_ready = pd.read_csv(os.path.join(DATA_DIR, "prophet_ready.csv"), parse_dates=["ds"])
    forecast_30d  = pd.read_csv(os.path.join(DATA_DIR, "prophet_forecast_30d.csv"), parse_dates=["ds"])
    ensemble      = pd.read_csv(os.path.join(DATA_DIR, "ensemble_predictions.csv"), parse_dates=["ds"])
    comparison    = pd.read_csv(os.path.join(DATA_DIR, "model_comparison.csv"))

    best_row  = comparison.iloc[0]
    avg_fc    = forecast_30d["yhat"].mean()
    max_fc    = forecast_30d["yhat"].max()
    fc_range  = max_fc - forecast_30d["yhat"].min()

    c1, c2, c3, c4, c5 = st.columns(5)
    kpi_card(c1, "Best Model",            best_row["Model"],       "Lowest test MAPE")
    kpi_card(c2, "Best MAPE",             f"{best_row['MAPE (%)']:.2f}%", "Mean Absolute % Error",
             value_color=C["green"])
    kpi_card(c3, "30-Day Avg Forecast",   f"£{avg_fc:,.0f}",       "Daily average revenue")
    kpi_card(c4, "30-Day Peak",           f"£{max_fc:,.0f}",       "Maximum forecast day")
    kpi_card(c5, "Forecast Swing",        f"£{fc_range:,.0f}",     "Peak minus trough")

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── Historical + 30-day forecast ──────────────────────────────────────────
    section_title("Historical Revenue + 30-Day Forward Forecast")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=prophet_ready["ds"], y=prophet_ready["y"],
        mode="lines", name="Historical Revenue",
        line=dict(color="#94A3B8", width=1.2),
    ))
    fig.add_trace(go.Scatter(
        x=pd.concat([forecast_30d["ds"], forecast_30d["ds"][::-1]]),
        y=pd.concat([forecast_30d["yhat_upper"], forecast_30d["yhat_lower"][::-1]]),
        fill="toself", fillcolor="rgba(5,150,105,0.10)",
        line=dict(color="rgba(255,255,255,0)"),
        name="Confidence Band",
    ))
    fig.add_trace(go.Scatter(
        x=forecast_30d["ds"], y=forecast_30d["yhat"],
        mode="lines+markers", name="30-Day Forecast",
        line=dict(color=C["green"], width=2.5),
        marker=dict(size=5, color=C["green"]),
    ))
    fig.update_layout(**{**LAYOUT, "height": 400,
                          "xaxis_title": "Date", "yaxis_title": "Revenue (£)",
                          "legend": dict(
                              orientation="h", yanchor="bottom", y=1.02,
                              xanchor="right", x=1,
                              font=dict(color=C["text_b"], size=12),
                          )})
    st.plotly_chart(fig, use_container_width=True)

    # ── Model comparison charts ───────────────────────────────────────────────
    l, r = st.columns([1.3, 0.7])

    with l:
        section_title("Test Set: All Models vs. Actual Revenue")
        fig2 = go.Figure()
        if "actual" in ensemble.columns:
            fig2.add_trace(go.Scatter(
                x=ensemble["ds"], y=ensemble["actual"],
                mode="lines+markers", name="Actual",
                line=dict(color=C["navy"], width=2.5),
                marker=dict(size=4),
            ))
        model_traces = [
            ("prophet_predicted", "Prophet",          C["amber"],  "dash"),
            ("lstm_predicted",    "LSTM",              C["red"],    "dot"),
            ("optimal_blend",     "Hybrid Ensemble",   C["green"],  "solid"),
        ]
        for col, label, color, dash in model_traces:
            if col in ensemble.columns:
                fig2.add_trace(go.Scatter(
                    x=ensemble["ds"], y=ensemble[col],
                    mode="lines", name=label,
                    line=dict(color=color, width=2, dash=dash),
                ))
        fig2.update_layout(**{**LAYOUT, "height": 360,
                               "xaxis_title": "Date", "yaxis_title": "Revenue (£)",
                               "legend": dict(
                                   orientation="h", yanchor="bottom", y=1.02,
                                   font=dict(color=C["text_b"], size=12),
                               )})
        st.plotly_chart(fig2, use_container_width=True)

    with r:
        section_title("Model Ranking by MAPE")
        cmp = comparison.sort_values("MAPE (%)")
        bar_cols = [C["green"] if i == 0 else "#CBD5E1" for i in range(len(cmp))]
        fig3 = go.Figure(go.Bar(
            y=cmp["Model"], x=cmp["MAPE (%)"],
            orientation="h",
            marker_color=bar_cols,
            text=cmp["MAPE (%)"].apply(lambda v: f"{v:.2f}%"),
            textposition="outside",
            textfont=dict(color=C["text_b"], size=11),
        ))
        fig3.update_layout(**{**LAYOUT, "height": 360,
                               "xaxis_title": "MAPE (%)", "showlegend": False,
                               "yaxis": dict(
                                   categoryorder="total ascending",
                                   tickfont=dict(color=C["text_b"], size=11),
                               )})
        st.plotly_chart(fig3, use_container_width=True)

    # ── Tables ────────────────────────────────────────────────────────────────
    section_title("Full Model Performance Comparison")
    display = comparison.copy()
    display["MAPE (%)"] = display["MAPE (%)"].apply(lambda v: f"{v:.2f}%")
    display["MAE"]  = display["MAE"].apply(lambda v: f"£{v:,.0f}")
    display["RMSE"] = display["RMSE"].apply(lambda v: f"£{v:,.0f}")
    st.dataframe(display, use_container_width=True, hide_index=True)

    section_title("30-Day Forecast Detail")
    fc_display = forecast_30d[["ds", "yhat", "yhat_lower", "yhat_upper"]].copy()
    fc_display["ds"] = fc_display["ds"].dt.strftime("%d %b %Y")
    fc_display.columns = ["Date", "Forecast (£)", "Lower Bound (£)", "Upper Bound (£)"]
    for col in ["Forecast (£)", "Lower Bound (£)", "Upper Bound (£)"]:
        fc_display[col] = fc_display[col].apply(lambda v: f"£{v:,.0f}")
    st.dataframe(fc_display, use_container_width=True, hide_index=True, height=310)
