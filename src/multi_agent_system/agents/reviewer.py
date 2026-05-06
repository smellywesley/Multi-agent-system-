"""Reviewer specialist agent."""

from multi_agent_system.agents.base import BaseAgent
from multi_agent_system.schemas.messages import AgentMessage


class ReviewerAgent(BaseAgent):
    """Reviews combined specialist outputs."""

    def __init__(self) -> None:
        super().__init__(name="reviewer")

    def handle(self, message: AgentMessage) -> AgentMessage:
        return AgentMessage(
            sender=self.name,
            recipient=message.sender,
            content=f"Review outcome: {message.content}",
        )
