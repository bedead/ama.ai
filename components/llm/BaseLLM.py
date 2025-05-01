from abc import ABC, abstractmethod
from typing import List


class BaseLLM(ABC):
    """Abstract base class for LLM implementations"""

    @abstractmethod
    def generate_response(
        self, contents: str | List[str], system_instruction, **kwargs
    ) -> str:
        """Generate single-turn response from the LLM"""
        pass

    @abstractmethod
    def chat(self, message: str, **kwargs) -> str:
        """Generate response based on chat history"""
        pass
