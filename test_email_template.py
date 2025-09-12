import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

def test_email_template(recipient_email):
    """
    Send a test email using the customer_confirmation.html template
    to verify how it renders in different email clients.
    
    Args:
        recipient_email (str): Email address to send the test to
    """
    # Path to the email template
    template_path = Path("templates/core/emails/customer_confirmation.html")
    
    # Read the template
    with open(template_path, "r", encoding="utf-8") as file:
        template_content = file.read()
    
    # Replace template variables with test data
    test_data = {
        "first_name": "Test",
        "last_name": "User",
        "service_name": "Website Development",
        "request_id": "TEST123",
        "created_at": "2023-06-15 10:30:00"
    }
    
    # Simple template variable replacement
    # In a real Django app, you'd use the template engine
    email_content = template_content
    for key, value in test_data.items():
        email_content = email_content.replace("{{ " + key + " }}", str(value))
    
    # Handle Django template filters (simple version)
    email_content = email_content.replace("{{ created_at|date:\"F j, Y\" }}", "June 15, 2023")
    email_content = email_content.replace("{{ created_at|time:\"g:i A\" }}", "10:30 AM")
    
    # Create the email
    msg = MIMEMultipart()
    msg["Subject"] = "[TEST] TFuture Email Template"
    msg["From"] = "your-test-email@example.com"  # Replace with your email
    msg["To"] = recipient_email
    
    # Attach the HTML content
    msg.attach(MIMEText(email_content, "html"))
    
    print(f"Preparing to send test email to {recipient_email}")
    print("To send the email, you'll need to configure SMTP settings.")
    print("For testing purposes, you can use services like Mailtrap.io")
    
    # Uncomment and configure the following code to actually send the email
    """
    # SMTP Configuration (example for Mailtrap)
    smtp_server = "smtp.mailtrap.io"
    smtp_port = 2525
    smtp_username = "your-mailtrap-username"
    smtp_password = "your-mailtrap-password"
    
    # Send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.login(smtp_username, smtp_password)
        server.sendmail(msg["From"], msg["To"], msg.as_string())
        print(f"Test email sent to {recipient_email}")
    """
    
    print("\nEmail Preview (first 500 characters):")
    print(email_content[:500] + "...")
    print("\nTo test in multiple email clients, send to addresses that use different providers")
    print("(Gmail, Outlook, Yahoo, etc.) or use an email testing service like Litmus or Email on Acid.")

if __name__ == "__main__":
    # Replace with the email where you want to receive the test
    test_recipient = "your-email@example.com"
    test_email_template(test_recipient)