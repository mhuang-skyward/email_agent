"""
Email utility functions for the MCP Email Agent.

This module contains helper functions for email operations including:
- Email retrieval via POP3
- Email sending via SMTP
- Email parsing and formatting

All functions use environment variables for email server configuration.
"""

from email.parser import Parser
import poplib
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

# Email format constants
FORMAT_HEADERS = "FORMAT_HEADERS"  # Format with only email headers
FORMAT_MESSAGE = "FORMAT_MESSAGE"  # Format with only email body
FORMAT_COMBINED = "FORMAT_COMBINED"  # Format with both headers and body

# Load email configuration from environment variables
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
POP3_SERVER = os.getenv("POP3_SERVER")
POP3_PORT = int(os.getenv("POP3_PORT", 995))
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

def inboxLogin():
    """Logs into the email inbox using POP3.
    
    Uses environment variables for server and authentication details.
    
    Returns:
        poplib.POP3_SSL: The connected POP3 mailbox object.
    """
    mailbox = poplib.POP3_SSL(POP3_SERVER, POP3_PORT)
    mailbox.user(EMAIL_USER)
    mailbox.pass_(EMAIL_PASS)
    return mailbox

def addAttr(mail: dict, name: str):
    """Safely retrieves an email attribute.
    
    Args:
        mail (dict): Email message dictionary.
        name (str): Attribute name to retrieve.
        
    Returns:
        Any: The attribute value if it exists, None otherwise.
    """
    if name in mail:
        return mail.get(name)
    else:
        return None

def getEmails(ids: list):
    """Retrieves emails from the mailbox.
    
    Args:
        ids (list): List of email IDs to retrieve. If empty, retrieves all emails.
        
    Returns:
        list: List of email dictionaries containing headers and body.
    """
    mb = inboxLogin()
    emails = []
    if not ids:
        for i in range(len(mb.list()[1])):
            emails.append(setEmail(mb.retr(i + 1), i + 1, FORMAT_COMBINED))
    else:
        for id in ids:
            emails.append(setEmail(mb.retr(id), id, FORMAT_COMBINED))
    mb.quit()
    return emails

def deleteEmails(ids: list):
    """Deletes specified emails from the mailbox.
    
    Args:
        ids (list): List of email IDs to delete.
    """
    mb = inboxLogin()
    for id in ids:
        mb.dele(id)
    mb.quit()

def setEmail(mail: list, id: int, format: str):
    """Parses an email message into a structured dictionary.
    
    Args:
        mail (list): Raw email data from POP3 server.
        id (int): Email ID.
        format (str): Desired format - one of FORMAT_HEADERS, FORMAT_MESSAGE, or FORMAT_COMBINED.
        
    Returns:
        dict: Structured email data with headers and/or body based on the format.
    """
    obj = {}
    obj['id'] = id
    msg = Parser().parsestr(b'\r\n'.join(mail[1]).decode('utf-8'))
    
    # Extract headers if requested
    if format == FORMAT_HEADERS or format == FORMAT_COMBINED:
        obj['From'] = addAttr(msg, 'From')
        obj['Content-Type'] = addAttr(msg, 'Content-Type')
        obj['MIME-Version'] = addAttr(msg, 'MIME-Version')
        obj['User-Agent'] = addAttr(msg, 'User-Agent')
        obj['Subject'] = addAttr(msg, 'Subject') 
        obj['Encoding'] = addAttr(msg, 'Encoding')
        obj['To'] = addAttr(msg, 'To')
        obj['Cc'] = addAttr(msg, 'Cc')
        obj['Content-Language'] = addAttr(msg, 'Content-Language')
    
    # Extract body if requested
    if format == FORMAT_MESSAGE or format == FORMAT_COMBINED:
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type():
                    body = part.get_payload(decode=True)
        else:
            body = msg.get_payload(decode=True)
        obj['body'] = body
    
    return obj

def sendEmail(fromAddress: str, toAddresses: list, contentType: str, subject: str, body: str):
    """Sends an email via SMTP.
    
    Args:
        fromAddress (str): Sender's email address.
        toAddresses (list): List of recipient email addresses.
        contentType (str): Content type of the email (e.g., 'text/plain', 'text/html').
        subject (str): Email subject line.
        body (str): Email body content.
        
    Returns:
        str: Success message or error message.
    """
    try:
        # Connect to SMTP server
        send = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        send.ehlo()  # Identify to the server
        send.starttls()  # Enable encryption
        send.ehlo()  # Re-identify over secure connection
        send.login(EMAIL_USER, EMAIL_PASS)
        
        # Construct email message
        message = "From: " + fromAddress + "\n"
        message += "To: " + ", ".join(toAddresses) + "\n"
        message += "MIME-Version: 1.0\n"
        message += "Content-type: " + contentType + "\n"
        message += "Subject: " + subject + "\n\n"
        message += body
        
        # Send email
        send.sendmail(fromAddress, toAddresses, message)
        send.quit()
        return "Email sent successfully"
    except Exception as e:
        return f"Failed to send email: {str(e)}"