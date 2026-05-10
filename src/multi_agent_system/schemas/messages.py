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

class ScreeningDecision(BaseModel):
    pmid: str
    decision: str
    reason: str

class BatchScreeningResult(BaseModel):
    decisions: List[ScreeningDecision]

class ClinicalExtraction(BaseModel):
    study_design: str = Field(description="Methodology (e.g. RCT)")
    sample_size: str = Field(description="Total N-size")
    statistical_endpoint: str = Field(description="HR, OR, CI, and p-values.")
    key_findings: str = Field(description="1-sentence bottom line.")
    risk_of_bias_flags: list[str] = Field(default_factory=list)
    limitations: str = Field(description="Study limits.")

class ExtractionResult(BaseModel):
    doi: Optional[str] = None
    pmid: Optional[str] = None
    extraction: ClinicalExtraction

class SynthesisReport(BaseModel):
    clinical_consensus: str = Field(description="Lancet-level meta-synthesis.")
    conflicting_findings: List[str] = Field(default_factory=list)
    overall_evidence_quality: str = Field(description="GRADE assessment.")
    clinical_recommendation: str = Field(description="Actionable directives.")

class AgentMessage(BaseModel):
    sender: str
    recipient: str
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    citations: List[Citation] = Field(default_factory=list)
    extractions: List[ExtractionResult] = Field(default_factory=list)
    synthesis: Optional[SynthesisReport] = None

class PICOQuery(BaseModel):
    population: str
    intervention: str
    comparison: Optional[str] = None
    outcome: str
    inclusion_criteria: str = Field(description="Flat string only. No dicts.")
    exclusion_criteria: str = Field(description="Flat string only. No dicts.")
    # THE CRITICAL FIX: Explicitly forbid the AI from adding extra filters
    pubmed_query: str = Field(description="A SIMPLE Boolean string. Example: 'stem cell therapy AND leukemia'. DO NOT add Date, Mesh, or Study Type filters.")
