"""Sales Dashboard -- Revenue trends, KPIs, and transaction analysis."""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")


def load_data():
    daily = pd.read_csv(os.path.join(DATA_DIR, "daily_sales_features.csv"), parse_dates=["Date"])
    return daily


def render():
    st.header("Sales Dashboard")
    daily = load_data()

    # KPI row
    total_rev = daily["total_revenue"].sum()
    total_qty = daily["total_quantity"].sum()
    total_txn = daily["transaction_count"].sum()
    avg_order = total_rev / total_txn if total_txn > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"£{total_rev:,.0f}")
    col2.metric("Total Quantity", f"{total_qty:,.0f}")
    col3.metric("Total Transactions", f"{total_txn:,.0f}")
    col4.metric("Avg Order Value", f"£{avg_order:,.2f}")

    st.divider()

    # Revenue trend
    st.subheader("Revenue Trend")
    ma_window = st.slider("Moving Average Window (days)", 7, 60, 30, key="sales_ma")
    daily["MA"] = daily["total_revenue"].rolling(ma_window).mean()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=daily["Date"], y=daily["total_revenue"],
                             mode="lines", name="Daily Revenue",
                             line=dict(color="#bdc3c7", width=1), opacity=0.5))
    fig.add_trace(go.Scatter(x=daily["Date"], y=daily["MA"],
                             mode="lines", name=f"{ma_window}-day MA",
                             line=dict(color="#3498db", width=3)))
    fig.update_layout(height=400, template="plotly_white",
                      xaxis_title="Date", yaxis_title="Revenue (GBP)")
    st.plotly_chart(fig, use_container_width=True)

    # Two-column layout
    left, right = st.columns(2)

    with left:
        st.subheader("Day of Week Analysis")
        dow = daily.groupby("day_of_week")["total_revenue"].mean().reset_index()
        dow["day_name"] = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        fig2 = px.bar(dow, x="day_name", y="total_revenue", color="total_revenue",
                      color_continuous_scale="Blues", labels={"total_revenue": "Avg Revenue"})
        fig2.update_layout(height=350, showlegend=False, template="plotly_white")
        st.plotly_chart(fig2, use_container_width=True)

    with right:
        st.subheader("Monthly Revenue")
        daily["month_name"] = daily["Date"].dt.strftime("%b %Y")
        monthly = daily.groupby(daily["Date"].dt.to_period("M"))["total_revenue"].sum().reset_index()
        monthly["Date"] = monthly["Date"].dt.to_timestamp()
        fig3 = px.bar(monthly, x="Date", y="total_revenue",
                      color_discrete_sequence=["#27ae60"])
        fig3.update_layout(height=350, template="plotly_white",
                           xaxis_title="Month", yaxis_title="Revenue")
        st.plotly_chart(fig3, use_container_width=True)

    # Transaction volume
    st.subheader("Daily Transaction Volume")
    fig4 = px.area(daily, x="Date", y="transaction_count",
                   color_discrete_sequence=["#9b59b6"])
    fig4.update_layout(height=300, template="plotly_white")
    st.plotly_chart(fig4, use_container_width=True)
