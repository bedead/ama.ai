from components.llm.utils import get_gemini_client, get_chat_gemini_response
from components.gmail.gmail_toolkit import GmailToolKit
from components.llm.routes.mail_important import get_mail_importance_decision
from components.json.reader import JSONEmailReader
from components.llm.process.email_summary import mail_summary

from typing import List

gmail_tool = GmailToolKit()
email_reader = JSONEmailReader()
gmail_tool.start()


client = get_gemini_client()
while True:
    emails: List[dict] = email_reader.get_email_content()
    if isinstance(emails, List) and len(emails) > 0:
        print(f"Number of emails: {len(emails)}")
        gmail_tool.pause()
        for email in emails:
            str_email = f"From: {email['sender']}\nSubject: {email['subject']}"
            print(str_email)
            decision: dict = get_mail_importance_decision(email, json_output=True)

            print(f"Decision:{decision.get('output').lower()}")
            print("=" * 80)  # Separator
            if decision.get("output").lower() == "yes":
                summarry: str = mail_summary(data=email)
                print(f"Summary: {summarry}")

            else:
                gmail_tool.resume()
                print(f"Skipped email from {email['sender']}")
    else:
        gmail_tool.resume()
        print("No emails found.")

    question = input("You: ")
    # response = get_chat_gemini_response(client, question=question)
    # print(f"AI: {response.text}")
    if question.lower() == "exit":
        gmail_tool.stop()
        break
