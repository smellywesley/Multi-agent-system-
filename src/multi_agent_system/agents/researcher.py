"""Research specialist agent."""

from multi_agent_system.agents.base import BaseAgent
from multi_agent_system.schemas.messages import AgentMessage, Citation
from multi_agent_system.tools.pubmed_client import PubMedClient
from multi_agent_system.tools.semantic_scholar_client import SemanticScholarClient


class ResearcherAgent(BaseAgent):
    """Executes federated search and returns deduplicated citations."""

    def __init__(
        self,
        pubmed_client: PubMedClient | None = None,
        semantic_scholar_client: SemanticScholarClient | None = None,
    ) -> None:
        super().__init__(name="researcher")
        self.pubmed_client = pubmed_client or PubMedClient()
        self.semantic_scholar_client = semantic_scholar_client or SemanticScholarClient()

    def handle(self, message: AgentMessage) -> AgentMessage:
        pubmed = self.pubmed_client.search(query=message.content, max_results=20)
        semantic_scholar = self.semantic_scholar_client.search(
            query=message.content,
            max_results=20,
        )
        citations = self._deduplicate(pubmed + semantic_scholar)

        return AgentMessage(
            sender=self.name,
            recipient=message.sender,
            content=f"Retrieved {len(citations)} federated citations.",
            metadata={"query": message.content},
            citations=citations,
        )

    def _deduplicate(self, citations: list[Citation]) -> list[Citation]:
        by_doi: dict[str, Citation] = {}
        no_doi: list[Citation] = []

        for citation in citations:
            if citation.doi:
                key = citation.doi.lower().strip()
                by_doi.setdefault(key, citation)
            else:
                no_doi.append(citation)

        return list(by_doi.values()) + no_doi
