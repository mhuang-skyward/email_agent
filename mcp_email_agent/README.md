# MCP Email Agent

This repository implements an MCP-based email agent that allows AI assistants to interact with email services through the Model Context Protocol (MCP). It demonstrates how to create an interactive AI application that can dynamically access external tools and data sources, specifically focusing on email operations.

## Prerequisites

- Ubuntu operating system or WSL
- Python 3.12.3
- pip (Python package installer)

## Setup

1. Clone this repository:
```
git clone https://github.com/mhuang-skyward/email_agent.git
```
```
cd MCP_Agent_Tutorial
```

2. Create a new environment and install the required dependencies:
```
python3 -m venv .venv
source .venv/bin/activate
```
```
pip install -r requirements.txt
```

If you're using WSL and encounter issues, try:
```
pip install --break-system-packages -r requirements.txt
```

3. Set up your environment variables:
```
cp .env.example .env
```

4. Open the `.env` file and add your email configuration:
- POP3 server settings
- SMTP server settings
- Email credentials
- Bedrock API keys (if using AWS Bedrock)

## Running the Application

1. In one terminal, start the server:
```
python sse_server.py
```

2. In another terminal, start the client:
```
python sse_client.py
```

The client and server are configured to connect over `localhost:5553`.

## Available MCP Tools

The MCP Email Agent implements the following tools:

### 1. pollEmails
- **Description**: Retrieves all emails from the inbox
- **Parameters**: None
- **Returns**: List of emails with headers and body content

### 2. getEmailsById
- **Description**: Retrieves specific emails by their IDs
- **Parameters**: `ids` (list of integer message IDs)
- **Returns**: Requested emails with full content

### 3. deleteEmailsById
- **Description**: Deletes specific emails from the inbox
- **Parameters**: `ids` (list of integer message IDs)
- **Returns**: Confirmation of deletion
- **Note**: Deleting emails invalidates the current order of IDs

### 4. sendTextEmail
- **Description**: Sends a plain text email
- **Parameters**:
  - `fromAddress` (string): Sender's email address
  - `toAddresses` (list of strings): Recipients' email addresses
  - `subject` (string): Email subject line
  - `body` (string): Plain text message content

### 5. sendHtmlEmail
- **Description**: Sends an HTML-formatted email
- **Parameters**:
  - `fromAddress` (string): Sender's email address
  - `toAddresses` (list of strings): Recipients' email addresses
  - `subject` (string): Email subject line
  - `body` (string): HTML-formatted message content

## Component Architecture

### Model Context Protocol Flow

1. User sends a message through the client interface
2. The language model (Claude) receives the message and evaluates whether it needs external tools
3. If a tool is needed, the model sends a structured request to the MCP Server
4. The MCP Server processes the request and executes the email operation
5. The model incorporates the tool results into its final response
6. The client displays the final response to the user

### Key Files

- **sse_server.py**: Implements the MCP server using Server-Sent Events (SSE)
- **sse_client.py**: Connects to the MCP server and manages conversations
- **email_fix.py**: Standalone function for testing email sending
- **test_email.py**: Tests SMTP authentication
- **test_smtp_settings.py**: Comprehensive SMTP connection testing
- **direct_test.py**: Tests email sending without MCP framework

## Testing and Troubleshooting

The repository includes several utility scripts to help diagnose email connectivity issues:

1. Use **test_smtp_settings.py** to verify your SMTP server configuration
2. Try **test_email.py** to test authentication without sending an email
3. Run **direct_test.py** to attempt sending a test email directly
4. If issues persist, **email_fix.py** provides fallback mechanisms for email sending

## Technical Details

The implementation uses:
- Server-Sent Events (SSE) as the transport protocol for MCP
- POP3 for retrieving emails
- SMTP for sending emails
- Python's built-in email libraries for message formatting
- Anthropic's Claude model for natural language understanding