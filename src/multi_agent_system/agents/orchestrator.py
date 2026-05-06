"""Orchestrator agent coordinating specialists."""

from multi_agent_system.agents.base import BaseAgent
from multi_agent_system.agents.extractor import ExtractorAgent
from multi_agent_system.agents.researcher import ResearcherAgent
from multi_agent_system.agents.reviewer import ReviewerAgent
from multi_agent_system.schemas.messages import AgentMessage


class OrchestratorAgent(BaseAgent):
    """Coordinates specialist agents and aggregates outputs."""

    def __init__(self) -> None:
        super().__init__(name="orchestrator")
        self.researcher = ResearcherAgent()
        self.extractor = ExtractorAgent()
        self.reviewer = ReviewerAgent()

    def handle(self, message: AgentMessage) -> AgentMessage:
        research = self.researcher.handle(message)
        extracted = self.extractor.handle(research)
        return self.reviewer.handle(extracted)
