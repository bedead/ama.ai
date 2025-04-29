from components.llm.utils import get_gemini_client
from components.gmail.gmail_toolkit import GmailToolKit
from components.llm.routes.mail_important import is_mail_important
from components.llm.routes.respone_route import is_mail_response_needed
from components.llm.routes.response_format_route import (
    is_response_proffessional_or_formal,
)
from components.json.reader import JSONEmailReader
from components.llm.process.email_summary import mail_summary
from components.llm.process.email_response import generate_response_suggestion

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
        for mail_data in emails:
            str_email = f"From: {mail_data['sender']}\nSubject: {mail_data['subject']}"
            print(str_email)
            response: dict = is_mail_important(mail_data, json_output=True)

            print(f"Decision:{response.get('output').lower()}")
            print("=" * 80)  # Separator
            ## checking if mail is important or not, if important summaries and process further
            if response.get("output").lower() == "yes":
                summarry: str = mail_summary(data=mail_data)
                print(f"Summary: {summarry}")

                ## checking if the mail requires some response
                response: dict = is_mail_response_needed(
                    data=mail_data, json_output=True
                )

                if response.get("output").lower() == "yes":
                    ## analyze response format
                    response: dict = is_response_proffessional_or_formal(
                        data=mail_data, json_output=True
                    )
                    response = response.get("output").lower()
                    ## check if output in following options, if yes procced
                    if response in ["proffessional", "formal"]:
                        ## generating mail response based on gmail data, and predicted response format
                        generate_response_suggestion(
                            data=mail_data, response_format_type=response
                        )

                        
                    

            else:
                gmail_tool.resume()
                print(f"Skipped email from {mail_data['sender']}")
    else:
        gmail_tool.resume()
        print("No emails found.")

    question = input("You: ")
    # response = get_chat_gemini_response(client, question=question)
    # print(f"AI: {response.text}")
    if question.lower() == "exit":
        gmail_tool.stop()
        break
