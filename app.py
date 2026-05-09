import streamlit as st
import json
import sys
import time
from pathlib import Path

# Ensuring local modules are discoverable
sys.path.append(str(Path(__file__).parent / "src"))
from multi_agent_system.workflows.review_workflow import ReviewWorkflow

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="NEURAL CLINICAL INTELLIGENCE", 
    page_icon="🧬", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SCI-FI STYLING ---
st.markdown("""
    <style>
    .reportview-container { background: #0e1117; color: #00ffcc; }
    .stButton>button { background-color: #00ffcc; color: black; border-radius: 5px; font-weight: bold; width: 100%; }
    .stTextInput>div>div>input { color: #00ffcc; }
    </style>
    """, unsafe_allow_stdio=True)

st.title("🧬 NEURAL CLINICAL INTELLIGENCE")
st.caption("MAY 2026 RELEASE // MULTI-AGENT SYSTEM [STABLE V4.2]")

with st.sidebar:
    st.header("⚡ CORE STATUS")
    st.success("SAMBANOVA: Llama 3.3 70B [ACTIVE]")
    st.success("GOOGLE AI: Gemini 3 Flash [READY]")
    st.divider()
    st.markdown("### SYSTEM SPECS")
    st.info("- Reasoning: DeepSeek-V3.2 Engine\n- Context Window: 128K\n- Latency: < 200ms")
    st.divider()
    st.warning("EXPERIMENTAL: Medical advice is not intended. For research intelligence only.")

# --- RESEARCH INPUT ---
question = st.text_area(
    "INPUT RESEARCH QUERY:",
    placeholder="Enter clinical question for neural analysis...",
    height=100
)
