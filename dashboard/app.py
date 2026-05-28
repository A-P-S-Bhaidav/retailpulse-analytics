"""RetailPulse Analytics Dashboard -- Main Application."""

import streamlit as st

st.set_page_config(
    page_title="RetailPulse Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Professional Corporate CSS styling
st.markdown("""
<style>
    /* Main typography and background */
    .stApp {
        background-color: #F8F9FA;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Header styling */
    .main-header {
        font-size: 2.25rem; 
        font-weight: 600; 
        color: #111827;
        padding-bottom: 0.5rem; 
        margin-bottom: 2rem;
        border-bottom: 2px solid #E5E7EB;
    }
    
    /* Metric Cards Override (Streamlit native metrics) */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 600;
        color: #111827;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem;
        font-weight: 500;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    [data-testid="stMetricDelta"] {
        font-size: 0.875rem;
    }
    
    /* Clean headers */
    h1, h2, h3 {
        color: #111827 !important;
        font-weight: 600 !important;
    }
    
    /* Dataframes */
    .stDataFrame {
        border-radius: 8px;
        border: 1px solid #E5E7EB;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("### RetailPulse Analytics")
st.sidebar.markdown("Executive Intelligence Platform")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Modules",
    ["Executive Sales Summary", "Customer Intelligence", "Demand Forecasting", "Inventory Optimization"],
    index=0,
)

st.sidebar.markdown("---")
st.sidebar.markdown('<span style="color:#6B7280; font-size:0.8rem;">Data synchronized up to: Dec 2011</span>', unsafe_allow_html=True)

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
