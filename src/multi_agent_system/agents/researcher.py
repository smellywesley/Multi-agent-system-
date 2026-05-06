"""Research specialist agent."""

from multi_agent_system.agents.base import BaseAgent
from multi_agent_system.schemas.messages import AgentMessage
from multi_agent_system.tools.pubmed_client import PubMedClient


class ResearcherAgent(BaseAgent):
    """Executes PubMed searches and returns structured citations."""

    def __init__(self, pubmed_client: PubMedClient | None = None) -> None:
        super().__init__(name="researcher")
        self.pubmed_client = pubmed_client or PubMedClient()

    def handle(self, message: AgentMessage) -> AgentMessage:
        citations = self.pubmed_client.search(query=message.content, max_results=20)
        return AgentMessage(
            sender=self.name,
            recipient=message.sender,
            content=f"Retrieved {len(citations)} PubMed citations.",
            metadata={"query": message.content},
            citations=citations,
        )
