"""Extraction specialist agent."""

import time

from multi_agent_system.agents.base import BaseAgent
from multi_agent_system.config import get_settings
from multi_agent_system.schemas.messages import AgentMessage, ClinicalExtraction, ExtractionResult
from multi_agent_system.tools.llm_client import LLMClient


class ExtractorAgent(BaseAgent):
    """Extracts structured clinical findings from citation abstracts."""

    def __init__(self, llm_client: LLMClient | None = None) -> None:
        super().__init__(name="extractor")
        settings = get_settings()
        self.llm_client = llm_client or LLMClient(settings=settings)

    def handle(self, message: AgentMessage) -> AgentMessage:
        extractions: list[ExtractionResult] = []

        for citation in message.citations:
            if not citation.abstract.strip():
                continue
            prompt = (
                "Extract structured clinical details from this biomedical abstract. "
                "Return study design, sample size, key findings, "
                "risk-of-bias flags, and limitations.\n\n"
                f"Title: {citation.title}\n"
                f"Abstract: {citation.abstract}"
            )
            extraction = self.llm_client.generate_structured(
                prompt=prompt,
                schema=ClinicalExtraction,
            )
            extractions.append(
                ExtractionResult(doi=citation.doi, pmid=citation.pmid, extraction=extraction)
            )
            time.sleep(2)

        return AgentMessage(
            sender=self.name,
            recipient=message.sender,
            content=f"Extracted clinical structure from {len(extractions)} citations.",
            metadata=message.metadata,
            citations=message.citations,
            extractions=extractions,
        )
