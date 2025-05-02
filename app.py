import logging
from typing import List
import strip_markdown

from components.llm.utils import get_gemini_client
from components.gmail.gmail_toolkit import GmailToolKit
from components.json.reader import JSONEmailReader

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


def main():
    gmail_tool = GmailToolKit()
    email_reader = JSONEmailReader()
    gmail_tool.start()

    client = get_gemini_client()

    while True:
        emails: List[dict] = email_reader.get_email_content()

        if not isinstance(emails, list) or not emails:
            logger.info("No emails found.")
            gmail_tool.resume()
            continue

        logger.info(f"Number of emails: {len(emails)}")
        gmail_tool.pause()

        for mail_data in emails:
            logger.info(
                f"Processing email from {mail_data['sender']} - Subject: {mail_data['subject']}"
            )

            important_response = is_mail_important(mail_data, json_output=True)
            decision1 = important_response.get("output", "").lower().strip()

            logger.debug(
                f"is_mail_important output: '{decision1}' (ASCII: {[ord(c) for c in decision1]})"
            )

            if decision1 == "yes":
                logger.info("Email identified as important.")

                summary = mail_summary(data=mail_data)
                logger.info(f"Summary generated: {summary}")

                response_needed = is_mail_response_needed(
                    data=mail_data, json_output=True
                )
                decision2 = response_needed.get("output", "").lower().strip()

                logger.debug(
                    f"is_response_needed output: '{decision2}' (ASCII: {[ord(c) for c in decision2]})"
                )

                if decision2 == "yes":
                    logger.info("Response required for this email.")

                    format_response = is_response_proffessional_or_formal(
                        data=mail_data, json_output=True
                    )
                    response_format = format_response.get("output", "").lower().strip()

                    if response_format in ["proffessional", "formal"]:
                        logger.info(
                            f"Email format identified as '{response_format}'. Generating response..."
                        )
                        response_suggestion = generate_response_suggestion(
                            data=mail_data, response_format_type=response_format
                        )
                        RESPONSE_TXT: str = strip_markdown.strip_markdown(
                            response_suggestion
                        )
                        logger.info(RESPONSE_TXT)
                    else:
                        logger.info(
                            f"Response format '{response_format}' not suitable for automated suggestion."
                        )
                else:
                    logger.info("No response required for this email.")
            else:
                logger.info(
                    f"Email from {mail_data['sender']} identified as not important. Skipping."
                )
                gmail_tool.resume()

        # Prompt user input (manual control loop)
        question = input("You: ")
        if question.lower() == "exit":
            logger.info("Exiting system and stopping Gmail tool.")
            gmail_tool.stop()
            break


if __name__ == "__main__":
    main()
