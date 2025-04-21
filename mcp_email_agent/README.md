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
cd mcp_email_agent
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

## Project Structure

```
mcp_email_agent/
│
├── email_agent_utils.py    # Email helper functions and utilities
├── requirements.txt        # Project dependencies
├── sse_client.py           # MCP client implementation
├── sse_server.py           # MCP server with email tools
│
└── tests/                  # Test utilities
    ├── __init__.py
    ├── direct_test.py                # Test email sending without MCP
    ├── test_email.py                 # Test SMTP authentication
    ├── test_email_with_fallback.py   # Test email with fallback mechanisms
    ├── test_mcp_tools.py             # Pytest tests for all MCP tools
    └── test_smtp_settings.py         # Test SMTP configurations
```

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

## Testing and Troubleshooting

### Manual Email Testing

The repository includes several utility scripts in the `tests/` directory to help diagnose email connectivity issues:

1. Use `tests/test_smtp_settings.py` to verify your SMTP server configuration
2. Try `tests/test_email.py` to test authentication without sending an email
3. Run `tests/direct_test.py` to attempt sending a test email directly
4. Use `tests/test_email_with_fallback.py` for robust email testing with automatic fallback

You can run these manual tests with:
```
python -m tests.test_email
python -m tests.test_smtp_settings
python -m tests.direct_test
python -m tests.test_email_with_fallback
```

### Unit Tests

The repository also includes pytest-based unit tests for the MCP tools:

```
pytest tests/test_mcp_tools.py
```

These tests use mocking to verify the functionality of all MCP tools without needing to connect to actual email servers. You can also run individual tests:

```
pytest tests/test_mcp_tools.py::test_poll_emails
pytest tests/test_mcp_tools.py::test_send_text_email
```

## Technical Details

The implementation uses:
- Server-Sent Events (SSE) as the transport protocol for MCP
- POP3 for retrieving emails
- SMTP for sending emails
- Python's built-in email libraries for message formatting
- Anthropic's Claude model for natural language understanding