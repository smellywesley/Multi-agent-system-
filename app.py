import streamlit as st
import sys
from pathlib import Path

# Ensuring local modules are discoverable
sys.path.append(str(Path(__file__).parent / "src"))
from multi_agent_system.workflows.review_workflow import ReviewWorkflow

# --- PAGE CONFIG ---
st.set_page_config(page_title="Clinical Intelligence", page_icon="", layout="wide")

# --- APPLE PRO STYLING ---
st.markdown("""
    <style>
    /* 1. Base Typography and True Black Background */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"]  {import streamlit as st
import sys
from pathlib import Path

# Ensuring local modules are discoverable
sys.path.append(str(Path(__file__).parent / "src"))
from multi_agent_system.workflows.review_workflow import ReviewWorkflow

# --- PAGE CONFIG ---
st.set_page_config(page_title="Clinical Intelligence", page_icon="", layout="wide")

# --- APPLE PRO STYLING ---
st.markdown("""
    <style>
    /* 1. Base Typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
        color: #f5f5f7;
    }

    /* 2. THE FLUID AURORA BACKGROUND */
    .stApp {
        background: linear-gradient(-45deg, #000000, #0a1128, #110822, #000000, #050d1a);
        background-size: 400% 400%;
        animation: fluidAurora 25s ease infinite;
        background-attachment: fixed; /* Locks background so content scrolls OVER it */
    }
    
    @keyframes fluidAurora {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* 3. Glassmorphism Top Header (Apple Safari Style) */
    [data-testid="stHeader"] {
        background: rgba(0, 0, 0, 0.4) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Hide Streamlit Default Footer */
    footer {visibility: hidden;}

    /* 4. Premium Text Area */
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

    /* 5. Apple Primary Pill Button */
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

    /* 6. Download Button (Secondary Outline Style) */
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

    /* 7. Glassmorphism Expanders (Evidence Cards) */
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

    /* 8. Typography Polish */
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
        margin-bottom: 5px;
        padding-top: 20px;
    }
    .apple-subtitle {
        font-size: 22px;
        font-weight: 400;
        color: #86868b;
        margin-bottom: 40px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- PREMIUM HEADER ---
st.markdown('<div class="apple-title">Clinical Intelligence.</div>', unsafe_allow_html=True)
st.markdown('<div class="apple-subtitle">Pro-level synthesis. Powered by Groq.</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Architecture Status")
    st.success("Primary Engine: Groq 8B")
    st.info("Failover Engine: SambaNova 70B")

# 1. First, we define the input
question = st.text_area("", placeholder="Enter a clinical research question...", height=120)

# 2. Then, we only run the workflow IF the button is clicked
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

                        with st.expander(f"📄 {study_design} (PMID: {ext.pmid})"):
                            st.markdown(f"**🔗 Source:** [View on PubMed]({pubmed_url}) | **DOI:** {doi_display}")
                            st.markdown(f"**👥 Sample Size:** {data.get('sample_size', 'N/A')}")
                            st.markdown(f"**💡 Key Findings:** {data.get('key_findings', 'N/A')}")
                            st.markdown(f"**⚠️ Limitations:** {data.get('limitations', 'N/A')}")
                            
                            bias = data.get('risk_of_bias_flags', [])
                            if bias:
                                st.markdown(f"**🚩 Risk of Bias:** {', '.join(bias)}")

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
        font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
        background-color: #000000;
        color: #f5f5f7;
    }

    /* 2. Hide Streamlit Branding for an "App" feel */
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* 3. Premium Text Area */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        color: #f5f5f7;
        font-size: 16px;
        padding: 16px;
        transition: all 0.3s ease;
    }
    .stTextArea textarea:focus {
        border-color: #2997ff;
        box-shadow: 0 0 0 4px rgba(41, 151, 255, 0.15);
        background: rgba(255, 255, 255, 0.08);
    }

    /* 4. Apple Primary Pill Button */
    .stButton>button {
        background-color: #f5f5f7;
        color: #1d1d1f;
        border: none;
        border-radius: 980px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.4s cubic-bezier(0.25, 1, 0.5, 1);
        width: 100%;
    }
    .stButton>button:hover {
        transform: scale(1.01);
        background-color: #ffffff;
        box-shadow: 0 4px 20px rgba(255, 255, 255, 0.2);
    }

    /* 5. Download Button (Secondary Outline Style) */
    .stDownloadButton>button {
        background-color: transparent;
        color: #2997ff;
        border: 1px solid #2997ff;
        border-radius: 980px;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stDownloadButton>button:hover {
        background-color: #2997ff;
        color: #ffffff;
        transform: scale(1.01);
    }

    /* 6. Glassmorphism Expanders (Evidence Cards) */
    div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        overflow: hidden;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        transition: transform 0.3s ease, border-color 0.3s ease;
        margin-bottom: 12px;
    }
    div[data-testid="stExpander"]:hover {
        transform: translateY(-2px);
        border-color: rgba(255, 255, 255, 0.2);
    }
    div[data-testid="stExpander"] summary {
        font-weight: 600;
        letter-spacing: 0.3px;
        color: #f5f5f7;
    }

    /* 7. Typography Polish */
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
        margin-bottom: 5px;
        padding-top: 20px;
    }
    .apple-subtitle {
        font-size: 22px;
        font-weight: 400;
        color: #86868b;
        margin-bottom: 40px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- PREMIUM HEADER ---
st.markdown('<div class="apple-title">Clinical Intelligence.</div>', unsafe_allow_html=True)
st.markdown('<div class="apple-subtitle">Pro-level synthesis. Powered by Groq.</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Architecture Status")
    st.success("Primary Engine: Groq 8B")
    st.info("Failover Engine: SambaNova 70B")

# 1. First, we define the input
question = st.text_area("", placeholder="Enter a clinical research question...", height=120)

# 2. Then, we only run the workflow IF the button is clicked
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
                
                # 1. The Meta-Analysis
                if hasattr(result, 'content') and result.content:
                    st.markdown(result.content)
                
                # 2. The Structured Bottom-Line
                if hasattr(result, 'synthesis') and result.synthesis:
                    st.markdown(f"### Consensus\n{result.synthesis.clinical_consensus}")
                    st.markdown(f"### Recommendation\n{result.synthesis.clinical_recommendation}")
                
                # 3. ACADEMIC EVIDENCE CARDS & DOWNLOAD COMPILER
                if hasattr(result, 'extractions') and result.extractions:
                    st.divider()
                    st.header("Clinical Evidence Base")
                    
                    # Initialize the downloadable text dossier
                    dossier_text = "CLINICAL INTELLIGENCE: RESEARCH DOSSIER\n"
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
                            data = {} 

                        study_design = data.get('study_design', 'Unknown Design')
                        pubmed_url = f"https://pubmed.ncbi.nlm.nih.gov/{ext.pmid}/"
                        doi_display = ext.doi if ext.doi else "Not provided"

                        # Build the Glassmorphism UI Card
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
