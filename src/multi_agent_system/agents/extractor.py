"""Extraction specialist agent."""

from multi_agent_system.agents.base import BaseAgent
from multi_agent_system.schemas.messages import AgentMessage


class ExtractorAgent(BaseAgent):
    """Extracts key facts from a message."""

    def __init__(self) -> None:
        super().__init__(name="extractor")

    def handle(self, message: AgentMessage) -> AgentMessage:
        return AgentMessage(
            sender=self.name,
            recipient=message.sender,
            content=f"Extracted facts: {message.content}",
        )
