"""Reviewer specialist agent."""

import json

from multi_agent_system.agents.base import BaseAgent
from multi_agent_system.config import get_settings
from multi_agent_system.schemas.messages import AgentMessage, SynthesisReport
from multi_agent_system.tools.llm_client import LLMClient


class ReviewerAgent(BaseAgent):
    """Synthesizes clinical extractions into a final consensus report."""

    def __init__(self, llm_client: LLMClient | None = None) -> None:
        super().__init__(name="reviewer")
        settings = get_settings()
        self.llm_client = llm_client or LLMClient(settings=settings)

    def handle(self, message: AgentMessage) -> AgentMessage:
        serialized_extractions = [result.model_dump(mode="json") for result in message.extractions]
        prompt = (
            "Analyze these clinical extractions. Weigh randomized controlled trials and "
            "large sample sizes heavier than small observational studies. Identify the "
            "consensus, list any explicit contradictions, assess the overall quality of the "
            "evidence, and provide a final clinical recommendation.\n\n"
            f"Extractions JSON:\n{json.dumps(serialized_extractions, indent=2)}"
        )

        synthesis = self.llm_client.generate_structured(
            prompt=prompt,
            schema=SynthesisReport,
            use_heavy_model=True  # <--- THIS ACTIVATES THE 70B BRAIN
        )

        content = self._to_markdown_summary(synthesis)
        return AgentMessage(
            sender=self.name,
            recipient=message.sender,
            content=content,
            metadata=message.metadata,
            citations=message.citations,
            extractions=message.extractions,
            synthesis=synthesis,
        )

    def _to_markdown_summary(self, synthesis: SynthesisReport) -> str:
        contradictions = "\n".join(
            f"- {finding}" for finding in synthesis.conflicting_findings
        ) or "- None reported"
        return (
            "## Clinical Synthesis Report\n\n"
            f"**Clinical consensus:** {synthesis.clinical_consensus}\n\n"
            f"**Overall evidence quality:** {synthesis.overall_evidence_quality}\n\n"
            "**Conflicting findings:**\n"
            f"{contradictions}\n\n"
            f"**Clinical recommendation:** {synthesis.clinical_recommendation}"
        )
