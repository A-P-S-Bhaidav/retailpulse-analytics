"""RetailPulse Analytics — Main Entry Point."""

import sys
import os

# Ensure the dashboard directory is on path so views/ is importable
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st

st.set_page_config(
    page_title="RetailPulse Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
  /* Global reset */
  .stApp {
    background: #F0F4F8;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  }

  /* Remove default top padding */
  .block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1400px;
  }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background: #1E3A5F;
    border-right: none;
  }
  [data-testid="stSidebar"] * {
    color: rgba(255,255,255,0.85) !important;
  }
  [data-testid="stSidebar"] .stRadio label {
    color: rgba(255,255,255,0.75) !important;
    font-size: 0.9rem !important;
  }
  [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: rgba(255,255,255,0.5) !important;
    font-size: 0.75rem !important;
  }

  /* Remove Streamlit branding / footer */
  footer { visibility: hidden; }
  #MainMenu { visibility: hidden; }
  header { visibility: hidden; }

  /* Metric override */
  [data-testid="stMetricValue"] {
    font-size: 1.8rem !important;
    font-weight: 700 !important;
  }

  /* Divider */
  hr { border-color: #E1E8EF; }

  /* Table styling */
  .stDataFrame { border-radius: 8px; overflow: hidden; }

  /* Plotly charts */
  .js-plotly-plot { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# Sidebar branding
st.sidebar.markdown("""
<div style="padding: 8px 0 16px 0;">
  <div style="font-size:1.15rem;font-weight:700;color:white;letter-spacing:0.01em;">
    RetailPulse
  </div>
  <div style="font-size:0.72rem;color:rgba(255,255,255,0.45);margin-top:2px;
              text-transform:uppercase;letter-spacing:0.08em;">
    Analytics Platform
  </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown('<div style="font-size:0.7rem;color:rgba(255,255,255,0.4);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px;">Modules</div>', unsafe_allow_html=True)

page = st.sidebar.radio(
    label="",
    options=[
        "Executive Sales Summary",
        "Customer Intelligence",
        "Demand Forecasting",
        "Inventory Optimization",
    ],
    index=0,
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="font-size:0.72rem;color:rgba(255,255,255,0.35);line-height:1.6;">
  Dataset: Online Retail II<br>
  Source: UCI ML Repository<br>
  Period: Dec 2009 – Dec 2011<br>
  Records: 525,461 transactions
</div>
""", unsafe_allow_html=True)

if page == "Executive Sales Summary":
    from views import sales
    sales.render()
elif page == "Customer Intelligence":
    from views import customers
    customers.render()
elif page == "Demand Forecasting":
    from views import forecast
    forecast.render()
elif page == "Inventory Optimization":
    from views import inventory
    inventory.render()
