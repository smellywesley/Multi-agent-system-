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
    sample_size: str = Field(description="The exact total N-size of the study (e.g., 'N=540').")
    
    # THE FIX: Forcing Quantitative Extraction for Meta-Analysis
    statistical_endpoint: str = Field(description="The primary numerical endpoint data. You MUST extract the Hazard Ratio (HR), Odds Ratio (OR), Confidence Intervals (CI), and p-value if present. If no math is provided, write 'Quantitative data not reported'.")
    
    key_findings: str = Field(description="A brutally concise, 1-sentence 'bottom line' summary of the results.")
    risk_of_bias_flags: list[str] = Field(default_factory=list)
    limitations: str = Field(description="A brief note on study limits.")
    
class ExtractionResult(BaseModel):
    """Extraction paired with paper identifiers."""
    doi: Optional[str] = None
    pmid: Optional[str] = None
    extraction: ClinicalExtraction

class SynthesisReport(BaseModel):
    """Final weighted clinical synthesis across extracted studies."""
    clinical_consensus: str = Field(description="A rigorous, high-density academic meta-synthesis. Focus on mechanistic pathways and primary endpoints. NO FILLER. Write for a Lancet-level audience.")
    conflicting_findings: List[str] = Field(default_factory=list, description="Identify methodological or statistical contradictions.")
    overall_evidence_quality: str = Field(description="GRADE criteria assessment (e.g., High, Moderate, Low).")
    clinical_recommendation: str = Field(description="Technical, actionable translational directives based strictly on the data.")

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
    
    # THE FIX: Force the AI to write a broad search that actually yields results
    pubmed_query: str = Field(description="A BROAD and INCLUSIVE PubMed Boolean search string. ONLY combine the Population and Intervention using AND. DO NOT include the Outcome or Comparison in the search string, as this will result in 0 papers found.")

"""Structured message models."""

import warnings
from typing import Any, List, Dict, Optional
from pydantic import BaseModel, Field

warnings.filterwarnings("ignore", message=".*any.*is not a Python type.*")

class Citation(BaseModel):
    source: str
    pmid: Optional[str] = None
    title: str
    abstract: str = ""
    authors: List[str] = Field(default_factory=list)
    doi: Optional[str] = None

class PICOQuery(BaseModel):
    population: str = Field(description="The patient population or problem.")
    intervention: str = Field(description="The primary intervention or exposure.")
    comparison: str | None = Field(default=None, description="The comparison group, if any.")
    outcome: str = Field(description="The clinical outcome being measured.")
    
    # THE FIX: Force the AI to output a flat string, completely banning dictionaries/nested JSON
    inclusion_criteria: str = Field(description="A single flat string of text. DO NOT use nested JSON, dictionaries, or key-value pairs. State the rules for inclusion (e.g., 'Human subjects, RCTs only').")
    exclusion_criteria: str = Field(description="A single flat string of text. DO NOT use nested JSON, dictionaries, or key-value pairs. State the rules for exclusion.")
    
    pubmed_query: str = Field(description="A BROAD and INCLUSIVE PubMed Boolean search string. ONLY combine Population and Intervention using AND. Do NOT make it too restrictive.")
# NEW: The Screening Blueprint
class ScreeningDecision(BaseModel):
    pmid: str = Field(description="The PubMed ID of the paper.")
    decision: str = Field(description="MUST be strictly 'INCLUDE' or 'EXCLUDE'.")
    reason: str = Field(description="A brief 1-sentence justification based on the inclusion/exclusion criteria.")

class BatchScreeningResult(BaseModel):
    decisions: List[ScreeningDecision]

class ClinicalExtraction(BaseModel):
    study_design: str = Field(description="The methodology used (e.g., Double-blind RCT).")
    sample_size: str | int | None = Field(default=None, description="The number of patients.")
    key_findings: str = Field(description="A brutally concise, 1-sentence 'bottom line' summary of the results. Translate dense academic jargon into plain English.")
    risk_of_bias_flags: list[str] = Field(default_factory=list)
    limitations: str = Field(description="A brief note on study limits.")

class ExtractionResult(BaseModel):
    doi: Optional[str] = None
    pmid: Optional[str] = None
    extraction: ClinicalExtraction

class BatchExtractionWrapper(BaseModel):
    papers: List[ExtractionResult]

class SynthesisReport(BaseModel):
    clinical_consensus: str = Field(description="A rigorous, high-density academic meta-synthesis. Focus on mechanistic pathways and primary endpoints. NO FILLER. Write for a Lancet-level audience.")
    conflicting_findings: List[str] = Field(default_factory=list, description="Identify methodological or statistical contradictions.")
    overall_evidence_quality: str = Field(description="GRADE criteria assessment (e.g., High, Moderate, Low).")
    clinical_recommendation: str = Field(description="Technical, actionable translational directives based strictly on the data.")

class AgentMessage(BaseModel):
    sender: str
    recipient: str
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    citations: List[Citation] = Field(default_factory=list)
    extractions: List[ExtractionResult] = Field(default_factory=list)
    synthesis: Optional[SynthesisReport] = None
