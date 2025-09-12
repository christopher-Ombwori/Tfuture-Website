import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from pathlib import Path
from django.template.loader import render_to_string
from django.utils import timezone


def test_admin_notification_template():
    """
    Test the admin notification email template by sending a test email.
    This script can be run independently to verify the template rendering.
    """
    # Test data to replace template variables
    context = {
        'name': 'Test User',
        'email': 'test@example.com',
        'phone': '+1 (555) 123-4567',
        'service': 'Website Design',
        'message': 'This is a test message to verify the admin notification template styling and layout. '
                  'Please check that all sections are displayed correctly and the design matches the customer template.',
        'admin_url': 'https://tfuturedesigns.studio/admin/',
        'created_at': timezone.now(),
    }
    
    # Render the template with test data
    template_path = 'templates/core/emails/admin_notification.html'
    with open(template_path, 'r', encoding='utf-8') as file:
        template_content = file.read()
    
    # Replace template variables manually
    for key, value in context.items():
        if key == 'created_at':
            # Format date and time
            date_str = value.strftime('%B %d, %Y')
            time_str = value.strftime('%I:%M %p')
            template_content = template_content.replace('{{ created_at|date:"F j, Y" }}', date_str)
            template_content = template_content.replace('{{ created_at|time:"g:i A" }}', time_str)
        else:
            template_content = template_content.replace('{{ ' + key + ' }}', str(value))
    
    # Email configuration
    sender_email = input("Enter sender email: ")
    sender_password = input("Enter sender password: ")
    recipient_email = input("Enter recipient email for testing: ")
    
    # Create message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'TEST: Admin Notification Template'
    msg['From'] = sender_email
    msg['To'] = recipient_email
    
    # Attach HTML content
    html_part = MIMEText(template_content, 'html')
    msg.attach(html_part)
    
    # Send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print(f"\nTest email sent successfully to {recipient_email}")
        print("Please check the email to verify the template design.")
    except Exception as e:
        print(f"\nError sending email: {e}")


if __name__ == "__main__":
    print("\nAdmin Notification Template Test")
    print("================================\n")
    print("This script will send a test email using the admin notification template.")
    print("You'll need to provide email credentials for sending the test.\n")
    
    test_admin_notification_template()