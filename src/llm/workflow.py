from typing import Any, Dict, List
import logging

from google.genai.chats import Chat

from .base_llm import BaseLLM
from .providers.google import GeminiLLM
from .providers.groq import GroqLLM


from ..utils.prompts import (
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
        self.llm: BaseLLM = llm
        self.chat_instance: Chat = None
        self.chat_history: List[Dict[str, str]] = []
        self.log = logging.getLogger("ama.llm.workflow")

    def analyze_importance(
        self, email_data: Dict[str, Any], json_output: bool = False
    ) -> Dict[str, str] | str:
        """Analyze email importance using configured LLM"""
        try:
            response = self.llm.generate_response(
                contents=str(email_data),
                system_instruction=analyze_importance_system_instructions,
            )
            return {"output": response.strip()} if json_output else response
        except Exception as e:
            self.log.error(f"Error analyzing importance: {e}")
            return {"output": "Error"}

    def summarize_email(
        self, email_data: Dict[str, Any], json_output: bool = False
    ) -> Dict[str, str] | str:
        """Generate email summary using configured LLM"""
        try:
            response = self.llm.generate_response(
                contents=str(email_data),
                system_instruction=summarize_email_system_instructions,
            )
            return {"output": response.strip()} if json_output else response
        except Exception as e:
            self.log.error(f"Error summarizing email: {e}")
            return {"output": "Error"}

    def is_response_needed(
        self, email_data: Dict[str, Any], json_output: bool = False
    ) -> Dict[str, str] | str:
        """Determine if a response is needed using configured LLM"""
        try:
            response = self.llm.generate_response(
                contents=str(email_data),
                system_instruction=is_response_needed_system_instructions,
            )
            return {"output": response.strip()} if json_output else response
        except Exception as e:
            self.log.error(f"Error determining response needed: {e}")
            return {"output": "Error"}

    def mail_response_format(
        self, email_data: Dict[str, Any], json_output: bool = False
    ) -> Dict[str, str] | str:
        """Determine the response format using configured LLM"""
        try:
            response = self.llm.generate_response(
                contents=str(email_data),
                system_instruction=mail_response_format_system_instructions,
            )
            return {"output": response.strip()} if json_output else response
        except Exception as e:
            self.log.error(f"Error determining mail response format: {e}")
            return {"output": "Error"}

    def generate_response(
        self,
        email_data: Dict[str, Any],
        json_output: bool = False,
        style: str = "professional",
    ) -> Dict[str, str] | str:
        """Generate email response suggestion based on format using configured LLM"""
        try:
            generate_response_system_instructions.format(style=style)
            response = self.llm.generate_response(
                contents=str(email_data),
                system_instruction=generate_response_system_instructions,
            )
            return {"output": response.strip()} if json_output else response
        except Exception as e:
            self.log.error(f"Error generating response: {e}")
            return {"output": "Error"}

    def add_user_information(
        self, user_information: Dict[str, Any], json_output: bool = False
    ):
        pass

    def chat_response(
        self,
        message: str,
        additional_context: List[Dict[str, List | str]] | str,
        role: str,
        tool_calling: bool = False,
        tool_choice: str = None,
        tools: List[str] = None,
        stream: bool = False,
    ) -> str:
        """Generate response using chat based on chat history"""
        try:
            if not self.chat_instance and self.llm.model_provider == "google":
                self.chat_instance = self.llm.initialize_chat()
                response = self.llm.chat(message, chat_instance=self.chat_instance)
            else:
                self.chat_history.append(
                    {"role": "system", "content": additional_context}
                )
                self.chat_history.append({"role": "user", "content": message})

                response = self.llm.chat(self.chat_history)
                self.chat_history.append({"role": "assistant", "content": response})
            return response
        except Exception as e:
            self.log.error(f"Error generating chat response: {e}")
            return "Error"

    def clear_chat(self):
        """Clear the chat"""
        self.chat_instance = None
        self.chat_history = []


# Usage example:
def get_ai_toolkit(llm_type: str = "google" or "groq") -> AIToolkit:
    if llm_type.lower() == "google":
        llm = GeminiLLM()
    elif llm_type.lower() == "groq":
        llm = GroqLLM()
    # Add more LLM implementations as needed
    return AIToolkit(llm)
