"""RetailPulse Analytics — Customer Intelligence Dashboard."""

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

SEG_COLORS = {
    "VIP / Champions":  "#1E3A5F",
    "Dormant":          "#CBD5E1",
    "High Value":       "#2E86AB",
    "At Risk":          "#C0392B",
    "New Customers":    "#27AE60",
    "Loyal":            "#8E44AD",
}

RISK_COLORS = {
    "High Risk":   "#C0392B",
    "Medium Risk": "#F39C12",
    "Low Risk":    "#27AE60",
}


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
                  letter-spacing:0.1em;text-transform:uppercase;">Module 2 of 4</div>
      <div style="color:white;font-size:1.85rem;font-weight:700;margin-top:4px;">
        Customer Intelligence</div>
      <div style="color:rgba(255,255,255,0.7);font-size:0.9rem;margin-top:4px;">
        RFM segmentation, clustering analysis, and churn risk profiling.</div>
    </div>""", unsafe_allow_html=True)

    segments = pd.read_csv(os.path.join(DATA_DIR, "customer_segments.csv"))
    churn_path = os.path.join(DATA_DIR, "customer_churn.csv")
    churn = pd.read_csv(churn_path) if os.path.exists(churn_path) else None

    total = len(segments)
    avg_mon = segments["monetary"].mean()
    avg_freq = segments["frequency"].mean()
    avg_rec = segments["recency"].mean()
    high_risk_n = len(churn[churn["churn_risk"] == "High Risk"]) if churn is not None else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    card(c1, "Total Customers", f"{total:,}", "Unique buyer IDs")
    card(c2, "Avg Lifetime Value", f"£{avg_mon:,.0f}", "Monetary RFM metric")
    card(c3, "Avg Order Frequency", f"{avg_freq:.1f}", "Orders per customer")
    card(c4, "Avg Recency", f"{avg_rec:.0f} days", "Since last purchase")
    card(c5, "High-Risk Churners", f"{high_risk_n:,}", "Require intervention", PALETTE["danger"])

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    l, r = st.columns([1, 1])
    with l:
        st.markdown("#### Customer Segments (K-Means, k=4)")
        seg_counts = segments["kmeans_label"].value_counts().reset_index()
        seg_counts.columns = ["Segment", "Customers"]
        seg_counts["color"] = seg_counts["Segment"].map(SEG_COLORS)
        fig = go.Figure(go.Pie(
            labels=seg_counts["Segment"], values=seg_counts["Customers"],
            hole=0.55,
            marker=dict(colors=[SEG_COLORS.get(s, "#94A3B8") for s in seg_counts["Segment"]],
                        line=dict(color="white", width=2)),
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>%{value:,} customers<br>%{percent}<extra></extra>",
        ))
        fig.update_layout(**CHART_LAYOUT, height=360, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with r:
        st.markdown("#### RFM Score Distribution")
        fig2 = go.Figure(go.Histogram(
            x=segments["rfm_score"], nbinsx=12,
            marker=dict(color=PALETTE["accent"], line=dict(color="white", width=1.5)),
        ))
        fig2.update_layout(**CHART_LAYOUT, height=360,
                           xaxis_title="RFM Score (3–9)", yaxis_title="Number of Customers")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("#### RFM Scatter — Recency vs. Monetary Value by Segment")
    fig3 = px.scatter(
        segments, x="recency", y="monetary", color="kmeans_label", size="frequency",
        size_max=16, opacity=0.65,
        color_discrete_map=SEG_COLORS,
        labels={"recency": "Recency (days since last purchase)",
                "monetary": "Monetary Value (£)", "kmeans_label": "Segment",
                "frequency": "Order Frequency"},
        hover_data={"recency": True, "monetary": True, "frequency": True},
    )
    fig3.update_layout(**CHART_LAYOUT, height=420,
                       legend=dict(orientation="h", yanchor="bottom", y=1.02))
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("#### Segment Profile Summary")
    summary = segments.groupby("kmeans_label").agg(
        Customers=("Customer ID", "count"),
        Avg_Recency=("recency", "mean"),
        Avg_Frequency=("frequency", "mean"),
        Avg_Monetary=("monetary", "mean"),
        Avg_RFM_Score=("rfm_score", "mean"),
    ).round(1).sort_values("Avg_Monetary", ascending=False)
    summary.index.name = "Segment"
    summary.columns = ["Customers", "Avg Recency (days)", "Avg Orders", "Avg Spend (£)", "Avg RFM Score"]
    st.dataframe(summary.style.background_gradient(subset=["Avg Spend (£)"], cmap="Blues"),
                 use_container_width=True)

    if churn is not None:
        st.markdown("---")
        st.markdown("#### Churn Risk Analysis")
        cl, cr = st.columns(2)
        with cl:
            risk_counts = churn["churn_risk"].value_counts().reset_index()
            risk_counts.columns = ["Risk Level", "Customers"]
            fig4 = go.Figure(go.Bar(
                x=risk_counts["Risk Level"], y=risk_counts["Customers"],
                marker_color=[RISK_COLORS.get(r, "#94A3B8") for r in risk_counts["Risk Level"]],
                text=risk_counts["Customers"],
                texttemplate="%{text:,}", textposition="outside",
            ))
            fig4.update_layout(**CHART_LAYOUT, height=320,
                               yaxis_title="Customers", showlegend=False,
                               title="Customers by Risk Tier")
            st.plotly_chart(fig4, use_container_width=True)

        with cr:
            fig5 = go.Figure(go.Histogram(
                x=churn["churn_probability"], nbinsx=30,
                marker=dict(color=PALETTE["danger"], line=dict(color="white", width=1)),
            ))
            fig5.update_layout(**CHART_LAYOUT, height=320,
                               xaxis_title="Churn Probability Score",
                               yaxis_title="Customers",
                               title="Churn Probability Distribution")
            st.plotly_chart(fig5, use_container_width=True)

        st.markdown("#### Top 15 Highest-Risk Customers")
        top_risk = churn[churn["churn_risk"] == "High Risk"].nlargest(15, "churn_probability")[
            ["Customer ID", "recency", "frequency", "monetary", "churn_probability", "churn_risk"]
        ].reset_index(drop=True)
        top_risk.columns = ["Customer ID", "Recency (days)", "Orders", "Spend (£)",
                             "Churn Probability", "Risk Level"]
        st.dataframe(top_risk.style.background_gradient(subset=["Churn Probability"], cmap="Reds"),
                     use_container_width=True)
