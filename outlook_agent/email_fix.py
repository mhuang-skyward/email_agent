import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

def send_test_email():
    """Send a test email using the proper configuration for Outlook"""
    load_dotenv()  # Load environment variables
    
    # Get credentials from environment
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")
    smtp_server = os.getenv("SMTP_SERVER", "smtp-mail.outlook.com")
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_user  # Send to self for testing
    msg['Subject'] = "Test Email from Python"
    
    body = "This is a test email sent from Python to verify SMTP settings."
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # Use SSL connection on port 465
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, 465, context=context) as server:
            print(f"Connecting to {smtp_server}:465 using SSL")
            server.login(email_user, email_pass)
            print("Authentication successful!")
            
            server.send_message(msg)
            print("Email sent successfully!")
            return True
    except Exception as e:
        print(f"Failed with SSL connection: {str(e)}")
        
        # Fall back to TLS connection on port 587
        try:
            with smtplib.SMTP(smtp_server, 587) as server:
                print(f"\nRetrying with {smtp_server}:587 using STARTTLS")
                server.ehlo('example.com')  # Use a valid domain for EHLO
                server.starttls(context=context)
                server.ehlo('example.com')  # Re-identify after STARTTLS
                
                server.login(email_user, email_pass)
                print("Authentication successful!")
                
                server.send_message(msg)
                print("Email sent successfully!")
                return True
        except Exception as e2:
            print(f"Failed with TLS connection: {str(e2)}")
            return False

if __name__ == "__main__":
    send_test_email()