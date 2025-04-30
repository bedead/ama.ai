from google import genai
from dotenv import load_dotenv
import os
from google.genai.types import GenerateContentConfig
from typing import List

load_dotenv()


def get_google_gemini_key():
    return os.environ.get("GEMINI_API_KEY")


def get_groq_key():
    return os.environ.get("GROQ_API_KEY")


def get_gemini_client():
    key = get_google_gemini_key()
    client = genai.Client(api_key=key)
    return client


def get_single_call_gemini_response(
    client,
    system_instruction: str = None,
    model_name="gemini-1.5-flash",
    contents: List[str] = ["what can you do?"],
):
    response = client.models.generate_content(
        model=model_name,
        config=GenerateContentConfig(
            system_instruction=system_instruction,
        ),
        contents=contents,
    )
    return response


def get_chat_gemini_response(
    client, model_name="gemini-2.0-flash", question="what can you do?"
):
    chat = client.chats.create(model=model_name)
    response = chat.send_message(message=question)
    return response
