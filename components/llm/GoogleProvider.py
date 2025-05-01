from typing import List
from google.genai.chats import Chat
from google.genai.types import GenerateContentConfig
from google import genai

from .BaseLLM import BaseLLM
from .utils import get_google_gemini_key


class GeminiLLM(BaseLLM):
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        self.client = genai.Client(api_key=get_google_gemini_key())
        self.model_name = model_name

    def generate_response(
        self, contents: str | List[str], system_instruction, **kwargs
    ) -> str:
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

    def chat(self, message: str, **kwargs) -> str:
        response = kwargs.get("chat_instance").send_message(message)
        return response.text
