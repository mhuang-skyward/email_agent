from typing import List
from mcp.server.fastmcp import FastMCP
from mcp.types import Tool
from dotenv import load_dotenv
import os
import aiohttp
from email.parser import Parser
import poplib
import smtplib

# Initialize MCP server
mcp = FastMCP("SimpleMCPServer")

# Email constants
FORMAT_HEADERS = "FORMAT_HEADERS"
FORMAT_MESSAGE = "FORMAT_MESSAGE"
FORMAT_COMBINED = "FORMAT_COMBINED"

# Load email configuration from environment variables
def getStrEnvVar (name: str):
    return str(os.getenv(name))

def getIntEnvVar (name: str, default: int):
    if str(os.getenv(name)).isnumeric():
        return int(str(os.getenv(name)))
    else:
        return default

# Email helper functions
def inboxLogin():
    mailbox = poplib.POP3_SSL(POP3_SERVER, POP3_PORT)
    mailbox.user(EMAIL_USER)
    mailbox.pass_(EMAIL_PASS)
    return mailbox

def addAttr(mail: dict, name: str):
    if name in mail:
        return mail.get(name)
    else:
        return None

def getEmails(ids: list):
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
    mb = inboxLogin()
    for id in ids:
        mb.dele(id)
    mb.quit()

def setEmail(mail: list, id: int, format: str):
    obj = {}
    obj['id'] = id
    msg = Parser().parsestr(b'\r\n'.join(mail[1]).decode('utf-8'))
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
    try:
        # Use the exact same sequence that worked in the original code
        send = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        send.ehlo()  # Identify to the server
        send.starttls()  # Enable encryption
        send.ehlo()  # Re-identify over secure connection - this is crucial
        send.login(EMAIL_USER, EMAIL_PASS)
        
        message = "From: " + fromAddress + "\n"
        message += "To: " + ", ".join(toAddresses) + "\n"
        message += "MIME-Version: 1.0\n"
        message += "Content-type: " + contentType + "\n"
        message += "Subject: " + subject + "\n\n"
        message += body
        
        send.sendmail(fromAddress, toAddresses, message)
        send.quit()
        return "Email sent successfully"
    except Exception as e:
        return f"Failed to send email: {str(e)}"

#### Write Tools here ####
@mcp.tool()
async def pollEmails() -> list:
    """Returns a list of all emails currently in the inbox. Result is a list of 
    dict objects representing the email in the current inbox.
    """
    return getEmails([])

@mcp.tool()
async def getEmailsById(ids: list) -> list:
    """Returns a list of emails currently in the inbox based on ID. Result is a
    list of dict objects representing the selected emails.

    Args:
        ids: A list of integer based message IDs
    """
    return getEmails(ids)

@mcp.tool()
async def deleteEmailsById(ids: list) -> list:
    """Deletes a list of emails currently in the inbox based on ID. Note that 
    deleting any emails invalidates the current order of IDs.

    Args:
        ids: A list of integer based message IDs
    """
    deleteEmails(ids)

@mcp.tool()
async def sendTextEmail(fromAddress: str, toAddresses: list, subject: str, body: str) -> None:
    """Sends an email in text format. No result is returned.

    Args:
        fromAddress: String. The originating address.
        toAddresses: List of strings. The destination addresses.
        subject: String. The subject line.
        body: String. The message body.
    """
    try:
        result = sendEmail(fromAddress, toAddresses, "text/plain", subject, body)
        return result  # This should be a string like "Email sent successfully"
    except Exception as e:
        return f"Error sending email: {str(e)}"

@mcp.tool()
async def sendHtmlEmail(fromAddress: str, toAddresses: list, subject: str, body: str) -> None:
    """Sends an email in HTML format. No result is returned.

    Args:
        fromAddress: String. The originating address.
        toAddresses: List of strings. The destination addresses.
        subject: String. The subject line.
        body: String. The message body.
    """
    try:
        result = sendEmail(fromAddress, toAddresses, "text/html", subject, body)
        return result
    except Exception as e:
        return f"Error sending HTML email: {str(e)}"


async def list_tools() -> List[Tool]:
    """List the tools available to the LLM."""
    return [
        Tool(
            name="pollEmails",
            description="Returns a list of all emails currently in the inbox",
            inputSchema={
                "name": "pollEmails",
                "required": [],
                "properties": {}
            },
        ),
        Tool(
            name="getEmailsById",
            description="Returns specific emails by their IDs",
            inputSchema={
                "name": "getEmailsById",
                "required": ["ids"],
                "properties": {
                    "ids": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "List of email IDs to retrieve"
                    }
                }
            },
        ),
        Tool(
            name="deleteEmailsById",
            description="Deletes specific emails by their IDs",
            inputSchema={
                "name": "deleteEmailsById",
                "required": ["ids"],
                "properties": {
                    "ids": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "List of email IDs to delete"
                    }
                }
            },
        ),
        Tool(
            name="sendTextEmail",
            description="Sends a plain text email",
            inputSchema={
                "name": "sendTextEmail",
                "required": ["fromAddress", "toAddresses", "subject", "body"],
                "properties": {
                    "fromAddress": {
                        "type": "string",
                        "description": "Email address to send from"
                    },
                    "toAddresses": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of email addresses to send to"
                    },
                    "subject": {
                        "type": "string",
                        "description": "Email subject line"
                    },
                    "body": {
                        "type": "string",
                        "description": "Plain text body of the email"
                    }
                }
            },
        ),
        Tool(
            name="sendHtmlEmail",
            description="Sends an HTML-formatted email",
            inputSchema={
                "name": "sendHtmlEmail",
                "required": ["fromAddress", "toAddresses", "subject", "body"],
                "properties": {
                    "fromAddress": {
                        "type": "string",
                        "description": "Email address to send from"
                    },
                    "toAddresses": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of email addresses to send to"
                    },
                    "subject": {
                        "type": "string",
                        "description": "Email subject line"
                    },
                    "body": {
                        "type": "string",
                        "description": "HTML-formatted body of the email"
                    }
                }
            },
        )
    ]

load_dotenv()

EMAIL_USER = getStrEnvVar("EMAIL_USER")
EMAIL_PASS = getStrEnvVar("EMAIL_PASS")
POP3_SERVER = getStrEnvVar("POP3_SERVER")
POP3_PORT = getIntEnvVar("POP3_PORT", 995)
SMTP_SERVER = getStrEnvVar("SMTP_SERVER")
SMTP_PORT = getIntEnvVar("SMTP_PORT", 587)

# Start MCP server with SSE transport
if __name__ == "__main__":
    mcp.run(transport="sse")