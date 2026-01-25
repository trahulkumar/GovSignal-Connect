import streamlit as st
import pandas as pd
import numpy as np
import time

# Helper function to mock simulation data if we can't run the full orchestrator live in Streamlit easily
def generate_mock_data():
    steps = 100
    legacy_ccc = np.random.normal(45, 2, steps) # Legacy Cycle ~45 days
    readiness_ccc = np.random.normal(35, 3, steps) # Optimized Cycle ~35 days
    
    # Introduce a 'shock' where Legacy spikes but Readiness adapts
    spike_start = 60
    legacy_ccc[spike_start:] += np.linspace(0, 20, steps-spike_start)
    readiness_ccc[spike_start:] += np.linspace(0, 5, steps-spike_start) # Better adaptation
    
    return pd.DataFrame({
        "Step": range(steps),
        "Legacy ERP (CCC)": legacy_ccc,
        "Readiness Protocol (CCC)": readiness_ccc
    })

# Streamlit App
st.set_page_config(page_title="GovSignal CFO Dashboard", layout="wide")

st.title("🛡️ GovSignal-Connect: Readiness Protocol Dashboard")
st.markdown("**Financial Intelligence for Critical Supply Chains**")

# Sidebar: Signal Feed
st.sidebar.header("📡 Live Geopolitical Signals")
st.sidebar.markdown("Monitoring `defense.gov` & `sam.gov`...")

# Mock Signals
signals = [
    {"time": "10:42 AM", "msg": "Trade Agreement with key ally signed", "risk": "LOW"},
    {"time": "09:15 AM", "msg": "Semiconductor export restrictions under review", "risk": "MEDIUM"},
    {"time": "08:30 AM", "msg": "DoD announces blockage in Strait of Hormuz", "risk": "HIGH", "action": "Triggered Pre-emptive Buy"},
]

for s in signals:
    color = "green" if s["risk"] == "LOW" else "orange" if s["risk"] == "MEDIUM" else "red"
    st.sidebar.markdown(f"**[{s['time']}]** :{color}[{s['risk']}]")
    st.sidebar.write(f"{s['msg']}")
    if "action" in s:
        st.sidebar.info(f"🤖 AI Action: {s['action']}")
    st.sidebar.markdown("---")

# Main Dashboard
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("Cash Conversion Cycle (CCC) Optimization")
    industry = st.selectbox("Select Industry", ["Semiconductors", "Pharmaceuticals", "Defense Logistics"])
    
    data = generate_mock_data()
    st.line_chart(data.set_index("Step"))
    
    st.markdown("""
    > **Insight:** The Readiness Protocol reduced Cash Conversion Cycle by **22%** during the simulated volatility event (Step 60+).
    """)

with col2:
    st.subheader("Key Metrics")
    st.metric(label="Service Level", value="99.2%", delta="+4.2%")
    st.metric(label="WACC Optimization", value="7.8%", delta="-0.2%")
    st.metric(label="Stockout Risk", value="Low", delta="Stable")

st.markdown("---")
st.subheader("📋 Active Procurement Opportunities (SAM.gov)")
# Mock SAM Data
st.table(pd.DataFrame([
    {"Notice ID": "N-10293", "Title": "Advanced Packaging Research", "Due": "2025-12-01"},
    {"Notice ID": "N-55401", "Title": "Ruggedized Field Laptops", "Due": "2025-11-15"}
]).set_index("Notice ID"))
