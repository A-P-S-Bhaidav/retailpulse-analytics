"""RetailPulse Analytics — Inventory Optimization Dashboard."""

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
                  letter-spacing:0.1em;text-transform:uppercase;">Module 4 of 4</div>
      <div style="color:white;font-size:1.85rem;font-weight:700;margin-top:4px;">
        Inventory Optimization</div>
      <div style="color:rgba(255,255,255,0.7);font-size:0.9rem;margin-top:4px;">
        EOQ, safety stock, reorder points, and stockout simulation analysis.</div>
    </div>""", unsafe_allow_html=True)

    metrics = pd.read_csv(os.path.join(DATA_DIR, "inventory_metrics.csv"))
    sim = pd.read_csv(os.path.join(DATA_DIR, "inventory_simulation.csv"), parse_dates=["Date"])
    daily = pd.read_csv(os.path.join(DATA_DIR, "daily_sales_features.csv"), parse_dates=["Date"])

    md = dict(zip(metrics["Metric"], metrics["Value"]))

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    card(c1, "Economic Order Qty", md.get("EOQ", "N/A"), "Units per order")
    card(c2, "Safety Stock (95%)", md.get("Safety Stock (95%)", "N/A"), "Buffer units")
    card(c3, "Reorder Point", md.get("Reorder Point (95%)", "N/A"), "Trigger level")
    card(c4, "Lead Time", md.get("Lead Time", "N/A"), "Days to receive")
    card(c5, "Fill Rate", md.get("Fill Rate", "N/A"), "Service level",
         PALETTE["positive"])
    stockout_days = md.get("Stockout Days", "0")
    card(c6, "Stockout Days", stockout_days, "Days out of stock",
         PALETTE["danger"] if str(stockout_days) not in ["0", "0 days"] else PALETTE["positive"])

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # Parse ROP for reference line
    try:
        rop_num = int(str(md.get("Reorder Point (95%)", "0")).replace(",", "").replace(" units", ""))
    except (ValueError, AttributeError):
        rop_num = 0

    # Stock simulation chart
    st.markdown("#### Inventory Level Simulation (Historical Period)")
    fig = go.Figure()
    stockout_days_sim = sim[sim["stockout"] > 0]
    # Stock fill
    fig.add_trace(go.Scatter(
        x=sim["Date"], y=sim["stock_level"],
        mode="lines", name="Stock Level",
        line=dict(color=PALETTE["accent"], width=2),
        fill="tozeroy", fillcolor="rgba(46,134,171,0.08)",
    ))
    # Reorder events
    reorder_sim = sim[sim["ordered"] > 0]
    if len(reorder_sim) > 0:
        fig.add_trace(go.Scatter(
            x=reorder_sim["Date"], y=reorder_sim["stock_level"],
            mode="markers", name="Reorder Triggered",
            marker=dict(color=PALETTE["warning"], size=9, symbol="triangle-up"),
        ))
    # Stockout events
    if len(stockout_days_sim) > 0:
        fig.add_trace(go.Scatter(
            x=stockout_days_sim["Date"], y=[0] * len(stockout_days_sim),
            mode="markers", name="Stockout Event",
            marker=dict(color=PALETTE["danger"], size=10, symbol="x"),
        ))
    if rop_num > 0:
        fig.add_hline(y=rop_num, line_dash="dash", line_color=PALETTE["danger"],
                      line_width=1.5,
                      annotation_text=f"Reorder Point ({rop_num:,} units)",
                      annotation_position="top right",
                      annotation_font_color=PALETTE["danger"])
    fig.update_layout(**CHART_LAYOUT, height=400,
                      xaxis_title="Date", yaxis_title="Units in Stock",
                      legend=dict(orientation="h", yanchor="bottom", y=1.02))
    st.plotly_chart(fig, use_container_width=True)

    l, r = st.columns(2)
    with l:
        st.markdown("#### Daily Demand Distribution")
        fig2 = go.Figure(go.Histogram(
            x=daily["total_quantity"], nbinsx=40,
            marker=dict(color=PALETTE["primary"], line=dict(color="white", width=1)),
        ))
        mean_qty = daily["total_quantity"].mean()
        fig2.add_vline(x=mean_qty, line_dash="dash", line_color=PALETTE["warning"],
                       annotation_text=f"Mean: {mean_qty:,.0f}",
                       annotation_position="top right")
        fig2.update_layout(**CHART_LAYOUT, height=320,
                           xaxis_title="Daily Units Sold", yaxis_title="Frequency")
        st.plotly_chart(fig2, use_container_width=True)

    with r:
        st.markdown("#### Reorder Events Log")
        orders = sim[sim["ordered"] > 0][["Date", "ordered", "stock_level"]].copy()
        if len(orders) > 0:
            orders.columns = ["Date", "Order Quantity", "Stock at Trigger"]
            orders["Date"] = orders["Date"].dt.strftime("%d %b %Y")
            orders["Order Quantity"] = orders["Order Quantity"].apply(lambda x: f"{x:,.0f}")
            orders["Stock at Trigger"] = orders["Stock at Trigger"].apply(lambda x: f"{x:,.0f}")
            st.dataframe(orders.reset_index(drop=True), use_container_width=True, height=300)
        else:
            st.info("No reorder events were triggered in the simulation period.")

    # Optimization parameters table
    st.markdown("#### Optimization Parameters Reference")
    st.dataframe(metrics, use_container_width=True, hide_index=True)
