"""Structured message models."""

import warnings
from typing import Any, List, Dict, Optional
from pydantic import BaseModel, Field

# Silence the Pydantic noise in the logs
warnings.filterwarnings("ignore", message=".*any.*is not a Python type.*")

class Citation(BaseModel):
    """A literature citation result."""
    source: str
    pmid: Optional[str] = None
    title: str
    abstract: str = ""
    authors: List[str] = Field(default_factory=list)
    doi: Optional[str] = None

class ClinicalExtraction(BaseModel):
    study_design: str = Field(description="The methodology used (e.g., Double-blind RCT).")
    sample_size: str | int | None = Field(default=None, description="The number of patients.")
    
    # THE FIX: Aggressively force the AI to simplify the text into a bottom line
    key_findings: str = Field(description="A brutally concise, 1-sentence 'bottom line' summary of the results. Translate dense academic jargon into plain English. NO statistics, NO raw data points. Just the core takeaway.")
    
    risk_of_bias_flags: list[str] = Field(default_factory=list)
    limitations: str = Field(description="A brief note on study limits.")

class ExtractionResult(BaseModel):
    """Extraction paired with paper identifiers."""
    doi: Optional[str] = None
    pmid: Optional[str] = None
    extraction: ClinicalExtraction

class SynthesisReport(BaseModel):
    """Final weighted clinical synthesis across extracted studies."""
    clinical_consensus: str = Field(description="A rigorous, high-density academic meta-synthesis of the provided literature. Focus exclusively on mechanistic pathways, statistical outcome trends, and primary endpoints. DO NOT use introductory filler like 'X has emerged as a powerful tool'. Write exactly like a principal investigator publishing a systematic review in The Lancet or NEJM. Use precise medical terminology.")
    conflicting_findings: List[str] = Field(default_factory=list, description="Identify specific methodological, statistical, or cohort-based contradictions between the provided studies.")
    overall_evidence_quality: str = Field(description="GRADE criteria assessment of the evidence (e.g., High, Moderate, Low) based strictly on study designs (e.g., RCTs vs. Observational) and extracted limitations.")
    clinical_recommendation: str = Field(description="Translational directives for clinical practice or highly specific future trial designs. Must be actionable, technical, and strictly bound by the extracted evidence.")
class AgentMessage(BaseModel):
    """A message passed between agents."""
    sender: str
    recipient: str
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    citations: List[Citation] = Field(default_factory=list)
    extractions: List[ExtractionResult] = Field(default_factory=list)
    synthesis: Optional[SynthesisReport] = None

class PICOQuery(BaseModel):
    population: str = Field(description="The patient population or problem.")
    intervention: str = Field(description="The primary intervention or exposure.")
    comparison: str | None = Field(default=None, description="The comparison group, if any.")
    outcome: str = Field(description="The clinical outcome being measured.")
    
    # THE FIX: Ensuring the Orchestrator doesn't crash when asking for the search string
    pubmed_query: str = Field(description="A highly optimized PubMed Boolean search string using MeSH terms and synonyms.")
