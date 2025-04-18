# Email MCP

Email MCP is a simple Model Context Protocol (MCP) server that adds email functionality to an AI agent - both POP3 and SMTP.

Configuration allows the registration of the POP3 and SMTP details for an email account that can be used for the purpose of email.

### Tools

The following tools are accessible by the attached LLM:

* **pollEmails()** Returns the message ID and headers of all the emails presently stored in the slected mailbox. Function has no inputs and returns a `list` of `dict` objects.

* **getEmailsById(ids: list)** Returns the message ID and message body of all the emails called. Only input is an ID list of all the required messages. Function returns a `list` of `dict` objects.

* **deleteEmailsById(ids: list)** Deletes a list of emails currenly in the inbox based on ID. Note that deleting any emails invalidates the current order of IDs - as such it is best to prompt the model to carry this action at the end. Function returns nothing.

* **sendTextEmail(fromAddress: str, toAddresses: list, subject: str, body: str)** Sends a plain text formatted email via SMTP. Inputs are (in order); outgoing email address, destination addresses, subject text, body text of the email content. Function returns nothing.

* **sendHtmlEmail(fromAddress: str, toAddresses: list, subject: str, body: str)** Sends a HTML formatted email via SMTP. Inputs are (in order); outgoing email address, destination addresses, subject text, HTML formatted text of the email content. Function returns nothing.

### Installation

Installation to _Claude Desktop_ requires the addition of the following to the developer config file:
```
{
    "mcpServers": {
        "mcp_email": {
            "command": "uv",
            "args": [
                "--directory",
                "/Absolute/path/to/server/directory",
                "run",
                "main.py"
            ],
            "env": {
                "EMAIL_USER": "Email account username",
                "EMAIL_PASS": "Email account password",
                "POP3_SERVER": "POP3 Server Address",
                "POP3_PORT": "POP3 Server Port Number",
                "SMTP_SERVER": "SMTP Server Address",
                "SMTP_PORT": "SMTP Server Port Number"
            }
        }
    }
}
```
**Please Note:** The second argument should be the absolute path to the MCP_EMAIL folder. For windows users it is also assumed that Python is already set up in your Path variable. For Windows installations, the backslashes should be escaped.

Finally the environment variables are should be included so as to be used to receive and send emails via POP3 and SMTP.