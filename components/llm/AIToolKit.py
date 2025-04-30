from typing import Any, Dict, List

from .BaseLLM import BaseLLM
from .GoogleProvider import GeminiLLM
from .GroqProvider import GroqLLM


from .prompts_utils import (
    # LLM RESPONSE GENERATE
    IS_MAIL_IMPORTANT_PROMPT as analyze_importance_system_instructions,
    IS_RESPONSE_NEEDED_PROMPT as is_response_needed_system_instructions,
    # ROUTES FOR DECISION MAKING
    MAIL_SUMMARY_PROMPT as summarize_email_system_instructions,
    GENERATE_MAIL_RESPONSE_SUGGESTION_PROMPT as generate_response_system_instructions,
    MAIL_RESPONSE_FORMAT_PROMPT as mail_response_format_system_instructions,
)


class AIToolkit:
    def __init__(self, llm: BaseLLM):
        self.llm = llm
        self.chat_history: List[Dict[str, str]] = []

    def analyze_importance(
        self, email_data: Dict[str, Any], json_output: bool = False
    ) -> Dict[str, str] | str:
        """Analyze email importance using configured LLM"""
        response = self.llm.generate_response(
            contents=str(email_data),
            system_instruction=analyze_importance_system_instructions,
        )
        return {"output": response.strip()} if json_output else response

    def summarize_email(
        self, email_data: Dict[str, Any], json_output: bool = False
    ) -> Dict[str, str] | str:
        """Generate email summary using configured LLM"""
        response = self.llm.generate_response(
            contents=str(email_data),
            system_instruction=summarize_email_system_instructions,
        )
        return {"output": response.strip()} if json_output else response

    def is_response_needed(
        self, email_data: Dict[str, Any], json_output: bool = False
    ) -> Dict[str, str] | str:
        """Determine if a response is needed using configured LLM"""
        response = self.llm.generate_response(
            contents=str(email_data),
            system_instruction=is_response_needed_system_instructions,
        )
        return {"output": response.strip()} if json_output else response

    def mail_response_format(
        self, email_data: Dict[str, Any], json_output: bool = False
    ) -> Dict[str, str] | str:
        """Determine the response format using configured LLM"""
        response = self.llm.generate_response(
            contents=str(email_data),
            system_instruction=mail_response_format_system_instructions,
        )
        return {"output": response.strip()} if json_output else response

    def generate_response(
        self,
        email_data: Dict[str, Any],
        json_output: bool = False,
        style: str = "professional",
    ) -> Dict[str, str] | str:
        """Generate email response using configured LLM"""
        generate_response_system_instructions.format(style=style)
        response = self.llm.generate_response(
            contents=str(email_data),
            system_instruction=generate_response_system_instructions,
        )
        return {"output": response.strip()} if json_output else response

    def chat_response(self, message: str, remember_context: bool = True) -> str:
        """Generate response using chat history if remember_context is True"""
        if remember_context:
            self.chat_history.append({"role": "user", "content": message})
            response = self.llm.chat(self.chat_history)
            self.chat_history.append({"role": "assistant", "content": response})
            return response
        return self.llm.generate_response(message)

    def clear_chat_history(self):
        """Clear the chat history"""
        self.chat_history = []


# Usage example:
def get_ai_toolkit(llm_type: str = "gemini" or "groq") -> AIToolkit:
    if llm_type.lower() == "gemini":
        llm = GeminiLLM()
    elif llm_type.lower() == "groq":
        llm = GroqLLM()
    # Add more LLM implementations as needed
    return AIToolkit(llm)
