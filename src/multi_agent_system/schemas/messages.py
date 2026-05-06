"""Structured message models."""

from pydantic import BaseModel, Field


class Citation(BaseModel):
    """A PubMed citation result."""

    pmid: str
    title: str
    abstract: str = ""
    authors: list[str] = Field(default_factory=list)
    doi: str | None = None


class AgentMessage(BaseModel):
    """A message passed between agents."""

    sender: str
    recipient: str
    content: str
    metadata: dict[str, str] = Field(default_factory=dict)
    citations: list[Citation] = Field(default_factory=list)


class PICOQuery(BaseModel):
    """PICO extraction plus generated PubMed boolean query."""

    population: str
    intervention: str
    comparison: str | None = None
    outcome: str
    pubmed_query: str
