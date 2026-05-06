"""Streamlit portal for biomedical research workflow."""

import json

import streamlit as st

from multi_agent_system.config import get_settings
from multi_agent_system.workflows.review_workflow import ReviewWorkflow

st.set_page_config(page_title="Biomedical Research Intelligence", layout="wide")

settings = get_settings()

st.title("Biomedical Research Intelligence")

with st.sidebar:
    st.header("System Status")
    st.caption(f"Current provider: `{settings.llm_provider}`")
    sambanova_ok = settings.sambanova_api_key not in {"", "replace_me"}
    gemini_ok = settings.gemini_api_key not in {"", "replace_me"}
    st.success("SambaNova (Primary): Ready" if sambanova_ok else "SambaNova (Primary): Missing key")
    st.success("Gemini (Failover): Ready" if gemini_ok else "Gemini (Failover): Missing key")
    st.info("PHI warning: do not submit identifiable patient data.")

question = st.text_area(
    "Biomedical Research Question",
    height=180,
    placeholder=(
        "e.g., In adults with treatment-resistant depression, does ketamine "
        "improve remission compared with placebo?"
    ),
)

if st.button("Run Research", type="primary"):
    if not question.strip():
        st.warning("Please enter a research question before running.")
    else:
        workflow = ReviewWorkflow()
        with st.status("Starting workflow...", expanded=True) as status:
            st.write("Orchestrating...")
            st.write("Searching PubMed/Semantic Scholar...")
            st.write("Extracting Clinical Data...")
            st.write("Synthesizing Report...")
            result = workflow.run(task=question)
            status.update(label="Research complete", state="complete")

        st.subheader("Clinical Synthesis Report")
        if result.synthesis:
            synthesis = result.synthesis
            st.markdown(
                "\n".join(
                    [
                        "## Clinical Synthesis Report",
                        f"**Clinical consensus:** {synthesis.clinical_consensus}",
                        f"**Overall evidence quality:** {synthesis.overall_evidence_quality}",
                        "**Conflicting findings:**",
                        *[
                            f"- {item}"
                            for item in (synthesis.conflicting_findings or ["None reported"])
                        ],
                        f"**Clinical recommendation:** {synthesis.clinical_recommendation}",
                    ]
                )
            )
        else:
            st.markdown(result.content)

        with st.expander("Source Citations"):
            if result.citations:
                for citation in result.citations:
                    st.markdown(
                        f"- **{citation.title}**  \\n"
                        f"DOI: `{citation.doi or 'N/A'}` | Source: `{citation.source}`"
                    )
            else:
                st.write("No citations returned.")

        with st.expander("Raw Clinical Extractions"):
            st.code(json.dumps([item.model_dump() for item in result.extractions], indent=2))

        report_text = result.content
        st.download_button(
            "Download Report",
            data=report_text,
            file_name="clinical_synthesis_report.md",
            mime="text/markdown",
        )
