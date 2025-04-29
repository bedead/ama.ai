from components.llm.utils import get_gemini_client, get_single_call_gemini_response
from components.llm.prompts_utils import (
    GENERATE_MAIL_RESPONSE_SUGGESTION_PROMPT as system_instructions,
)


def generate_response_suggestion(data: dict, response_format_type: str) -> str:
    client = get_gemini_client()

    response = get_single_call_gemini_response(
        client, system_instruction=system_instructions, contents=str(data)
    )
    return response.text
