from typing import Dict, List
from google.genai.chats import Chat

from ..base_llm import BaseLLM
from ...utils.utils import get_google_gemini_key


class GeminiLLM(BaseLLM):
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        from google import genai

        self.model_provider = "google"
        self.client = genai.Client(api_key=get_google_gemini_key())
        self.model_name = model_name

    def generate_response(
        self, contents: str | List[str], system_instruction, **kwargs
    ) -> str:
        from google.genai.types import GenerateContentConfig

        response = self.client.models.generate_content(
            model=self.model_name,
            config=GenerateContentConfig(
                system_instruction=system_instruction,
            ),
            contents=contents,
        )
        return response.text

    def initialize_chat(self, **kwargs) -> Chat:
        """Initialize chat with the model"""

        return self.client.chats.create(model=self.model_name)

    def chat(self, message: str | List[Dict[str, str]], **kwargs) -> str:
        response = kwargs.get("chat_instance").send_message(message)
        return response.text
