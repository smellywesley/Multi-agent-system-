"""Base agent contract."""

from abc import ABC, abstractmethod

from multi_agent_system.schemas.messages import AgentMessage


class BaseAgent(ABC):
    """Abstract agent interface."""

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def handle(self, message: AgentMessage) -> AgentMessage:
        """Handle an incoming message and return a response."""
