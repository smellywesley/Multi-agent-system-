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
    clinical_consensus: str
    conflicting_findings: List[str] = Field(default_factory=list)
    overall_evidence_quality: str
    clinical_recommendation: str

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
