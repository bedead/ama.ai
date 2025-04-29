from components.llm.utils import get_gemini_client, get_single_call_gemini_response
from components.llm.prompts_utils import (
    IS_RESPONSE_NEEDED_PROMPT as system_instructions,
)


def is_mail_response_needed(data: dict, json_output=False) -> str | dict:
    client = get_gemini_client()

    response = get_single_call_gemini_response(
        client, system_instruction=system_instructions, contents=str(data)
    )
    if json_output:
        return {"output": response.text}
    return response.text
