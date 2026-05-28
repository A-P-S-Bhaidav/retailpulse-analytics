"""RetailPulse Analytics — Sales Dashboard."""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")

PALETTE = {
    "primary":   "#1E3A5F",
    "accent":    "#2E86AB",
    "positive":  "#27AE60",
    "warning":   "#F39C12",
    "danger":    "#C0392B",
    "light_bg":  "#F7F9FC",
    "border":    "#E1E8EF",
    "text_main": "#111827",
    "text_sub":  "#6B7280",
}

CHART_LAYOUT = dict(
    template="plotly_white",
    font=dict(family="Inter, Helvetica, Arial, sans-serif", size=12, color=PALETTE["text_main"]),
    margin=dict(l=10, r=10, t=40, b=10),
    paper_bgcolor="white",
    plot_bgcolor="white",
    hoverlabel=dict(bgcolor="white", font_size=13),
)


def card(col, label, value, sub=""):
    col.markdown(f"""
    <div style="background:white;border:1px solid {PALETTE['border']};border-radius:10px;
                padding:20px 16px;text-align:center;box-shadow:0 1px 4px rgba(0,0,0,0.06);">
      <div style="font-size:0.75rem;font-weight:600;color:{PALETTE['text_sub']};
                  text-transform:uppercase;letter-spacing:0.06em;">{label}</div>
      <div style="font-size:1.9rem;font-weight:700;color:{PALETTE['text_main']};
                  margin:6px 0 2px;">{value}</div>
      <div style="font-size:0.78rem;color:{PALETTE['text_sub']};">{sub}</div>
    </div>""", unsafe_allow_html=True)


def render():
    st.markdown(f"""
    <div style="background:{PALETTE['primary']};border-radius:12px;padding:28px 32px;margin-bottom:28px;">
      <div style="color:rgba(255,255,255,0.65);font-size:0.8rem;font-weight:600;
                  letter-spacing:0.1em;text-transform:uppercase;">Module 1 of 4</div>
      <div style="color:white;font-size:1.85rem;font-weight:700;margin-top:4px;">
        Executive Sales Summary</div>
      <div style="color:rgba(255,255,255,0.7);font-size:0.9rem;margin-top:4px;">
        Revenue performance, transaction trends, and time-pattern analysis.</div>
    </div>""", unsafe_allow_html=True)

    daily = pd.read_csv(os.path.join(DATA_DIR, "daily_sales_features.csv"), parse_dates=["Date"])

    total_rev = daily["total_revenue"].sum()
    total_qty = int(daily["total_quantity"].sum())
    total_txn = int(daily["transaction_count"].sum())
    avg_order = total_rev / total_txn if total_txn > 0 else 0
    avg_daily  = daily["total_revenue"].mean()

    c1, c2, c3, c4, c5 = st.columns(5)
    card(c1, "Total Revenue", f"£{total_rev:,.0f}", "All periods")
    card(c2, "Avg Daily Revenue", f"£{avg_daily:,.0f}", "Per trading day")
    card(c3, "Total Units Sold", f"{total_qty:,}", "Items dispatched")
    card(c4, "Total Transactions", f"{total_txn:,}", "Unique invoices")
    card(c5, "Avg Order Value", f"£{avg_order:,.2f}", "Revenue per invoice")

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # Revenue trend
    st.markdown("#### Revenue Trend with Moving Average")
    ma_window = st.slider("Moving average window (days)", 7, 60, 30, key="s_ma")
    daily["MA"] = daily["total_revenue"].rolling(ma_window).mean()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily["Date"], y=daily["total_revenue"],
        mode="lines", name="Daily Revenue",
        line=dict(color="#CBD5E1", width=1),
        fill="tozeroy", fillcolor="rgba(30,58,95,0.04)",
    ))
    fig.add_trace(go.Scatter(
        x=daily["Date"], y=daily["MA"],
        mode="lines", name=f"{ma_window}-day MA",
        line=dict(color=PALETTE["accent"], width=2.5),
    ))
    fig.update_layout(**CHART_LAYOUT, height=360,
                      xaxis_title="Date", yaxis_title="Revenue (£)",
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig, use_container_width=True)

    l, r = st.columns(2)
    with l:
        st.markdown("#### Average Revenue by Day of Week")
        dow_map = {0:"Mon",1:"Tue",2:"Wed",3:"Thu",4:"Fri",5:"Sat",6:"Sun"}
        daily["dow_num"] = daily["Date"].dt.dayofweek
        dow = daily.groupby("dow_num")["total_revenue"].mean().reset_index()
        dow["day"] = dow["dow_num"].map(dow_map)
        colors = [PALETTE["accent"] if v == dow["total_revenue"].max() else "#CBD5E1"
                  for v in dow["total_revenue"]]
        fig2 = go.Figure(go.Bar(x=dow["day"], y=dow["total_revenue"],
                                marker_color=colors, text=dow["total_revenue"].round(0),
                                texttemplate="£%{text:,.0f}", textposition="outside"))
        fig2.update_layout(**CHART_LAYOUT, height=320, yaxis_title="Avg Revenue (£)",
                           showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    with r:
        st.markdown("#### Monthly Revenue")
        monthly = daily.groupby(daily["Date"].dt.to_period("M"))["total_revenue"].sum().reset_index()
        monthly["Date"] = monthly["Date"].dt.to_timestamp()
        monthly["label"] = monthly["Date"].dt.strftime("%b %Y")
        fig3 = go.Figure(go.Bar(
            x=monthly["label"], y=monthly["total_revenue"],
            marker_color=PALETTE["primary"],
            text=monthly["total_revenue"].round(0),
            texttemplate="£%{text:,.0f}", textposition="outside",
        ))
        fig3.update_layout(**CHART_LAYOUT, height=320,
                           yaxis_title="Revenue (£)", showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("#### Daily Transaction Volume")
    fig4 = go.Figure(go.Scatter(
        x=daily["Date"], y=daily["transaction_count"],
        mode="lines", fill="tozeroy",
        line=dict(color=PALETTE["positive"], width=1.5),
        fillcolor="rgba(39,174,96,0.08)",
    ))
    fig4.update_layout(**CHART_LAYOUT, height=240,
                       xaxis_title="Date", yaxis_title="Transactions")
    st.plotly_chart(fig4, use_container_width=True)
