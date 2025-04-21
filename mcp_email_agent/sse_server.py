"""
MCP Email Agent Server.

This module implements a Model Context Protocol (MCP) server that provides email
functionality to language models. It uses the SSE (Server-Sent Events) transport
protocol to communicate with MCP clients.

The server exposes several tools for email operations including:
- Reading emails from an inbox
- Retrieving specific emails by ID
- Deleting emails
- Sending plain text and HTML emails
"""

from typing import List
from mcp.server.fastmcp import FastMCP
from mcp.types import Tool
import aiohttp
from dotenv import load_dotenv

# Import email utility functions from our module
from email_agent_utils import (
    getEmails,
    deleteEmails,
    sendEmail
)

# Load environment variables
load_dotenv()

# Initialize MCP server
mcp = FastMCP("SimpleMCPServer")

# Tool definitions
@mcp.tool()
async def pollEmails() -> list:
    """Retrieves all emails from the inbox.
    
    Fetches every email currently in the inbox using POP3.
    
    Returns:
        list: A list of dictionaries representing all emails in the inbox.
              Each dictionary contains email headers and body content.
    """
    return getEmails([])

@mcp.tool()
async def getEmailsById(ids: list) -> list:
    """Retrieves specific emails by their IDs.
    
    Args:
        ids (list): A list of integer message IDs to retrieve.
        
    Returns:
        list: A list of dictionaries representing the requested emails.
              Each dictionary contains email headers and body content.
    """
    return getEmails(ids)

@mcp.tool()
async def deleteEmailsById(ids: list) -> list:
    """Deletes specific emails from the inbox.
    
    Note that deleting emails will invalidate the current order of IDs
    for subsequent operations.
    
    Args:
        ids (list): A list of integer message IDs to delete.
    """
    deleteEmails(ids)

@mcp.tool()
async def sendTextEmail(fromAddress: str, toAddresses: list, subject: str, body: str) -> str:
    """Sends a plain text email.
    
    Args:
        fromAddress (str): The sender's email address.
        toAddresses (list): List of recipient email addresses.
        subject (str): Email subject line.
        body (str): Plain text content for the email body.
        
    Returns:
        str: Success or error message.
    """
    try:
        result = sendEmail(fromAddress, toAddresses, "text/plain", subject, body)
        return result
    except Exception as e:
        return f"Error sending email: {str(e)}"

@mcp.tool()
async def sendHtmlEmail(fromAddress: str, toAddresses: list, subject: str, body: str) -> str:
    """Sends an HTML-formatted email.
    
    Args:
        fromAddress (str): The sender's email address.
        toAddresses (list): List of recipient email addresses.
        subject (str): Email subject line.
        body (str): HTML-formatted content for the email body.
        
    Returns:
        str: Success or error message.
    """
    try:
        result = sendEmail(fromAddress, toAddresses, "text/html", subject, body)
        return result
    except Exception as e:
        return f"Error sending HTML email: {str(e)}"


async def list_tools() -> List[Tool]:
    """List the tools available to the LLM.
    
    Defines the schema for each available tool in the MCP server.
    
    Returns:
        List[Tool]: List of Tool objects describing the available tools.
    """
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


# Start MCP server with SSE transport
if __name__ == "__main__":
    mcp.run(transport="sse")