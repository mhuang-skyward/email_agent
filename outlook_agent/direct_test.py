import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

def send_direct_test():
    """Test sending email directly without MCP"""
    load_dotenv()  # Load environment variables
    
    # Get credentials from environment
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")
    smtp_server = os.getenv("SMTP_SERVER")
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_user  # Send to self for testing
    msg['Subject'] = "Direct Test Email"
    
    body = "This is a direct test email sent from Python to verify SMTP settings."
    msg.attach(MIMEText(body, 'plain'))
    
    # Try with SSL (port 465)
    try:
        print("Trying SSL connection on port 465...")
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, 465, context=context) as server:
            server.login(email_user, email_pass)
            server.send_message(msg)
            print("Email sent successfully via SSL!")
            return True
    except Exception as ssl_error:
        print(f"SSL connection failed: {str(ssl_error)}")
    
    # Try with TLS (port 587)
    try:
        print("\nTrying TLS connection on port 587...")
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, 587) as server:
            server.ehlo('example.com')  # Use a valid domain
            server.starttls(context=context)
            server.ehlo('example.com')  # Reidentify
            server.login(email_user, email_pass)
            server.send_message(msg)
            print("Email sent successfully via TLS!")
            return True
    except Exception as tls_error:
        print(f"TLS connection failed: {str(tls_error)}")
    
    return False

if __name__ == "__main__":
    send_direct_test()