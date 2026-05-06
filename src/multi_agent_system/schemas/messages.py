"""Structured message models."""

from pydantic import BaseModel, Field


class AgentMessage(BaseModel):
    """A message passed between agents."""

    sender: str
    recipient: str
    content: str
    metadata: dict[str, str] = Field(default_factory=dict)
