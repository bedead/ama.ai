from components.llm.AIToolKit import get_ai_toolkit

ai_toolkit = get_ai_toolkit("gemini")
email_data = {
    "subject": "Meeting Reminder",
    "body": "Don't forget about the meeting tomorrow at 10 AM.",
    "attachments": ["agenda.pdf", "minutes.docx"],
    "sender": "",
}

result = ai_toolkit.analyze_importance(email_data, json_output=True)
print(result)
