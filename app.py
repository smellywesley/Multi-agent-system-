import streamlit as st
import sys
from pathlib import Path

# Ensuring local modules are discoverable
sys.path.append(str(Path(__file__).parent / "src"))
from multi_agent_system.workflows.review_workflow import ReviewWorkflow

# --- PAGE CONFIG ---
st.set_page_config(page_title="Clinical Intelligence", page_icon="", layout="wide")

# --- APPLE PRO STYLING ---
# Everything between the """ quotes is protected CSS, so Python won't crash on it
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
        color: #f5f5f7;
    }

    .stApp {
        background: linear-gradient(-45deg, #000000, #0a1128, #110822, #000000, #050d1a);
        background-size: 400% 400%;
        animation: fluidAurora 25s ease infinite;
        background-attachment: fixed; 
    }
    
    @keyframes fluidAurora {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    [data-testid="stHeader"] {
        background: rgba(0, 0, 0, 0.4) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    footer {visibility: hidden;}

    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        color: #f5f5f7;
        font-size: 16px;
        padding: 16px;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    .stTextArea textarea:focus {
        border-color: #2997ff;
        box-shadow: 0 0 0 4px rgba(41, 151, 255, 0.15);
        background: rgba(255, 255, 255, 0.08);
    }

    .stButton>button {
        background-color: rgba(255, 255, 255, 0.9);
        color: #000000;
        border: none;
        border-radius: 980px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.4s cubic-bezier(0.25, 1, 0.5, 1);
        width: 100%;
        backdrop-filter: blur(10px);
    }
    .stButton>button:hover {
        transform: scale(1.02);
        background-color: #ffffff;
        box-shadow: 0 4px 20px rgba(255, 255, 255, 0.3), 0 0 40px rgba(41, 151, 255, 0.2);
    }

    .stDownloadButton>button {
        background-color: rgba(41, 151, 255, 0.1);
        color: #2997ff;
        border: 1px solid rgba(41, 151, 255, 0.5);
        border-radius: 980px;
        width: 100%;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    .stDownloadButton>button:hover {
        background-color: #2997ff;
        color: #ffffff;
        transform: scale(1.02);
        box-shadow: 0 4px 20px rgba(41, 151, 255, 0.4);
    }

    div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        overflow: hidden;
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        transition: transform 0.4s cubic-bezier(0.25, 1, 0.5, 1), border-color 0.3s ease, background 0.3s ease;
        margin-bottom: 12px;
    }
    div[data-testid="stExpander"]:hover {
        transform: translateY(-3px) scale(1.005);
        border-color: rgba(255, 255, 255, 0.2);
        background: rgba(255, 255, 255, 0.05);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    div[data-testid="stExpander"] summary {
        font-weight: 600;
        letter-spacing: 0.3px;
        color: #f5f5f7;
    }

    h1, h2, h3 {
        font-weight: 700;
        letter-spacing: -0.015em;
    }
    
    .apple-title {
        font-size: 56px;
        font-weight: 700;
        letter-spacing: -0.02em;
        background: linear-gradient(180deg, #ffffff 0%, #a1a1a6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 40px;
        padding-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- PREMIUM HEADER ---
# Removed the "Powered by Groq" subtitle to keep it minimal
st.markdown('<div class="apple-title">Clinical Intelligence.</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Architecture Status")
    st.success("Primary Engine: Groq 8B")
    st.info("Failover Engine: SambaNova 70B")

question = st.text_area("", placeholder="Enter a clinical research question...", height=120)

if st.button("Initiate Research Protocol"):
    if not question.strip():
        st.warning("Please enter a clinical query to begin.")
    else:
        try:
            workflow = ReviewWorkflow()
            with st.status("Aggregating Global Literature...", expanded=True) as status:
                st.write("Orchestrating multi-agent protocol...")
                st.write("Scanning PubMed databases...")
                st.write("Extracting clinical trial data...")
                
                result = workflow.run(task=question)
                status.update(label="Synthesis Complete", state="complete")
            
            # --- FULL DASHBOARD VISUALIZATION ---
            if result:
                st.divider()
                st.header("Executive Summary")
                
                if hasattr(result, 'content') and result.content:
                    st.markdown(result.content)
                
                if hasattr(result, 'synthesis') and result.synthesis:
                    st.markdown(f"### Consensus\n{result.synthesis.clinical_consensus}")
                    st.markdown(f"### Recommendation\n{result.synthesis.clinical_recommendation}")
                
                if hasattr(result, 'extractions') and result.extractions:
                    st.divider()
                    st.header("Clinical Evidence Base")
                    
                    dossier_text = "CLINICAL INTELLIGENCE: RESEARCH DOSSIER\n"
                    dossier_text += "="*50 + "\n\n"
                    if hasattr(result, 'synthesis') and result.synthesis:
                        dossier_text += f"CONSENSUS:\n{result.synthesis.clinical_consensus}\n\n"
                        dossier_text += f"RECOMMENDATION:\n{result.synthesis.clinical_recommendation}\n\n"
                    dossier_text += "EVIDENCE BREAKDOWN:\n"
                    dossier_text += "-"*50 + "\n\n"
                    
                    for ext in result.extractions:
                        data = ext.extraction
                        if hasattr(data, 'model_dump'):
                            data = data.model_dump()
                        elif not isinstance(data, dict):
                            data = {} 

                        study_design = data.get('study_design', 'Unknown Design')
                        pubmed_url = f"https://pubmed.ncbi.nlm.nih.gov/{ext.pmid}/"
                        doi_display = ext.doi if ext.doi else "Not provided"

                        # Cleaned-up minimalist evidence cards
                        with st.expander(f"📄 {study_design} (PMID: {ext.pmid})"):
                            st.markdown(f"**🔗 Source:** [View on PubMed]({pubmed_url}) | **DOI:** {doi_display}")
                            st.markdown(f"**📝 Summary of Findings:** {data.get('key_findings', 'N/A')}")

                        # Dossier compiler
                        dossier_text += f"Paper PMID: {ext.pmid}\n"
                        dossier_text += f"URL: {pubmed_url}\n"
                        dossier_text += f"DOI: {doi_display}\n"
                        dossier_text += f"Study Design: {study_design}\n"
                        dossier_text += f"Summary of Findings: {data.get('key_findings', 'N/A')}\n"
                        dossier_text += "\n" + "-"*30 + "\n\n"

                    st.divider()
                    st.download_button(
                        label="Download Clinical Dossier",
                        data=dossier_text,
                        file_name="clinical_research_dossier.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
            else:
                st.error("No data returned from the multi-agent workflow.")
                
        except Exception as e:
            st.error(f"System Halt: {str(e)}")
            st.stop()
