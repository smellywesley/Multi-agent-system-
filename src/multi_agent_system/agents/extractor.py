"""Extraction specialist agent."""

from pydantic import BaseModel, Field

from multi_agent_system.agents.base import BaseAgent
from multi_agent_system.config import get_settings
from multi_agent_system.schemas.messages import AgentMessage, ClinicalExtraction, ExtractionResult
from multi_agent_system.tools.llm_client import LLMClient

# --- 2026 BATCH SCHEMA ---
# We define a custom wrapper so the LLM knows to return a list of results
class BatchedPaper(BaseModel):
    pmid: str
    doi: str | None
    extraction: ClinicalExtraction

class BatchExtractionWrapper(BaseModel):
    papers: list[BatchedPaper] = Field(description="List of clinical extractions for all provided papers.")

class ExtractorAgent(BaseAgent):
    """Extracts structured clinical findings from citation abstracts."""

    def __init__(self, llm_client: LLMClient | None = None) -> None:
        super().__init__(name="extractor")
        settings = get_settings()
        self.llm_client = llm_client or LLMClient(settings=settings)

    def handle(self, message: AgentMessage) -> AgentMessage:
        if not message.citations:
            return AgentMessage(
                sender=self.name,
                recipient=message.sender,
                content="No citations provided for extraction.",
                metadata=message.metadata,
                citations=[],
                extractions=[],
            )

        # 1. Compile all abstracts into ONE single document
        compiled_text = ""
        for i, citation in enumerate(message.citations):
            if not citation.abstract.strip():
                continue
            compiled_text += f"--- PAPER {i+1} ---\n"
            compiled_text += f"PMID: {citation.pmid}\n"
            compiled_text += f"DOI: {citation.doi}\n"
            compiled_text += f"Title: {citation.title}\n"
            compiled_text += f"Abstract: {citation.abstract}\n\n"

        if not compiled_text:
            return AgentMessage(
                sender=self.name,
                recipient=message.sender,
                content="No valid abstracts found to extract.",
                metadata=message.metadata,
                citations=message.citations,
                extractions=[],
            )

        # 2. Make ONE single API call instead of firing off a loop
        prompt = (
            "You are an expert clinical data extraction specialist. "
            "Below is a batch of biomedical abstracts. For EACH paper provided, "
            "extract the structured clinical details (study design, sample size, key findings, "
            "risk-of-bias flags, and limitations). \n"
            "Return them as a list of extractions mapped to their respective PMIDs.\n\n"
            f"{compiled_text}"
        )

        extractions: list[ExtractionResult] = []
        try:
            # The LLM reads all papers and returns everything at once
            batch_result = self.llm_client.generate_structured(
                prompt=prompt,
                schema=BatchExtractionWrapper,
            )
            
            # 3. Map the results back into the original format so the ReviewerAgent doesn't break
            for paper in batch_result.papers:
                extractions.append(
                    ExtractionResult(
                        doi=paper.doi,
                        pmid=paper.pmid,
                        extraction=paper.extraction
                    )
                )
        except Exception as e:
            print(f"CRITICAL BATCH EXTRACTION ERROR: {str(e)}")
            raise RuntimeError(f"Extraction failed: {str(e)}")

        return AgentMessage(
            sender=self.name,
            recipient=message.sender,
            content=f"Successfully extracted clinical structure from {len(extractions)} citations in a single batch.",
            metadata=message.metadata,
            citations=message.citations,
            extractions=extractions,
        )
