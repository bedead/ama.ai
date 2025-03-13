from components.llm.utils import get_gemini_client, get_single_call_gemini_response


def get_prompt(email_data: str):
    SYS_PROMPT = (
        """
    Analyze the following email data to determine if it is important. 
    The email may contain the sender, subject, body, date, and other metadata. 
    The body and subject can be in HTML, Markdown, or plain text—convert them to plain text before making a judgment.

    Criteria for Importance:
    - Emails from **known contacts**, urgent language, or **action-required** content  
    - **Work-related** or critical **personal matters**  
    - **High-priority keywords** (e.g., "urgent," "important," "invoice," "deadline")  

    Expected Output Format:
    Return the result only as shown below and no other text required:
    yes   # If the email is important
    no    # If the email is not important 
    Mail: """
        + email_data
    )

    return SYS_PROMPT


def get_mail_importance_decision(data, json_output=False):
    client = get_gemini_client()
    q = get_prompt(email_data=data)
    response = get_single_call_gemini_response(client, question=q)
    if json_output:
        return {"output": response.text}
    return response.text
