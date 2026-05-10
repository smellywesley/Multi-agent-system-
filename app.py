import streamlit as st
import sys
from pathlib import Path

# Ensuring local modules are discoverable
sys.path.append(str(Path(__file__).parent / "src"))
from multi_agent_system.workflows.review_workflow import ReviewWorkflow

# --- PAGE CONFIG ---
st.set_page_config(page_title="Clinical Intelligence", page_icon="", layout="wide")

# --- APPLE PRO STYLING & 3D DNA HELIX ---
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

    /* THE REVOLVING 3D DNA */
    .dna-container {
        position: fixed;
        right: 8%;
        top: 50%;
        transform: translateY(-50%) scale(1.3);
        height: 500px;
        width: 120px;
        z-index: 0;
        pointer-events: none;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        perspective: 1000px;
    }
    .base-pair {
        position: relative;
        width: 100%;
        height: 2px;
        transform-style: preserve-3d;
        animation: spinDNA 4s linear infinite;
    }
    .dot {
        position: absolute;
        top: -4px;
        width: 10px;
        height: 10px;
        border-radius: 50%;
    }
    .dot.left { left: 0; background: #2997ff; box-shadow: 0 0 15px #2997ff; }
    .dot.right { right: 0; background: #a1a1a6; box-shadow: 0 0 15px #a1a1a6; }
    .line {
        position: absolute;
        top: 0;
        left: 5px;
        right: 5px;
        height: 2px;
        background: rgba(255, 255, 255, 0.15);
    }
    @keyframes spinDNA {
        0% { transform: rotateY(0deg); }
        100% { transform: rotateY(360deg); }
    }

    /* SAFE STREAMLIT NATIVE WRAPPER - Replaces the broken HTML wrapper */
    [data-testid="block-container"] {
        max-width: 75% !important;
        padding-left: 5% !important;
        padding-right: 5% !important;
        z-index: 1;
    }

    [data-testid="stHeader"] {
        background: rgba(0, 0, 0, 0.4) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    footer {visibility: hidden;}

    /* INPUT BOX FIX - Ensuring it stays visible and clickable */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 16px;
        color: #f5f5f7 !important;
        font-size: 16px;
        padding: 16px;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        z-index: 10;
        position: relative;
    }
    .stTextArea textarea:focus {
        border-color: #2997ff !important;
        box-shadow: 0 0 0 4px rgba(41, 151, 255, 0.15) !important;
        background: rgba(255, 255, 255, 0.1) !important;
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
        z-index: 10;
        position: relative;
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
        text-align: center;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# 1. INJECT THE CSS 3D DNA 
dna_html = '<div class="dna-container">'
for i in range(25):
    delay = i * -0.15
    dna_html += f'<div class="base-pair" style="animation-delay: {delay}s;"><div class="line" style="animation-delay: {delay}s;"></div><div class="dot left" style="animation-delay: {delay}s;"></div><div class="dot right" style="animation-delay: {delay}s;"></div></div>'
dna_html += '</div>'
st.markdown(dna_html, unsafe_allow_html=True)

# 2. NO MORE RAW HTML WRAPPERS (Deleted the broken content-wrapper div entirely)

st.markdown('<div class="apple-title">Clinical Intelligence</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Architecture Status")
    st.success("Primary Engine: Groq 8B")
    st.info("Failover Engine: SambaNova 70B")

# The Text Box is now safely rendered by Streamlit natively
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
            
            if result:
                st.divider()
                st.header("Systematic Meta-Synthesis")
                
                if hasattr(result, 'synthesis') and result.synthesis:
                    st.markdown(f"### Mechanistic & Clinical Consensus\n{result.synthesis.clinical_consensus}")
                    st.markdown(f"### Translational Directives\n{result.synthesis.clinical_recommendation}")
                    
                    if hasattr(result.synthesis, 'overall_evidence_quality'):
                        st.markdown(f"**GRADE Evidence Assessment:** {result.synthesis.overall_evidence_quality}")
                        
                    if hasattr(result.synthesis, 'conflicting_findings') and result.synthesis.conflicting_findings:
                        st.markdown("**Methodological & Statistical Contradictions:**")
                        for conflict in result.synthesis.conflicting_findings:
                            st.markdown(f"- {conflict}")
                
                if hasattr(result, 'extractions') and result.extractions:
                    st.divider()
                    
                    # PRISMA TRACKING METRICS
                    st.header("PRISMA Screening & Evidence Matrix")
                    
                    # Calculate PRISMA stats if available
                    if hasattr(result, 'metadata') and 'screening_decisions' in result.metadata:
                        decisions = result.metadata['screening_decisions']
                        total_screened = len(decisions)
                        total_included = len([d for d in decisions if d['decision'].upper() == "INCLUDE"])
                        total_excluded = total_screened - total_included
                        
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Papers Screened", total_screened)
                        col2.metric("Excluded (Failed Criteria)", total_excluded)
                        col3.metric("Included in Synthesis", total_included)
                    
                    # BUILD THE QUANTITATIVE DATA TABLE
                    st.markdown("### Extracted Quantitative Data")
                    
                    # Prepare data for a clean table layout
                    table_data = []
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

                        study_design = data.get('study_design', 'Unknown')
                        n_size = data.get('sample_size', 'N/A')
                        stats = data.get('statistical_endpoint', 'N/A')
                        findings = data.get('key_findings', 'N/A')
                        pubmed_url = f"https://pubmed.ncbi.nlm.nih.gov/{ext.pmid}/"

                        # Append row for the UI table
                        table_data.append({
                            "PMID": ext.pmid,
                            "Design": study_design,
                            "N-Size": n_size,
                            "Statistical Endpoint": stats,
                            "Findings": findings
                        })

                        # Compile text for the downloadable dossier
                        dossier_text += f"PMID: {ext.pmid}\n"
                        dossier_text += f"Design: {study_design} (N={n_size})\n"
                        dossier_text += f"Statistics: {stats}\n"
                        dossier_text += f"Bottom Line: {findings}\n"
                        dossier_text += "-"*30 + "\n\n"

                    # Render the DataFrame natively in Streamlit
                    st.dataframe(
                        table_data, 
                        column_config={
                            "PMID": st.column_config.TextColumn("PMID", width="small"),
                            "Design": st.column_config.TextColumn("Design", width="medium"),
                            "N-Size": st.column_config.TextColumn("N-Size", width="small"),
                            "Statistical Endpoint": st.column_config.TextColumn("Statistics", width="large"),
                            "Findings": st.column_config.TextColumn("Key Findings", width="large"),
                        },
                        hide_index=True,
                        use_container_width=True
                    )

                    st.divider()
                    st.download_button(
                        label="Download Full PRISMA Dossier",
                        data=dossier_text,
                        file_name="prisma_clinical_dossier.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
            else:
                st.error("No data returned from the multi-agent workflow.")
                
        except Exception as e:
            st.error(f"System Halt: {str(e)}")
            st.stop()

# Close the wrapper div safely
st.markdown('</div>', unsafe_allow_html=True)
