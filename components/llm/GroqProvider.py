from typing import Any, Dict, List
from .BaseLLM import BaseLLM
from .utils import get_groq_key


class GroqLLM(BaseLLM):
    def __init__(self, model_name: str = "mixtral-8x7b-32768"):
        import groq

        self.client = groq.Groq(api_key=get_groq_key())
        self.model = model_name

    def generate_response(self, prompt: str, **kwargs) -> str:
        return self.chat([{"role": "user", "content": prompt}])

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        completion = self.client.chat.completions.create(
            messages=messages,
            model=self.model,
        )
        return completion.choices[0].message.content
