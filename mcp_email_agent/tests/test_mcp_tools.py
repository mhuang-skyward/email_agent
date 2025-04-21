"""
Pytest tests for MCP Email Agent tools.

This module contains tests for the MCP tools implemented in sse_server.py.
It uses mocking to test functionality without actual email server connections.
"""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock
import asyncio

# Add parent directory to path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the MCP tools from the server
from sse_server import (
    pollEmails,
    getEmailsById,
    deleteEmailsById,
    sendTextEmail,
    sendHtmlEmail
)

# Import email utility functions that we'll mock
import email_agent_utils


# Sample test data
SAMPLE_EMAIL = {
    'id': 1,
    'From': 'sender@example.com',
    'To': 'recipient@example.com',
    'Subject': 'Test Subject',
    'Content-Type': 'text/plain',
    'body': b'This is a test email body'
}

SAMPLE_EMAIL_LIST = [SAMPLE_EMAIL]


@pytest.fixture
def mock_email_utils():
    """Fixture to mock all email utility functions."""
    with patch('email_agent_utils.getEmails') as mock_get_emails, \
         patch('email_agent_utils.deleteEmails') as mock_delete_emails, \
         patch('email_agent_utils.sendEmail') as mock_send_email:
        
        # Configure the mocks
        mock_get_emails.return_value = SAMPLE_EMAIL_LIST
        mock_delete_emails.return_value = None
        mock_send_email.return_value = "Email sent successfully"
        
        yield {
            'get_emails': mock_get_emails,
            'delete_emails': mock_delete_emails,
            'send_email': mock_send_email
        }


@pytest.mark.asyncio
async def test_poll_emails(mock_email_utils):
    """Test the pollEmails MCP tool."""
    # Call the async function
    result = await pollEmails()
    
    # Verify the mock was called with empty list
    mock_email_utils['get_emails'].assert_called_once_with([])
    
    # Verify the result
    assert result == SAMPLE_EMAIL_LIST
    assert len(result) == 1
    assert result[0]['id'] == 1
    assert result[0]['From'] == 'sender@example.com'
    assert result[0]['Subject'] == 'Test Subject'


@pytest.mark.asyncio
async def test_get_emails_by_id(mock_email_utils):
    """Test the getEmailsById MCP tool."""
    # Call the async function with a specific ID
    result = await getEmailsById([1])
    
    # Verify the mock was called with the correct ID
    mock_email_utils['get_emails'].assert_called_once_with([1])
    
    # Verify the result
    assert result == SAMPLE_EMAIL_LIST
    assert len(result) == 1
    assert result[0]['id'] == 1


@pytest.mark.asyncio
async def test_delete_emails_by_id(mock_email_utils):
    """Test the deleteEmailsById MCP tool."""
    # Call the async function with a specific ID
    await deleteEmailsById([1])
    
    # Verify the mock was called with the correct ID
    mock_email_utils['delete_emails'].assert_called_once_with([1])


@pytest.mark.asyncio
async def test_send_text_email(mock_email_utils):
    """Test the sendTextEmail MCP tool."""
    # Test data
    from_address = "sender@example.com"
    to_addresses = ["recipient1@example.com", "recipient2@example.com"]
    subject = "Test Subject"
    body = "This is a test email"
    
    # Call the async function
    result = await sendTextEmail(from_address, to_addresses, subject, body)
    
    # Verify the mock was called with the correct parameters
    mock_email_utils['send_email'].assert_called_once_with(
        from_address, to_addresses, "text/plain", subject, body
    )
    
    # Verify the result
    assert result == "Email sent successfully"


@pytest.mark.asyncio
async def test_send_html_email(mock_email_utils):
    """Test the sendHtmlEmail MCP tool."""
    # Test data
    from_address = "sender@example.com"
    to_addresses = ["recipient1@example.com", "recipient2@example.com"]
    subject = "Test HTML Email"
    body = "<html><body><h1>Test</h1><p>This is an HTML email</p></body></html>"
    
    # Call the async function
    result = await sendHtmlEmail(from_address, to_addresses, subject, body)
    
    # Verify the mock was called with the correct parameters
    mock_email_utils['send_email'].assert_called_once_with(
        from_address, to_addresses, "text/html", subject, body
    )
    
    # Verify the result
    assert result == "Email sent successfully"


@pytest.mark.asyncio
async def test_send_text_email_error_handling(mock_email_utils):
    """Test error handling in the sendTextEmail MCP tool."""
    # Configure the mock to raise an exception
    mock_email_utils['send_email'].side_effect = Exception("Test error")
    
    # Test data
    from_address = "sender@example.com"
    to_addresses = ["recipient@example.com"]
    subject = "Test Subject"
    body = "This is a test email"
    
    # Call the async function
    result = await sendTextEmail(from_address, to_addresses, subject, body)
    
    # Verify the result contains the error message
    assert "Error sending email: Test error" in result


@pytest.mark.asyncio
async def test_send_html_email_error_handling(mock_email_utils):
    """Test error handling in the sendHtmlEmail MCP tool."""
    # Configure the mock to raise an exception
    mock_email_utils['send_email'].side_effect = Exception("Test error")
    
    # Test data
    from_address = "sender@example.com"
    to_addresses = ["recipient@example.com"]
    subject = "Test Subject"
    body = "<html><body>Test</body></html>"
    
    # Call the async function
    result = await sendHtmlEmail(from_address, to_addresses, subject, body)
    
    # Verify the result contains the error message
    assert "Error sending HTML email: Test error" in result


if __name__ == "__main__":
    pytest.main()