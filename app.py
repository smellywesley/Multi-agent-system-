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
            
           # --- FULL DASHBOARD VISUALIZATION ---
            if result:
                st.header("🔬 CLINICAL SYNTHESIS")
                
                # 1. The Meta-Analysis
                if hasattr(result, 'content') and result.content:
                    st.markdown(result.content)
                
                # 2. The Structured Bottom-Line
                if hasattr(result, 'synthesis') and result.synthesis:
                    st.markdown(f"### CONSENSUS\n{result.synthesis.clinical_consensus}")
                    st.markdown(f"### RECOMMENDATION\n{result.synthesis.clinical_recommendation}")
                
                # 3. ACADEMIC EVIDENCE CARDS & DOWNLOAD COMPILER
                if hasattr(result, 'extractions') and result.extractions:
                    st.divider()
                    st.header("📚 EXTRACTED CLINICAL EVIDENCE")
                    
                    # Initialize the downloadable text dossier
                    dossier_text = "NEURAL CLINICAL INTELLIGENCE: RESEARCH DOSSIER\n"
                    dossier_text += "="*50 + "\n\n"
                    if hasattr(result, 'synthesis') and result.synthesis:
                        dossier_text += f"CONSENSUS:\n{result.synthesis.clinical_consensus}\n\n"
                        dossier_text += f"RECOMMENDATION:\n{result.synthesis.clinical_recommendation}\n\n"
                    dossier_text += "EVIDENCE BREAKDOWN:\n"
                    dossier_text += "-"*50 + "\n\n"
                    
                    for ext in result.extractions:
                        # Safely parse the extraction data
                        data = ext.extraction
                        if hasattr(data, 'model_dump'):
                            data = data.model_dump()
                        elif not isinstance(data, dict):
                            data = {} # Fallback if parsing fails

                        study_design = data.get('study_design', 'N/A')
                        pubmed_url = f"https://pubmed.ncbi.nlm.nih.gov/{ext.pmid}/"
                        doi_display = ext.doi if ext.doi else "Not provided"

                        # Build the Professional UI Card
                        with st.expander(f"📄 {study_design} (PMID: {ext.pmid})"):
                            st.markdown(f"**🔗 Source:** [View on PubMed]({pubmed_url}) | **DOI:** {doi_display}")
                            st.markdown(f"**👥 Sample Size:** {data.get('sample_size', 'N/A')}")
                            st.markdown(f"**💡 Key Findings:** {data.get('key_findings', 'N/A')}")
                            st.markdown(f"**⚠️ Limitations:** {data.get('limitations', 'N/A')}")
                            
                            bias = data.get('risk_of_bias_flags', [])
                            if bias:
                                st.markdown(f"**🚩 Risk of Bias:** {', '.join(bias)}")

                        # Add this paper to the downloadable dossier
                        dossier_text += f"Paper PMID: {ext.pmid}\n"
                        dossier_text += f"URL: {pubmed_url}\n"
                        dossier_text += f"DOI: {doi_display}\n"
                        dossier_text += f"Study Design: {study_design}\n"
                        dossier_text += f"Sample Size: {data.get('sample_size', 'N/A')}\n"
                        dossier_text += f"Key Findings: {data.get('key_findings', 'N/A')}\n"
                        dossier_text += f"Limitations: {data.get('limitations', 'N/A')}\n"
                        if bias:
                            dossier_text += f"Risk of Bias: {', '.join(bias)}\n"
                        dossier_text += "\n" + "-"*30 + "\n\n"

                    st.divider()
                    # 4. THE DOWNLOAD BUTTON
                    st.download_button(
                        label="📥 DOWNLOAD CLINICAL DOSSIER (TXT)",
                        data=dossier_text,
                        file_name="clinical_research_dossier.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
            else:
                st.error("No data returned from the multi-agent workflow.")
                
        except Exception as e:
            st.error(f"CORE FAILURE: {str(e)}")
            st.stop()
