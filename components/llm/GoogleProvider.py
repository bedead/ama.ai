from typing import List, Dict
from google.genai.types import GenerateContentConfig, HttpOptions
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

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        chat = self.client.start_chat()
        for message in messages:
            if message["role"] == "user":
                response = chat.send_message(message["content"])
        return response.text
