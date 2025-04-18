# Import the necessary function
from main import sendTextEmail

# Call the function with your email details
sendTextEmail(
    fromAddress="mhuang@skywarditsolutions.com", 
    toAddresses=["mhuang@skywarditsolutions.com"], 
    subject="Hello from Python", 
    body="Hi from Python."
)