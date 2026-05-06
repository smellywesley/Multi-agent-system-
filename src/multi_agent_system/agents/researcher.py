"""Research specialist agent."""

from multi_agent_system.agents.base import BaseAgent
from multi_agent_system.schemas.messages import AgentMessage


class ResearcherAgent(BaseAgent):
    """Produces preliminary research notes for a task."""

    def __init__(self) -> None:
        super().__init__(name="researcher")

    def handle(self, message: AgentMessage) -> AgentMessage:
        return AgentMessage(
            sender=self.name,
            recipient=message.sender,
            content=f"Research notes: {message.content}",
        )
