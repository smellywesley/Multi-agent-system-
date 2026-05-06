"""Review workflow using orchestrator agent."""

from multi_agent_system.agents.orchestrator import OrchestratorAgent
from multi_agent_system.schemas.messages import AgentMessage


class ReviewWorkflow:
    """Runs end-to-end review flow via orchestrator."""

    def __init__(self, orchestrator: OrchestratorAgent | None = None) -> None:
        self.orchestrator = orchestrator or OrchestratorAgent()

    def run(self, task: str) -> AgentMessage:
        request = AgentMessage(sender="user", recipient="orchestrator", content=task)
        return self.orchestrator.handle(request)
