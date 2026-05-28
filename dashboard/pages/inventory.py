"""Inventory Dashboard -- Stock levels, reorder points, and optimization metrics."""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")


def load_data():
    metrics = pd.read_csv(os.path.join(DATA_DIR, "inventory_metrics.csv"))
    sim = pd.read_csv(os.path.join(DATA_DIR, "inventory_simulation.csv"), parse_dates=["Date"])
    daily = pd.read_csv(os.path.join(DATA_DIR, "daily_sales_features.csv"), parse_dates=["Date"])
    return metrics, sim, daily


def render():
    st.header("Inventory Dashboard")
    metrics, sim, daily = load_data()

    # KPIs from metrics
    metrics_dict = dict(zip(metrics["Metric"], metrics["Value"]))

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("EOQ", metrics_dict.get("EOQ", "N/A"))
    col2.metric("Safety Stock (95%)", metrics_dict.get("Safety Stock (95%)", "N/A"))
    col3.metric("Reorder Point", metrics_dict.get("Reorder Point (95%)", "N/A"))
    col4.metric("Fill Rate", metrics_dict.get("Fill Rate", "N/A"))

    st.divider()

    # Inventory simulation
    st.subheader("Inventory Level Simulation")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sim["Date"], y=sim["stock_level"],
                             mode="lines", name="Stock Level",
                             line=dict(color="#3498db", width=2),
                             fill="tozeroy", fillcolor="rgba(52, 152, 219, 0.1)"))

    # Add reorder point line
    rop_val = metrics_dict.get("Reorder Point (95%)", "0")
    try:
        rop_num = int(rop_val.replace(",", "").split()[0])
    except (ValueError, IndexError):
        rop_num = 0
    fig.add_hline(y=rop_num, line_dash="dash", line_color="#e74c3c",
                  annotation_text=f"Reorder Point ({rop_num:,})")

    fig.update_layout(height=400, template="plotly_white",
                      xaxis_title="Date", yaxis_title="Units in Stock")
    st.plotly_chart(fig, use_container_width=True)

    # Two-column layout
    left, right = st.columns(2)

    with left:
        st.subheader("Daily Demand Distribution")
        fig2 = px.histogram(daily, x="total_quantity", nbins=40,
                            color_discrete_sequence=["#2ecc71"],
                            labels={"total_quantity": "Daily Quantity"})
        fig2.update_layout(height=350, template="plotly_white",
                           yaxis_title="Frequency")
        st.plotly_chart(fig2, use_container_width=True)

    with right:
        st.subheader("Stockout Events")
        stockout_days = sim[sim["stockout"] > 0]
        if len(stockout_days) > 0:
            fig3 = px.bar(stockout_days, x="Date", y="stockout",
                          color_discrete_sequence=["#e74c3c"],
                          labels={"stockout": "Units Short"})
            fig3.update_layout(height=350, template="plotly_white")
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.success("No stockout events in the simulation period.")

    # Reorder events
    st.subheader("Reorder Events Timeline")
    orders = sim[sim["ordered"] > 0][["Date", "ordered", "stock_level"]].copy()
    orders.columns = ["Date", "Order Quantity", "Stock at Order"]
    if len(orders) > 0:
        st.dataframe(orders.reset_index(drop=True), use_container_width=True)
    else:
        st.info("No reorder events in the simulation period.")

    # Optimization metrics table
    st.subheader("Optimization Parameters")
    st.dataframe(metrics, use_container_width=True, hide_index=True)
