"""Base workflow class."""

import logging
from abc import ABC, abstractmethod
from typing import Optional
from ..schemas.messages import AgentMessage

class BaseWorkflow(ABC):
    """Abstract base class for all multi-agent workflows."""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(self.name)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    @abstractmethod
    def run(self, task: str) -> Optional[AgentMessage]:
        """Execute the workflow."""
        pass
