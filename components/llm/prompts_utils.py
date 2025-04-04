from textwrap import dedent

MAIL_SUMMARY_PROMPT = dedent(
    """
    Summarize the given email data into a concise format. 
    The email may contain the sender, subject, body, date, and other metadata. 
    The body and subject can be in HTML, Markdown, or plain text. Convert them to plain text before making a summary.

    Make sure that the summary is verbalized in a way that is easy to understand, doesn't involve complex vocabulary and captures the main points of the email.
    The summary should be in a single paragraph, which can be narrated in a way that sounds natural and human-like.
    
    Example of ways how you can start with summary(Can you use more similar ways to start):
    Hey, you have got a mail from ...
    (If something seems important): It's seems there is an important mail from ...
    (If something seems not important): It's seems there is a spam mail from ...
    (Mail from Friend/Relative/Family/Boss/etc): There's a mail from your friend/relative/etc ...
    
    (Additional information): You can you add emotional/scenario/etc judgment of the mail in the beginning or end of the summary. 
    """
)
IS_MAIL_IMPORTANT_PROMPT = dedent(
    """
    Analyze the given email data to determine if it is important or not. 
    The email may contain the sender, subject, body, date, and other metadata. 
    The body and subject can be in HTML, Markdown, or plain text—convert them to plain text before making a judgment.

    Criteria for Importance:
    - Emails from **known contacts**, urgent language, or **action-required** content  
    - **Work-related** or critical **personal matters** or **financial transactions** or **legal matters** or **Mail related for inquiry or maybe some friend contacting**   
    - **High-priority keywords** (e.g., "urgent," "important," "invoice," "deadline", "job accptance", "meeting", "interview", "offer", "contract", "payment", "confirmation")  
    - **Attachments** that are relevant to the email's content
    - **Follow-up** emails on previous conversations

    Expected Output Format:
    Return the result only as shown below and no other text required:
    yes   # If the email is important
    no    # If the email is not important 
    """
)
