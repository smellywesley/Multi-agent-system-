from multi_agent_system.agents.orchestrator import OrchestratorAgent
from multi_agent_system.schemas.messages import AgentMessage


def test_orchestrator_pipeline() -> None:
    orchestrator = OrchestratorAgent()
    msg = AgentMessage(sender="user", recipient="orchestrator", content="Draft summary")

    result = orchestrator.handle(msg)

    assert result.sender == "reviewer"
    assert "Review outcome:" in result.content
