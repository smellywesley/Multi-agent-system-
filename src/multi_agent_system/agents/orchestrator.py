"""Orchestrator Agent for breaking down queries."""

import logging
from .base import BaseAgent
from ..schemas.messages import AgentMessage, PICOQuery
from ..tools.llm_client import LLMClient

class OrchestratorAgent(BaseAgent):
    """Breaks down a clinical query into a strict PICO search and PRISMA rules."""
    
    def __init__(self, name="Orchestrator"):
        super().__init__(name=name)
        self.llm_client = LLMClient()
        self.logger = logging.getLogger(self.name)

    def handle(self, message: AgentMessage) -> AgentMessage:
        self.logger.info(f"Orchestrating task: {message.content}")

        prompt = f"""
        You are a Lead Clinical Orchestrator. 
        Convert the following research topic into a structured PICO query and define strict PRISMA screening criteria.
        
        RESEARCH TOPIC:
        {message.content}
        """

        try:
            # Generate the PICO Query using the 8B model
            pico_obj = self.llm_client.generate_structured(
                prompt=prompt,
                schema=PICOQuery,
                use_heavy_model=False
            )
            
            # THE FIX: Put the actual query in the 'content' so the Researcher finds it immediately
            return AgentMessage(
                sender=self.name,
                recipient=message.sender,
                content=pico_obj.pubmed_query, # <--- SEND THE QUERY, NOT A SUCCESS MESSAGE
                metadata={"pico_query": pico_obj.model_dump()}
            )
        except Exception as e:
            return AgentMessage(
                sender=self.name,
                recipient=message.sender,
                content=f"Error generating PICO: {str(e)}",
                metadata={}
            )
