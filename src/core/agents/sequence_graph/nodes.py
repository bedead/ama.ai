from typing import List
from core.agents.sequence_graph.states import SequenceState
from core.gmail.gmail_toolkit import GmailToolKit
from core.gmail.status import GmailToolKitRunningStatus
from core.json.reader import JSONEmailReader


def start_gmail_toolkit(state: SequenceState):
    """
    Start the Gmail toolkit if it is not already running.
    This Node checks the current status of the Gmail toolkit and starts it if it is not running.
    """
    if (
        state.gmail_toolkit_status != GmailToolKitRunningStatus.RUNNING
        and state.gmail_toolkit_status == GmailToolKitRunningStatus.STOPED
        and state.gmail_toolkit_status != GmailToolKitRunningStatus.PAUSED
    ):
        state.gmail_tool.start()
    return {"gmail_toolkit_status": GmailToolKitRunningStatus.RUNNING}


def pasue_gmail_toolkit(state: SequenceState):
    """
    Pause the Gmail toolkit if it is not already paused.
    This Node checks the current status of the Gmail toolkit and pauses it if it is not paused.
    """
    if (
        state.gmail_toolkit_status != GmailToolKitRunningStatus.PAUSED
        and state.gmail_toolkit_status == GmailToolKitRunningStatus.RUNNING
        and state.gmail_toolkit_status != GmailToolKitRunningStatus.STOPED
    ):
        state.gmail_tool.pause()
    return {"gmail_toolkit_status": GmailToolKitRunningStatus.PAUSED}


def resume_gmail_toolkit(state: SequenceState):
    if (
        state.gmail_toolkit_status != GmailToolKitRunningStatus.RUNNING
        and state.gmail_toolkit_status == GmailToolKitRunningStatus.PAUSED
        and state.gmail_toolkit_status != GmailToolKitRunningStatus.STOPED
    ):
        state.gmail_tool.resume()
    return {"gmail_toolkit_status": GmailToolKitRunningStatus.RUNNING}


def stop_gmail_toolkit(state: SequenceState):
    if (
        state.gmail_toolkit_status != GmailToolKitRunningStatus.STOPED
        and state.gmail_toolkit_status == GmailToolKitRunningStatus.RUNNING
        and state.gmail_toolkit_status != GmailToolKitRunningStatus.PAUSED
    ):
        state.gmail_tool.stop()
    return {"gmail_toolkit_status": GmailToolKitRunningStatus.STOPED}


def restart_gmail_toolkit(state: SequenceState):
    if (
        state.gmail_toolkit_status == GmailToolKitRunningStatus.RUNNING
        and state.gmail_toolkit_status != GmailToolKitRunningStatus.STOPED
        and state.gmail_toolkit_status != GmailToolKitRunningStatus.PAUSED
    ):
        state.gmail_tool.restart()
    return {"gmail_toolkit_status": GmailToolKitRunningStatus.RUNNING}


async def read_emails_json(state: SequenceState):
    """
    Read emails from the email reader and update the state with the email data.
    Asynch method (blocking), so that start on next node execution is awaited till the emails are read.
    """
    email_reader = JSONEmailReader()
    emails: List[dict] = await email_reader.get_all_email_content()

    if not isinstance(emails, list) or not emails:
        print("No emails found.")
        return None

    return {"email_list": emails}  # Return the first valid email data found


async def analyze_importance(state: SequenceState):
    """
    Analyze the importance of the email using the AI toolkit.
    """
    if not state.email_list:
        return None

    email_data = state.email_list[state.current_index]
    important_response = await state.ai_toolkit.analyze_importance(
        email_data=email_data, json_output=True
    )
    decision1 = important_response.get("output", "").lower().strip()

    return {"is_mail_important": decision1 == "yes"}


async def summarize_email(state: SequenceState):
    """
    Summarize the email using the AI toolkit.
    """
    if not state.email_list or state.current_index >= len(state.email_list):
        return None
    if state.is_mail_important:
        email_data = state.email_list[state.current_index]
        summary = await state.ai_toolkit.summarize_email(
            email_data=email_data, json_output=True
        )
        return {"email_summary": summary.get("output")}


async def is_response_needed(state: SequenceState):
    """
    Check if a response is needed for the email using the AI toolkit.
    """
    if not state.email_list or state.current_index >= len(state.email_list):
        return None
    if state.is_mail_important:
        email_data = state.email_list[state.current_index]
        response_needed = await state.ai_toolkit.is_response_needed(
            email_data=email_data, json_output=True
        )
        decision2 = response_needed.get("output", "").lower().strip()
        return {"is_response_needed": decision2 == "yes"}


async def mail_response_format(state: SequenceState):
    """
    Get the response format for the email using the AI toolkit.
    """
    if not state.email_list or state.current_index >= len(state.email_list):
        return None
    if state.is_mail_important and state.is_response_needed:
        email_data = state.email_list[state.current_index]
        format_response = await state.ai_toolkit.mail_response_format(
            email_data=email_data, json_output=True
        )
        response_format = format_response.get("output", "").lower().strip()
        return {"response_format": response_format}


async def generate_response(state: SequenceState):
    """
    Generate a response for the email using the AI toolkit.
    """
    if not state.email_list or state.current_index >= len(state.email_list):
        return None
    if state.is_mail_important and state.is_response_needed:
        email_data = state.email_list[state.current_index]
        response_suggestion = await state.ai_toolkit.generate_response(
            email_data=email_data,
            json_output=True,
            style=state.response_format,
        )
        response_text = response_suggestion.get("output")
        return {"response_email_draft": response_text}


def get_response_approval(state: SequenceState):
    """
    Get the response approval from the user.
    This is a placeholder function and should be replaced with actual user input handling.
    """
    # Simulate user approval for the response
    input_text = input("Do you approve the response? (yes/no): ").strip().lower()
    if input_text == "yes":
        user_approval = True
    elif input_text == "no":
        user_approval = False
    else:
        print("Invalid input. Please enter 'yes' or 'no'.")
        return None
    return {"response_approved": user_approval}


def get_edited_response(state: SequenceState):
    """
    Get the edited response from the user.
    This is a placeholder function and should be replaced with actual user input handling.
    """
    # Simulate user editing the response
    print("Current response draft:")
    print(state.response_email_draft)
    input_text = input("Please edit the response: ").strip()
    if input_text:
        return {"response_email_draft": input_text}
    return None


async def auto_edit_response(state: SequenceState):
    """
    Auto edit the response for the email using the AI toolkit (LLM) by giving customization instruction.
    """
    if not state.email_list or state.current_index >= len(state.email_list):
        return None
    if (
        state.is_mail_important
        and state.is_response_needed
        and state.response_email_draft != None
    ):
        email_data = state.email_list[state.current_index]
        edited_response = await state.ai_toolkit.edit_response(
            email_data=email_data,
            draft_mail=state.response_email_draft,
            json_output=True,
            style=state.response_format,
        )
        edited_response_text = edited_response.get("output")
        return {"response_edited": edited_response_text}


async def send_response(state: SequenceState):
    """
    Send the response for the email using the Gmail toolkit.
    """
    if not state.email_list or state.current_index >= len(state.email_list):
        return None
    if (
        state.is_mail_important
        and state.response_approved
        and state.is_response_needed
        and state.response_email_draft != None
    ):
        email_data = state.email_list[state.current_index]
        response_text = state.response_email_draft
        state.gmail_tool.send_mail(
            to=email_data["sender"],
            subject=email_data["subject"],
            body=response_text,
        )
        return {"response_sent": True}
