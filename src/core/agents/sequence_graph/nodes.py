from typing import List
from core.agents.sequence_graph.states import SequenceState
from core.gmail.gmail_toolkit import GmailToolKit
from core.gmail.status import GmailToolKitRunningStatus
from core.json.reader import JSONEmailReader


def start_gmail_toolkit(state: SequenceState):
    state.gmail_tool.start()
    return {"gmail_toolkit_status": GmailToolKitRunningStatus.RUNNING}


def pasue_gmail_toolkit(state: SequenceState):
    state.gmail_tool.pause()
    return {"gmail_toolkit_status": GmailToolKitRunningStatus.PAUSED}


def resume_gmail_toolkit(state: SequenceState):
    state.gmail_tool.resume()
    return {"gmail_toolkit_status": GmailToolKitRunningStatus.RUNNING}


def stop_gmail_toolkit(state: SequenceState):
    state.gmail_tool.stop()
    return {"gmail_toolkit_status": GmailToolKitRunningStatus.STOPED}


def restart_gmail_toolkit(state: SequenceState):
    state.gmail_tool.restart()
    return {"gmail_toolkit_status": GmailToolKitRunningStatus.RUNNING}


def read_emails_json(state: SequenceState):
    """Read emails from the email reader and update the state with the email data."""
    email_reader = JSONEmailReader()
    emails: List[dict] = email_reader.get_all_email_content()

    if not isinstance(emails, list) or not emails:
        print("No emails found.")
        return None

    return {"email_list": emails}  # Return the first valid email data found
