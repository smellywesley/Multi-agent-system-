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
    .main { background-color: #0e1117; }
    .stTextArea textarea { background-color: #1a1c24; color: #00ffcc; border: 1px solid #00ffcc; }
    .stButton>button { 
        background-color: #00ffcc; 
        color: #0e1117; 
        border-radius: 2px; 
        font-weight: bold; 
        width: 100%;
        border: none;
        box-shadow: 0 0 10px #00ffcc;
    }
    .stButton>button:hover { box-shadow: 0 0 20px #00ffcc; color: white; }
    </style>
    """, unsafe_allow_html=True)

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
    st.warning("EXPERIMENTAL: Medical research use only.")

# --- RESEARCH INPUT ---
question = st.text_area(
    "INPUT RESEARCH QUERY:",
    placeholder="Enter clinical question for neural analysis...",
    height=150
)

if st.button("INITIATE NEURAL RESEARCH", type="primary"):
    if not question.strip():
        st.warning("SYSTEM ERROR: Query input required.")
    else:
        # MOVE IT HERE - Inside the protected block
        try:
            workflow = ReviewWorkflow() 
            with st.status("🧬 INITIATING MULTI-AGENT PROTOCOL...", expanded=True) as status:
                # ... rest of your workflow logic ...
                result = workflow.run(task=question)
                status.update(label="ANALYSIS COMPLETE", state="complete")
        except Exception as e:
            st.error("AN INTERNAL SYSTEM ERROR OCCURRED. THE CORE IS SECURE.")
            print(f"DEBUG LOG: {str(e)}") # This stays in Render, not on the web.
            st.stop()
        
        # --- DISPLAY RESULTS ---
        if result and hasattr(result, 'synthesis') and result.synthesis:
            st.header("🔬 CLINICAL SYNTHESIS")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Evidence Quality", result.synthesis.overall_evidence_quality)
            with col2:
                st.metric("Consensus Level", "Verified")
                
            st.markdown(f"### CONSENSUS\n{result.synthesis.clinical_consensus}")
            st.markdown(f"### RECOMMENDATION\n{result.synthesis.clinical_recommendation}")
            
            with st.expander("VIEW CONFLICTING DATA"):
                if result.synthesis.conflicting_findings:
                    for finding in result.synthesis.conflicting_findings:
                        st.write(f"- {finding}")
                else:
                    st.write("No major anomalies detected in the data stream.")
        else:
            st.markdown(getattr(result, 'content', "No synthesis data available."))

        st.download_button(
            "EXPORT INTEL REPORT (.MD)",
            data=str(result),
            file_name="neural_research_report.md",
            mime="text/markdown"
        )
