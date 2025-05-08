from typing import Any, Dict, List, Optional
from pydantic import BaseModel

from core.gmail.gmail_toolkit import GmailToolKit
from core.gmail.status import GmailToolKitRunningStatus


class SequenceState(BaseModel):
    """
    A class to represent the state of a sequence agent in a graph.
    """

    # Attributes
    # id: str
    email_list: List[dict]
    current_index: int
    email: dict
    is_maiL_important: bool
    email_summary: Optional[str]
    is_response_needed: bool
    response_format: Optional[str]
    response_email_draft: Optional[str]
    response_approved: Optional[bool]
    response_sent: Optional[bool]
    response_edited: Optional[str]

    # tracking gmail_toolkit running status
    gmail_tool = GmailToolKit(interval=10, max_results=1)
    gmail_toolkit_status: GmailToolKitRunningStatus

    # tracking workflow message history
    messages: List[Dict[str, Any]]
