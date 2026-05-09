import streamlit as st
import json
import sys
from pathlib import Path

# Ensure local modules are discoverable
sys.path.append(str(Path(__file__).parent / "src"))

from multi_agent_system.workflows.review_workflow import ReviewWorkflow

st.set_page_config(page_title="Biomedical Research Intelligence", layout="wide")

st.title("🔬 Biomedical Research Intelligence")
st.markdown("### Agentic Systematic Review & Meta-Analysis System")

with st.sidebar:
    st.header("Settings")
    st.info("System is using SambaNova (Llama 3.1 405B) with Gemini 2.0 Flash fallback.")

question = st.text_area(
    "Enter your clinical research question:",
    placeholder="e.g., Is GLP-1 receptor agonist therapy effective for neuroprotection in Parkinson's disease?",
    height=150
)

if st.button("Run Research", type="primary"):
    if not question.strip():
        st.warning("Please enter a research question before running.")
    else:
        workflow = ReviewWorkflow()
        with st.status("Starting workflow...", expanded=True) as status:
            st.write("Orchestrating agents...")
            st.write("Searching PubMed & Semantic Scholar...")
            st.write("Extracting clinical data points...")
            st.write("Synthesizing final report...")
            
            try:
                result = workflow.run(task=question)
                status.update(label="Research complete!", state="complete")
            except Exception as e:
                status.update(label="Workflow failed", state="error")
                st.error("An internal system error occurred. Please try again later.")
                print(f"CRITICAL BACKEND ERROR: {str(e)}")
                st.stop()
        
        if result and hasattr(result, 'synthesis') and result.synthesis:
            st.subheader("Clinical Synthesis")
            st.markdown(f"**Clinical Consensus:** {result.synthesis.clinical_consensus}")
            st.markdown(f"**Evidence Quality:** {result.synthesis.overall_evidence_quality}")
            st.markdown(f"**Recommendation:** {result.synthesis.clinical_recommendation}")
            
            with st.expander("Conflicting Findings"):
                if result.synthesis.conflicting_findings:
                    for finding in result.synthesis.conflicting_findings:
                        st.write(f"- {finding}")
                else:
                    st.write("No major conflicting findings reported.")
        else:
            st.markdown(getattr(result, 'content', "No synthesis generated."))

        with st.expander("Source Citations"):
            if hasattr(result, 'citations') and result.citations:
                for cit in result.citations:
                    st.markdown(f"- **{cit.title}** ({cit.source})")
            else:
                st.write("No citations available.")

        st.download_button(
            "Download Full Report",
            data=str(result),
            file_name="research_report.md",
            mime="text/markdown"
        )
