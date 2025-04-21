import os
import smtplib
import ssl
from dotenv import load_dotenv

def test_smtp_connection():
    """Test SMTP connection with various configurations"""
    load_dotenv()  # Load environment variables
    
    # Get credentials from environment
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    
    print(f"Attempting connection to: {smtp_server}:{smtp_port}")
    print(f"Using credentials: {email_user}")
    
    # Try method 1: Standard with STARTTLS
    try:
        print("\nMethod 1: Standard SMTP with STARTTLS")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.set_debuglevel(1)  # Enable verbose debug output
        server.ehlo()  # Identify to the server
        if server.has_extn('STARTTLS'):
            server.starttls()  # Enable encryption
            server.ehlo()  # Re-identify over secure connection
            server.login(email_user, email_pass)
            print("Method 1: Authentication successful!")
        else:
            print("Method 1: STARTTLS not supported")
        server.quit()
    except Exception as e:
        print(f"Method 1 failed: {str(e)}")
    
    # Try method 2: Direct SSL
    try:
        print("\nMethod 2: SMTP_SSL (Direct SSL)")
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL(smtp_server, 465, context=context)
        server.set_debuglevel(1)
        server.login(email_user, email_pass)
        print("Method 2: Authentication successful!")
        server.quit()
    except Exception as e:
        print(f"Method 2 failed: {str(e)}")
    
    # Try method 3: Different port
    try:
        print("\nMethod 3: SMTP with port 25")
        server = smtplib.SMTP(smtp_server, 25)
        server.set_debuglevel(1)
        server.ehlo()
        if server.has_extn('STARTTLS'):
            server.starttls()
            server.ehlo()
        server.login(email_user, email_pass)
        print("Method 3: Authentication successful!")
        server.quit()
    except Exception as e:
        print(f"Method 3 failed: {str(e)}")

if __name__ == "__main__":
    test_smtp_connection()