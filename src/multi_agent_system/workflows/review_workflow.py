"""Clinical literature review workflow."""

from typing import Optional
from .base import BaseWorkflow
from ..agents.orchestrator import OrchestratorAgent
from ..agents.researcher import ResearcherAgent
from ..agents.screener import ScreenerAgent
from ..agents.extractor import ExtractorAgent
from ..agents.reviewer import ReviewerAgent
from ..schemas.messages import AgentMessage

class ReviewWorkflow(BaseWorkflow):
    """Orchestrates the multi-agent clinical review process."""

    def __init__(self):
        super().__init__(name="ReviewWorkflow")
        self.orchestrator = OrchestratorAgent()
        self.researcher = ResearcherAgent()
        self.screener = ScreenerAgent()
        self.extractor = ExtractorAgent()
        self.reviewer = ReviewerAgent()

    def run(self, task: str) -> Optional[AgentMessage]:
        self.logger.info(f"Starting review workflow for task: {task}")

        # 1. ORCHESTRATION
        init_msg = AgentMessage(
            sender="User",
            recipient=self.orchestrator.name,
            content=task
        )
        orch_result = self.orchestrator.handle(init_msg)
        if not orch_result.metadata.get("pico_query"):
            raise ValueError(f"Orchestrator Failed: {orch_result.content}")

        # 2. RESEARCH
        research_result = self.researcher.handle(orch_result)
        if not research_result.citations:
            raise ValueError(f"Researcher Failed: {research_result.content}")

        # 3. SCREENING
        screen_result = self.screener.handle(research_result)
        if not screen_result.citations:
            raise ValueError(f"Screener Failed (Or Rejected All Papers): {screen_result.content}")

        # 4. EXTRACTION
        extraction_result = self.extractor.handle(screen_result)
        if not extraction_result.extractions:
            raise ValueError(f"Extractor Failed: {extraction_result.content}")

        # 5. SYNTHESIS
        final_result = self.reviewer.handle(extraction_result)
        
        # THE FIX: Unbreakable string check instead of a fragile Pydantic object check
        if final_result.content != "Synthesis complete.":
            raise ValueError(f"Reviewer Failed: {final_result.content}")

        return final_result
