from typing import Any, Dict
from google.genai.chats import Chat
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
        self.chat_instance: Chat = None

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

    def chat_response(self, message: str) -> str:
        """Generate response using chat based on chat history"""
        if not self.chat_instance:
            self.chat_instance = self.llm.initialize_chat()

        response = self.llm.chat(message, chat_instance=self.chat_instance)
        return response

    def clear_chat(self):
        """Clear the chat"""
        self.chat_instance = None


# Usage example:
def get_ai_toolkit(llm_type: str = "gemini" or "groq") -> AIToolkit:
    if llm_type.lower() == "gemini":
        llm = GeminiLLM()
    elif llm_type.lower() == "groq":
        llm = GroqLLM()
    # Add more LLM implementations as needed
    return AIToolkit(llm)
