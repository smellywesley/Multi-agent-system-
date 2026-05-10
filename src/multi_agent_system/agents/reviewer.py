"""Reviewer Agent for synthesizing clinical data."""

from .base import BaseAgent
from ..schemas.messages import AgentMessage, SynthesisReport
from ..tools.llm_client import LLMClient

class ReviewerAgent(BaseAgent):
    """Synthesizes extracted clinical evidence into a final report."""
    
    def __init__(self, name="Reviewer"):
        super().__init__(name=name)
        self.llm_client = LLMClient()

    def handle(self, message: AgentMessage) -> AgentMessage:
        self.logger.info("Synthesizing clinical evidence...")
        
        if not message.extractions:
            return self._create_empty_response(message, "No extractions provided.")

        # Format the extracted data for the 70B model to read
        evidence_text = ""
        for ext in message.extractions:
            data = ext.extraction
            # Safety check depending on how the data was returned
            study_design = getattr(data, 'study_design', data.get('study_design', 'Unknown') if isinstance(data, dict) else 'Unknown')
            findings = getattr(data, 'key_findings', data.get('key_findings', 'Unknown') if isinstance(data, dict) else 'Unknown')
            evidence_text += f"PMID: {ext.pmid}\nDesign: {study_design}\nFindings: {findings}\n\n"

        prompt = f"""
        You are a Lead Clinical Researcher. Synthesize the following study data into a rigorous academic report.
        
        EVIDENCE:
        {evidence_text}
        """

        try:
            # THE FIX: Force the 70B model to output the strict SynthesisReport JSON
            synthesis_obj = self.llm_client.generate_structured(
                prompt=prompt,
                schema=SynthesisReport,
                use_heavy_model=True
            )
            
            return AgentMessage(
                sender=self.name,
                recipient=message.sender,
                content="Synthesis complete.",
                citations=message.citations,
                extractions=message.extractions,
                synthesis=synthesis_obj, # PACKAGED CORRECTLY!
                metadata=message.metadata
            )
        except Exception as e:
            return self._create_empty_response(message, f"Synthesis failed: {str(e)}")

    def _create_empty_response(self, message: AgentMessage, error_text: str) -> AgentMessage:
        return AgentMessage(
            sender=self.name,
            recipient=message.sender,
            content=error_text,
            metadata=message.metadata
        )
