"""Customer Dashboard -- Segmentation, RFM analysis, and churn risk."""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")


def load_data():
    segments = pd.read_csv(os.path.join(DATA_DIR, "customer_segments.csv"))
    churn_path = os.path.join(DATA_DIR, "customer_churn.csv")
    churn = pd.read_csv(churn_path) if os.path.exists(churn_path) else None
    return segments, churn


def render():
    st.header("Customer Dashboard")
    segments, churn = load_data()

    # KPIs
    total_cust = len(segments)
    avg_monetary = segments["monetary"].mean()
    avg_frequency = segments["frequency"].mean()
    avg_recency = segments["recency"].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Customers", f"{total_cust:,}")
    col2.metric("Avg Lifetime Value", f"£{avg_monetary:,.0f}")
    col3.metric("Avg Orders", f"{avg_frequency:.1f}")
    col4.metric("Avg Recency", f"{avg_recency:.0f} days")

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Customer Segments (K-Means)")
        seg_counts = segments["kmeans_label"].value_counts().reset_index()
        seg_counts.columns = ["Segment", "Count"]
        fig = px.pie(seg_counts, values="Count", names="Segment",
                     color_discrete_sequence=px.colors.qualitative.Set2,
                     hole=0.4)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("RFM Score Distribution")
        fig2 = px.histogram(segments, x="rfm_score", nbins=13,
                            color_discrete_sequence=["#3498db"],
                            labels={"rfm_score": "RFM Score"})
        fig2.update_layout(height=400, template="plotly_white",
                           yaxis_title="Customers")
        st.plotly_chart(fig2, use_container_width=True)

    # RFM Scatter
    st.subheader("RFM Analysis -- Recency vs Monetary")
    fig3 = px.scatter(segments, x="recency", y="monetary", color="kmeans_label",
                      size="frequency", size_max=15, opacity=0.6,
                      color_discrete_sequence=px.colors.qualitative.Set2,
                      labels={"recency": "Recency (days)", "monetary": "Monetary (GBP)",
                              "kmeans_label": "Segment"})
    fig3.update_layout(height=450, template="plotly_white")
    st.plotly_chart(fig3, use_container_width=True)

    # Segment details table
    st.subheader("Segment Summary")
    summary = segments.groupby("kmeans_label").agg(
        customers=("Customer ID", "count"),
        avg_recency=("recency", "mean"),
        avg_frequency=("frequency", "mean"),
        avg_monetary=("monetary", "mean"),
        avg_rfm=("rfm_score", "mean"),
    ).round(1).sort_values("avg_monetary", ascending=False)
    st.dataframe(summary, use_container_width=True)

    # Churn section
    if churn is not None:
        st.divider()
        st.subheader("Churn Risk Analysis")

        risk_counts = churn["churn_risk"].value_counts().reset_index()
        risk_counts.columns = ["Risk Level", "Count"]

        col_a, col_b = st.columns(2)
        with col_a:
            fig4 = px.bar(risk_counts, x="Risk Level", y="Count",
                          color="Risk Level",
                          color_discrete_map={"Low Risk": "#27ae60",
                                              "Medium Risk": "#f39c12",
                                              "High Risk": "#e74c3c"})
            fig4.update_layout(height=350, template="plotly_white", showlegend=False)
            st.plotly_chart(fig4, use_container_width=True)

        with col_b:
            fig5 = px.histogram(churn, x="churn_probability", nbins=30,
                                color_discrete_sequence=["#e74c3c"],
                                labels={"churn_probability": "Churn Probability"})
            fig5.update_layout(height=350, template="plotly_white",
                               yaxis_title="Customers")
            st.plotly_chart(fig5, use_container_width=True)

        # High risk customers table
        high_risk = churn[churn["churn_risk"] == "High Risk"].nlargest(10, "churn_probability")
        st.subheader(f"Top 10 Highest Churn Risk Customers")
        st.dataframe(
            high_risk[["Customer ID", "recency", "frequency", "monetary",
                       "churn_probability", "churn_risk"]].reset_index(drop=True),
            use_container_width=True,
        )
