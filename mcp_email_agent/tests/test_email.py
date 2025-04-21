import os
import smtplib
from dotenv import load_dotenv

def test_smtp_auth():
    """Test SMTP authentication without sending an email"""
    load_dotenv()  # Load environment variables
    
    # Get credentials from environment
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    
    print(f"Using credentials: {email_user} at {smtp_server}:{smtp_port}")
    
    try:
        # Connect to SMTP server
        send = smtplib.SMTP(smtp_server, smtp_port)
        send.ehlo()  # Identify to the server
        send.starttls()  # Enable encryption
        send.ehlo()  # Re-identify over secure connection
        
        # Try to authenticate
        send.login(email_user, email_pass)
        print("Authentication successful!")
        
        # Close connection
        send.quit()
        return True
    except Exception as e:
        print(f"Authentication failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_smtp_auth()