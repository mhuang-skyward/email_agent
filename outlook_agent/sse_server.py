from typing import List
from mcp.server.fastmcp import FastMCP
from mcp.types import Tool
from dotenv import load_dotenv
import os
import aiohttp
from email.parser import Parser
import poplib
import smtplib

load_dotenv()

# Initialize MCP server
mcp = FastMCP("SimpleMCPServer")

# Email constants
FORMAT_HEADERS = "FORMAT_HEADERS"
FORMAT_MESSAGE = "FORMAT_MESSAGE"
FORMAT_COMBINED = "FORMAT_COMBINED"

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
        # Get credentials directly from environment at execution time
        email_user = os.getenv("EMAIL_USER")
        email_pass = os.getenv("EMAIL_PASS")
        smtp_server = os.getenv("SMTP_SERVER")
        
        # Debug output to tool result
        debug_info = f"Using credentials: {email_user} with server {smtp_server}\n"
        
        # Import email modules for better formatting
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        import ssl
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = fromAddress
        msg['To'] = ", ".join(toAddresses)
        msg['Subject'] = subject
        
        # Attach body
        msg.attach(MIMEText(body, 'plain'))
        
        # Try SSL connection first (port 465)
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, 465, context=context) as server:
                server.login(email_user, email_pass)
                server.send_message(msg)
                return f"{debug_info}Email sent successfully via SSL (port 465)!"
        except Exception as ssl_error:
            debug_info += f"SSL connection failed: {str(ssl_error)}\nTrying TLS instead...\n"
            
            # Fall back to TLS connection (port 587)
            try:
                with smtplib.SMTP(smtp_server, 587) as server:
                    server.ehlo('example.com')  # Use a valid domain for EHLO
                    server.starttls(context=context)
                    server.ehlo('example.com')
                    server.login(email_user, email_pass)
                    server.send_message(msg)
                    return f"{debug_info}Email sent successfully via TLS (port 587)!"
            except Exception as tls_error:
                return f"{debug_info}Error sending email via TLS: {str(tls_error)}"
    except Exception as e:
        return f"Error preparing email: {str(e)}"


async def list_tools() -> List[Tool]:
    """List the tools available to the LLM."""
    return [
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
        )
    ]

# Start MCP server with SSE transport
if __name__ == "__main__":
    mcp.run(transport="sse")