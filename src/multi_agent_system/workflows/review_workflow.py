"""Clinical literature review workflow."""

from typing import Optional
from .base import BaseWorkflow
from ..agents.orchestrator import OrchestratorAgent
from ..agents.researcher import ResearcherAgent
from ..agents.screener import ScreenerAgent  # <-- THE BOUNCER IS IMPORTED
from ..agents.extractor import ExtractorAgent
from ..agents.reviewer import ReviewerAgent
from ..schemas.messages import AgentMessage

class ReviewWorkflow(BaseWorkflow):
    """Orchestrates the multi-agent clinical review process."""

    def __init__(self):
        super().__init__(name="ReviewWorkflow")
        # Instantiate all 5 agents
        self.orchestrator = OrchestratorAgent()
        self.researcher = ResearcherAgent()
        self.screener = ScreenerAgent()      # <-- THE BOUNCER IS HIRED
        self.extractor = ExtractorAgent()
        self.reviewer = ReviewerAgent()

    def run(self, task: str) -> Optional[AgentMessage]:
        self.logger.info(f"Starting review workflow for task: {task}")

        try:
            # 1. ORCHESTRATION: Break down the query and define PRISMA rules
            init_msg = AgentMessage(
                sender="User",
                recipient=self.orchestrator.name,
                content=task
            )
            orch_result = self.orchestrator.process(init_msg)
            if not orch_result.metadata.get("pico_query"):
                self.logger.error("Orchestrator failed to generate PICO query.")
                return None

            # 2. RESEARCH: Fetch papers from PubMed
            research_result = self.researcher.process(orch_result)
            if not research_result.citations:
                self.logger.warning("Researcher found no citations.")
                return research_result

            # 3. SCREENING: The Bouncer kicks out irrelevant/low-quality papers
            screen_result = self.screener.process(research_result)
            if not screen_result.citations:
                self.logger.warning("Screener rejected ALL papers. None passed the PRISMA criteria.")
                # We return the screen_result here so the UI can at least tell the user why they failed
                return screen_result

            # 4. EXTRACTION: Read the SURVIVING papers and pull the data
            extraction_result = self.extractor.process(screen_result)
            if not extraction_result.extractions:
                self.logger.warning("Extractor failed to pull data from the screened papers.")
                return extraction_result

            # 5. SYNTHESIS: The 70B Model writes the final academic consensus
            final_result = self.reviewer.process(extraction_result)
            return final_result

        except Exception as e:
            self.logger.error(f"Workflow failed: {e}")
            return None
