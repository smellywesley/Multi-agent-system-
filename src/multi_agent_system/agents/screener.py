"""Screening Agent for PRISMA-compliant study selection."""

from typing import List, Dict, Any
from .base import BaseAgent
from ..schemas.messages import AgentMessage, Citation, BatchScreeningResult
from ..tools.llm_client import LLMClient

class ScreenerAgent(BaseAgent):
    """Filters retrieved literature based on strict inclusion/exclusion criteria."""
    
    def __init__(self, name: str = "Screener"):
        super().__init__(name=name)
        self.llm_client = LLMClient()

    def process(self, message: AgentMessage) -> AgentMessage:
        self.logger.info("Initializing PRISMA screening protocol...")
        
        citations = message.citations
        pico_dict = message.metadata.get("pico_query", {})
        
        if not citations:
            return self._create_empty_response(message, "No citations provided for screening.")

        # Formatting the abstracts for the AI to read
        papers_text = ""
        for i, c in enumerate(citations):
            papers_text += f"\n--- PAPER {i+1} ---\nPMID: {c.pmid}\nTitle: {c.title}\nAbstract: {c.abstract}\n"

        prompt = f"""
        You are a strict Principal Investigator conducting a systematic review.
        You must screen the following papers against the criteria below.

        INCLUSION CRITERIA:
        {pico_dict.get('inclusion_criteria', 'Must be highly relevant to the clinical question.')}
        
        EXCLUSION CRITERIA:
        {pico_dict.get('exclusion_criteria', 'Exclude animal studies, in vitro studies, and irrelevant papers.')}

        PAPERS TO SCREEN:
        {papers_text}

        Evaluate every single paper. If it violates ANY exclusion criteria, you MUST mark it "EXCLUDE". 
        Only mark "INCLUDE" if it meets the inclusion criteria and passes all exclusion rules.
        """

        try:
            # Using the fast 8B model to churn through the abstracts rapidly
            screening_result = self.llm_client.generate_structured(
                prompt=prompt,
                schema=BatchScreeningResult,
                use_heavy_model=False 
            )
            
            # Filter the actual citations based on the AI's decisions
            included_pmids = [d.pmid for d in screening_result.decisions if d.decision.upper() == "INCLUDE"]
            filtered_citations = [c for c in citations if c.pmid in included_pmids]
            
            self.logger.info(f"Screening complete: {len(filtered_citations)}/{len(citations)} papers included.")

            return AgentMessage(
                sender=self.name,
                recipient=message.sender,
                content=f"Screened {len(citations)} papers. Included {len(filtered_citations)}.",
                citations=filtered_citations, # Only passing the surviving papers!
                metadata={
                    **message.metadata,
                    "screening_decisions": [d.model_dump() for d in screening_result.decisions] # Saving reasons for PRISMA
                }
            )

        except Exception as e:
            self.logger.error(f"Screening failed: {e}")
            return self._create_empty_response(message, f"Screening system failure: {str(e)}")

    def _create_empty_response(self, message: AgentMessage, error_text: str) -> AgentMessage:
        return AgentMessage(
            sender=self.name,
            recipient=message.sender,
            content=error_text,
            citations=[],
            metadata=message.metadata
        )
