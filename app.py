import json
from components.llm.utils import get_gemini_client, get_chat_gemini_response
from components.gmail.gmail_toolkit import GmailToolKit
import time
from components.llm.routes.mail_important import get_mail_importance_decision
from components.json.reader import EmailReader

gmail_tool = GmailToolKit()
email_reader = EmailReader()
gmail_tool.start()


client = get_gemini_client()
while True:
    emails = email_reader.get_email_content()
    if isinstance(emails, list):
        print(f"Number of emails: {len(emails)}")
        gmail_tool.pause()
        for email in emails:
            str_email = f"From: {email['sender']}\nSubject: {email['subject']}"
            print(str_email)
            decision = get_mail_importance_decision(str_email, json_output=True)

            print(f"Decision: {decision.get('output')}")
            print("=" * 80)  # Separator

    question = input("You: ")
    # response = get_chat_gemini_response(client, question=question)
    # print(f"AI: {response.text}")
    if question.lower() == "exit":
        gmail_tool.stop()
        break
