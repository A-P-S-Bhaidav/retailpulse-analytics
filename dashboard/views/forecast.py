"""RetailPulse Analytics — Demand Forecasting Dashboard."""

import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")

PALETTE = {
    "primary":   "#1E3A5F",
    "accent":    "#2E86AB",
    "positive":  "#27AE60",
    "warning":   "#F39C12",
    "danger":    "#C0392B",
    "prophet":   "#8E44AD",
    "lstm":      "#E74C3C",
    "ensemble":  "#27AE60",
    "border":    "#E1E8EF",
    "text_main": "#111827",
    "text_sub":  "#6B7280",
}

CHART_LAYOUT = dict(
    template="plotly_white",
    font=dict(family="Inter, Helvetica, Arial, sans-serif", size=12, color=PALETTE["text_main"]),
    margin=dict(l=10, r=10, t=40, b=10),
    paper_bgcolor="white", plot_bgcolor="white",
    hoverlabel=dict(bgcolor="white", font_size=13),
)


def card(col, label, value, sub="", color=None):
    c = color or PALETTE["text_main"]
    col.markdown(f"""
    <div style="background:white;border:1px solid {PALETTE['border']};border-radius:10px;
                padding:20px 16px;text-align:center;box-shadow:0 1px 4px rgba(0,0,0,0.06);">
      <div style="font-size:0.75rem;font-weight:600;color:{PALETTE['text_sub']};
                  text-transform:uppercase;letter-spacing:0.06em;">{label}</div>
      <div style="font-size:1.9rem;font-weight:700;color:{c};margin:6px 0 2px;">{value}</div>
      <div style="font-size:0.78rem;color:{PALETTE['text_sub']};">{sub}</div>
    </div>""", unsafe_allow_html=True)


def render():
    st.markdown(f"""
    <div style="background:{PALETTE['primary']};border-radius:12px;padding:28px 32px;margin-bottom:28px;">
      <div style="color:rgba(255,255,255,0.65);font-size:0.8rem;font-weight:600;
                  letter-spacing:0.1em;text-transform:uppercase;">Module 3 of 4</div>
      <div style="color:white;font-size:1.85rem;font-weight:700;margin-top:4px;">
        Demand Forecasting</div>
      <div style="color:rgba(255,255,255,0.7);font-size:0.9rem;margin-top:4px;">
        Hybrid Prophet + LSTM ensemble model — 30-day revenue outlook.</div>
    </div>""", unsafe_allow_html=True)

    prophet_ready = pd.read_csv(os.path.join(DATA_DIR, "prophet_ready.csv"), parse_dates=["ds"])
    forecast_30d  = pd.read_csv(os.path.join(DATA_DIR, "prophet_forecast_30d.csv"), parse_dates=["ds"])
    ensemble      = pd.read_csv(os.path.join(DATA_DIR, "ensemble_predictions.csv"), parse_dates=["ds"])
    comparison    = pd.read_csv(os.path.join(DATA_DIR, "model_comparison.csv"))

    best_row  = comparison.iloc[0]
    avg_fc    = forecast_30d["yhat"].mean()
    max_fc    = forecast_30d["yhat"].max()
    fc_range  = max_fc - forecast_30d["yhat"].min()

    c1, c2, c3, c4, c5 = st.columns(5)
    card(c1, "Best Model", best_row["Model"], f"Lowest MAPE")
    card(c2, "Best MAPE", f"{best_row['MAPE (%)']:.2f}%", "Mean Absolute % Error", PALETTE["positive"])
    card(c3, "30-Day Avg Forecast", f"£{avg_fc:,.0f}", "Daily average")
    card(c4, "30-Day Peak", f"£{max_fc:,.0f}", "Maximum predicted day")
    card(c5, "Forecast Range", f"£{fc_range:,.0f}", "Peak minus trough")

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # Historical + 30-day forecast
    st.markdown("#### Historical Revenue + 30-Day Forecast")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=prophet_ready["ds"], y=prophet_ready["y"],
        mode="lines", name="Historical Revenue",
        line=dict(color="#CBD5E1", width=1.2),
    ))
    # confidence band
    fig.add_trace(go.Scatter(
        x=pd.concat([forecast_30d["ds"], forecast_30d["ds"][::-1]]),
        y=pd.concat([forecast_30d["yhat_upper"], forecast_30d["yhat_lower"][::-1]]),
        fill="toself", fillcolor="rgba(39,174,96,0.10)",
        line=dict(color="rgba(255,255,255,0)"),
        name="Confidence Band", showlegend=True,
    ))
    fig.add_trace(go.Scatter(
        x=forecast_30d["ds"], y=forecast_30d["yhat"],
        mode="lines+markers", name="30-Day Forecast",
        line=dict(color=PALETTE["positive"], width=2.5),
        marker=dict(size=5, color=PALETTE["positive"]),
    ))
    fig.update_layout(**CHART_LAYOUT, height=400,
                      xaxis_title="Date", yaxis_title="Revenue (£)",
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig, use_container_width=True)

    # Model comparison
    l, r = st.columns([1.2, 0.8])
    with l:
        st.markdown("#### Test Set: All Models vs. Actual")
        fig2 = go.Figure()
        if "actual" in ensemble.columns:
            fig2.add_trace(go.Scatter(
                x=ensemble["ds"], y=ensemble["actual"],
                mode="lines+markers", name="Actual",
                line=dict(color=PALETTE["primary"], width=2.5),
                marker=dict(size=5),
            ))
        col_map = {
            "prophet_predicted": ("Prophet",  PALETTE["prophet"], "dash"),
            "lstm_predicted":    ("LSTM",     PALETTE["lstm"],    "dot"),
            "optimal_blend":     ("Ensemble", PALETTE["ensemble"], "solid"),
        }
        for col, (label, color, dash) in col_map.items():
            if col in ensemble.columns:
                fig2.add_trace(go.Scatter(
                    x=ensemble["ds"], y=ensemble[col],
                    mode="lines", name=label,
                    line=dict(color=color, width=2, dash=dash),
                ))
        fig2.update_layout(**CHART_LAYOUT, height=360,
                           xaxis_title="Date", yaxis_title="Revenue (£)",
                           legend=dict(orientation="h", yanchor="bottom", y=1.02))
        st.plotly_chart(fig2, use_container_width=True)

    with r:
        st.markdown("#### Model MAPE Ranking")
        cmp_sorted = comparison.sort_values("MAPE (%)")
        bar_colors = [PALETTE["positive"] if i == 0 else "#CBD5E1"
                      for i in range(len(cmp_sorted))]
        fig3 = go.Figure(go.Bar(
            y=cmp_sorted["Model"], x=cmp_sorted["MAPE (%)"],
            orientation="h", marker_color=bar_colors,
            text=cmp_sorted["MAPE (%)"].apply(lambda x: f"{x:.2f}%"),
            textposition="outside",
        ))
        fig3.update_layout(**CHART_LAYOUT, height=360, xaxis_title="MAPE (%)",
                           showlegend=False,
                           yaxis=dict(categoryorder="total ascending"))
        st.plotly_chart(fig3, use_container_width=True)

    # Model metrics table
    st.markdown("#### Full Model Comparison Table")
    display = comparison.copy()
    display["MAE"] = display["MAE"].apply(lambda x: f"£{x:,.0f}")
    display["RMSE"] = display["RMSE"].apply(lambda x: f"£{x:,.0f}")
    display["MAPE (%)"] = display["MAPE (%)"].apply(lambda x: f"{x:.2f}%")
    st.dataframe(display, use_container_width=True, hide_index=True)

    # 30-day table
    st.markdown("#### 30-Day Forward Forecast Detail")
    fc_display = forecast_30d[["ds","yhat","yhat_lower","yhat_upper"]].copy()
    fc_display["ds"] = fc_display["ds"].dt.strftime("%d %b %Y")
    fc_display.columns = ["Date", "Forecast (£)", "Lower Bound (£)", "Upper Bound (£)"]
    for c in ["Forecast (£)", "Lower Bound (£)", "Upper Bound (£)"]:
        fc_display[c] = fc_display[c].apply(lambda x: f"£{x:,.0f}")
    st.dataframe(fc_display, use_container_width=True, hide_index=True, height=300)
