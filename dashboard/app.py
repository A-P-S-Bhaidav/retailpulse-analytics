"""RetailPulse Analytics Dashboard -- Main Application."""

import streamlit as st

st.set_page_config(
    page_title="RetailPulse Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem; font-weight: 700; color: #1a1a2e;
        text-align: center; padding: 1rem 0; margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem; border-radius: 12px; color: white; text-align: center;
    }
    .metric-value { font-size: 2rem; font-weight: 700; }
    .metric-label { font-size: 0.9rem; opacity: 0.85; }
    .stTabs [data-baseweb="tab-list"] { gap: 2rem; }
    .stTabs [data-baseweb="tab"] {
        font-size: 1.1rem; font-weight: 600; padding: 0.8rem 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">RetailPulse Analytics Platform</div>', unsafe_allow_html=True)

page = st.sidebar.radio(
    "Navigation",
    ["Sales Dashboard", "Customer Dashboard", "Forecast Dashboard", "Inventory Dashboard"],
    index=0,
)

if page == "Sales Dashboard":
    from pages import sales
    sales.render()
elif page == "Customer Dashboard":
    from pages import customers
    customers.render()
elif page == "Forecast Dashboard":
    from pages import forecast
    forecast.render()
elif page == "Inventory Dashboard":
    from pages import inventory
    inventory.render()
