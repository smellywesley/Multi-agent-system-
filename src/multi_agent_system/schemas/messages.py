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
    """Structured clinical extraction from abstract text."""
    study_design: str
    sample_size: Optional[int] = None
    key_findings: str
    risk_of_bias_flags: List[str] = Field(default_factory=list)
    limitations: str

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

from pydantic import BaseModel, Field

class PICOQuery(BaseModel):
    population: str = Field(description="The patient population or problem.")
    intervention: str = Field(description="The primary intervention or exposure.")
    comparison: str | None = Field(default=None, description="The comparison group, if any.")
    outcome: str = Field(description="The clinical outcome being measured.")
    pubmed_query: str = Field(description="A highly optimized PubMed Boolean search string using MeSH terms and synonyms.")
