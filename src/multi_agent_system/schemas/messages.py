"""Structured message models."""

from pydantic import BaseModel, Field


class Citation(BaseModel):
    """A literature citation result."""

    source: str
    pmid: str | None = None
    title: str
    abstract: str = ""
    authors: list[str] = Field(default_factory=list)
    doi: str | None = None


class ClinicalExtraction(BaseModel):
    """Structured clinical extraction from abstract text."""

    study_design: str
    sample_size: int | None
    key_findings: str
    risk_of_bias_flags: list[str] = Field(default_factory=list)
    limitations: str


class ExtractionResult(BaseModel):
    """Extraction paired with paper identifiers."""

    doi: str | None = None
    pmid: str | None = None
    extraction: ClinicalExtraction


class AgentMessage(BaseModel):
    """A message passed between agents."""

    sender: str
    recipient: str
    content: str
    metadata: dict[str, str] = Field(default_factory=dict)
    citations: list[Citation] = Field(default_factory=list)
    extractions: list[ExtractionResult] = Field(default_factory=list)


class PICOQuery(BaseModel):
    """PICO extraction plus generated PubMed boolean query."""

    population: str
    intervention: str
    comparison: str | None = None
    outcome: str
    pubmed_query: str
