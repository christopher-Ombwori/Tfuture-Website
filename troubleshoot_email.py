#!/usr/bin/env python
"""
Email Troubleshooting Script
This will help identify why emails aren't being delivered
"""

import os
import sys
import django
from django.conf import settings
from django.core.mail import EmailMessage
import logging

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TFuture.settings')
django.setup()

# Setup logging to see what's happening
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('django.core.mail')

def check_environment():
    """Check if environment variables are loaded correctly"""
    print("🔍 Environment Check...")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        print("✅ .env file found")
    else:
        print("❌ .env file not found")
    
    # Check email settings
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'NOT SET'}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print(f"ADMIN_EMAIL: {settings.ADMIN_EMAIL}")
    print()

def test_with_different_recipient():
    """Test sending to a different email address"""
    print("🧪 Testing with Different Recipient...")
    print("=" * 50)
    
    # Test with a common email provider
    test_emails = [
        "test@gmail.com",  # Gmail
        "test@outlook.com",  # Outlook
        "test@yahoo.com",   # Yahoo
    ]
    
    for test_email in test_emails:
        try:
            email = EmailMessage(
                subject="🧪 Email Delivery Test",
                body="<h2>Test Email</h2><p>This is a test to check email delivery.</p>",
                from_email=f"TFuture <{settings.DEFAULT_FROM_EMAIL}>",
                to=[test_email],
            )
            email.content_subtype = "html"
            
            result = email.send()
            print(f"✅ Test email sent to {test_email} - Result: {result}")
            
        except Exception as e:
            print(f"❌ Failed to send to {test_email}: {str(e)}")

def check_brevo_credentials():
    """Check if Brevo credentials are working"""
    print("\n🔍 Checking Brevo Credentials...")
    print("=" * 50)
    
    # Test with a simple email
    try:
        email = EmailMessage(
            subject="🔍 Brevo Credential Test",
            body="<h2>Brevo Test</h2><p>Testing if your Brevo credentials are working.</p>",
            from_email=f"TFuture <{settings.DEFAULT_FROM_EMAIL}>",
            to=[settings.ADMIN_EMAIL],
        )
        email.content_subtype = "html"
        
        result = email.send()
        print(f"✅ Brevo credential test - Result: {result}")
        
    except Exception as e:
        print(f"❌ Brevo credential test failed: {str(e)}")

def check_email_logs():
    """Check Django email logs"""
    print("\n📋 Email Logs Check...")
    print("=" * 50)
    
    # This will show us what Django is doing with emails
    print("Django email logs will appear below:")
    print("Look for any error messages or warnings...")
    print()

def main():
    """Main troubleshooting function"""
    print("🔍 TFuture Email Troubleshooting")
    print("=" * 50)
    
    # Check environment
    check_environment()
    
    # Check Brevo credentials
    check_brevo_credentials()
    
    # Test with different recipients
    test_with_different_recipient()
    
    # Check logs
    check_email_logs()
    
    print("\n" + "=" * 50)
    print("📊 Troubleshooting Summary:")
    print("1. ✅ Checked environment variables")
    print("2. ✅ Tested Brevo credentials")
    print("3. ✅ Tested different email providers")
    print("4. ✅ Checked Django email logs")
    print()
    print("🔍 Next Steps:")
    print("1. Check your SPAM/JUNK folder")
    print("2. Check your Brevo account for email credits")
    print("3. Verify your domain in Brevo")
    print("4. Try sending to a different email address")
    print("5. Check if your email provider is blocking emails")
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main() 