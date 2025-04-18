from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from email.parser import Parser
import os
import poplib
import smtplib

mcp = FastMCP("mpc_email")

FORMAT_HEADERS = "FORMAT_HEADERS"
FORMAT_MESSAGE = "FORMAT_MESSAGE"
FORMAT_COMBINED = "FORMAT_COMBINED"

############################## Helper Functions ##############################

def getStrEnvVar (name: str):
    return str(os.getenv(name))

def getIntEnvVar (name: str, default: int):
    if str(os.getenv(name)).isnumeric():
        return int(str(os.getenv(name)))
    else:
        return default

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

def getEmails (ids: list):
    mb = inboxLogin()
    emails = []
    if not ids:
        for i in range(len(mb.list()[1])):
            emails.append(setEmail(mb.retr(i + 1), i + 1, FORMAT_COMBINED))
    else:
        for id in ids:
            for mail in mb.retr(id):
                emails.append(setEmail(mb.retr(id), id, FORMAT_COMBINED))
    mb.quit()
    return emails

def deleteEmails (ids: list):
    mb = inboxLogin()
    for id in ids:
        mb.dele(id)
    mb.quit()

def setEmail (mail: list, id: int, format: str):
    obj = {}
    obj['id'] = id
    msg = Parser().parsestr(b'\r\n'.join(mail[1]).decode('utf-8'))
    # TODO Introduce combined email format
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
    send = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    send.ehlo()  # Identify to the server
    send.starttls()  # Enable encryption
    send.ehlo()  # Re-identify over secure connection
    send.login(EMAIL_USER, EMAIL_PASS)
    message = "From: " + fromAddress + "\n"
    message += "To: " + ", ".join(toAddresses) + "\n"
    message += "MIME-Version: 1.0\n"
    message += "Content-type: " + contentType + "\n"
    message += "Subject: " + subject + "\n\n"
    message += body
    send.sendmail(fromAddress, toAddresses, message)
    send.quit()

################################# MCP Tools ##################################

@mcp.tool()
async def pollEmails() -> list:
    """Returms a list of all emails currenly in the inbox. Result is a list of 
    dict objects representing the email in the current inbox.
    """
    return getEmails([])

@mcp.tool()
def getEmailsById(ids: list) -> list:
    """Returms a list of emails currenly in the inbox based on ID. Result is a
    list of dict objects representing the selected emails.

    Args:
        ids: A list of integer based message IDs
    """
    return getEmails(ids)

@mcp.tool()
def deleteEmailsById(ids: list) -> list:
    """Deletes a list of emails currenly in the inbox based on ID. Note that 
    deleting any emails invalidates the current order of IDs.

    Args:
        ids: A list of integer based message IDs
    """
    deleteEmails(ids)

@mcp.tool()
def sendTextEmail(fromAddress: str, toAddresses: list, subject: str, body: str) -> None:
    """Sends an email in text format. No result is returned.

    Args:
        fromAddress: String. The Originating address.
        toAddresses: List of strings. The destination addresses.
        subject: String. The subject line.
        body: String. The message body.
    """
    sendEmail(fromAddress, toAddresses, "text/plain", subject, body)

@mcp.tool()
def sendHtmlEmail(fromAddress: str, toAddresses: list, subject: str, body: str) -> None:
    """Sends an email in HTML format. No result is returned.

    Args:
        fromAddress: String. The Originating address.
        toAddresses: List of strings. The destination addresses.
        subject: String. The subject line.
        body: String. The message body.
    """
    sendEmail(fromAddress, toAddresses, "text/html", subject, body)

##############################################################################

load_dotenv()

EMAIL_USER = getStrEnvVar("EMAIL_USER")
EMAIL_PASS = getStrEnvVar("EMAIL_PASS")
POP3_SERVER = getStrEnvVar("POP3_SERVER")
POP3_PORT = getIntEnvVar("POP3_PORT", 995)
SMTP_SERVER = getStrEnvVar("SMTP_SERVER")
SMTP_PORT = getIntEnvVar("SMTP_PORT", 587)

if __name__ == "__main__":
    mcp.run(transport='stdio')
