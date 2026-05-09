import streamlit as st
import sys
from pathlib import Path

# Ensuring local modules are discoverable
sys.path.append(str(Path(__file__).parent / "src"))
from multi_agent_system.workflows.review_workflow import ReviewWorkflow

# --- PAGE CONFIG ---
st.set_page_config(page_title="NEURAL CLINICAL INTELLIGENCE", page_icon="🧬", layout="wide")

# --- SCI-FI STYLING ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTextArea textarea { background-color: #1a1c24; color: #00ffcc; border: 1px solid #00ffcc; }
    .stButton>button { background-color: #00ffcc; color: #0e1117; border-radius: 2px; font-weight: bold; width: 100%; box-shadow: 0 0 10px #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧬 NEURAL CLINICAL INTELLIGENCE")
st.caption("MAY 2026 RELEASE // GROQ-POWERED STACK")

with st.sidebar:
    st.header("⚡ CORE STATUS")
    st.success("GROQ: Llama 3.3 70B [PRIMARY]")
    st.success("SAMBANOVA: Llama 3.3 [BACKUP]")
    st.info("GEMINI: DISABLED (RETIRED)")

# 1. First, we define the input
question = st.text_area("INPUT RESEARCH QUERY:", placeholder="Enter clinical question...", height=150)

# 2. Then, we only run the workflow IF the button is clicked
if st.button("INITIATE NEURAL RESEARCH", type="primary"):
    if not question.strip():
        st.warning("SYSTEM ERROR: Query input required.")
    else:
        try:
            workflow = ReviewWorkflow()
            with st.status("🧬 INITIATING MULTI-AGENT PROTOCOL...", expanded=True) as status:
                st.write("--- Orchestrating Central Intelligence...")
                st.write("--- Scanning Global Literature (PubMed/Scholar)...")
                st.write("--- Extracting Neural Clinical Data (Throttling Active)...")
                
                result = workflow.run(task=question)
                status.update(label="ANALYSIS COMPLETE", state="complete")
            
            if result and hasattr(result, 'synthesis') and result.synthesis:
                st.header("🔬 CLINICAL SYNTHESIS")
                st.markdown(f"### CONSENSUS\n{result.synthesis.clinical_consensus}")
                st.markdown(f"### RECOMMENDATION\n{result.synthesis.clinical_recommendation}")
            else:
                st.markdown(getattr(result, 'content', "No synthesis data available."))
        except Exception as e:
            st.error(f"CORE FAILURE: {str(e)}")
            st.stop()
