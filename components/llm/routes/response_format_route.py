from components.llm.utils import get_gemini_client, get_single_call_gemini_response
from components.llm.prompts_utils import (
    MAIL_RESPONSE_FORMAT_PROMPT as system_instructions,
)


def is_response_proffessional_or_formal(data: dict, json_output=False) -> str | dict:
    client = get_gemini_client()

    response = get_single_call_gemini_response(
        client, system_instruction=system_instructions, contents=str(data)
    )
    if json_output:
        return {"output": response.text}
    return response.text
