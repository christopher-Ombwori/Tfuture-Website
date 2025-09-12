#!/usr/bin/env python
"""
Test script for Brevo API email functionality
Run this to test if your Brevo API configuration is working
"""

import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TFuture.settings')
django.setup()

# Import after Django setup
from core.brevo_api import BrevoAPI

def check_api_key():
    """
    Check if Brevo API key is configured
    """
    print("\n🔍 Checking Brevo API Configuration...")
    print("=" * 50)
    
    if not hasattr(settings, 'BREVO_API_KEY') or not settings.BREVO_API_KEY:
        print("❌ BREVO_API_KEY is not configured in settings")
        print("Please add your Brevo API key to your .env file:")
        print("BREVO_API_KEY=your-api-key-here")
        return False
    
    print(f"✅ BREVO_API_KEY is configured")
    
    # Check other required settings
    if not settings.DEFAULT_FROM_EMAIL:
        print("⚠️ DEFAULT_FROM_EMAIL is not set")
    else:
        print(f"✅ DEFAULT_FROM_EMAIL is set to: {settings.DEFAULT_FROM_EMAIL}")
    
    if not settings.DEFAULT_FROM_NAME:
        print("⚠️ DEFAULT_FROM_NAME is not set")
    else:
        print(f"✅ DEFAULT_FROM_NAME is set to: {settings.DEFAULT_FROM_NAME}")
    
    if not settings.ADMIN_EMAIL:
        print("⚠️ ADMIN_EMAIL is not set")
    else:
        print(f"✅ ADMIN_EMAIL is set to: {settings.ADMIN_EMAIL}")
    
    return True

def test_send_email():
    """
    Test sending a simple email using Brevo API
    """
    print("\n🧪 Testing Brevo API Email Sending...")
    print("=" * 50)
    
    try:
        # Create a simple test email
        subject = "🧪 Test Email - TFuture Brevo API"
        html_content = """
        <html>
        <body>
            <h2>🎉 Brevo API Test Successful!</h2>
            <p>This is a test email from your TFuture website using the Brevo API.</p>
            <p>If you received this email, your Brevo API configuration is working perfectly!</p>
            <hr>
            <p><strong>Test Details:</strong></p>
            <ul>
                <li>API: Brevo API v3</li>
                <li>Endpoint: /smtp/email</li>
                <li>From: {from_name} &lt;{from_email}&gt;</li>
                <li>To: {to_email}</li>
            </ul>
        </body>
        </html>
        """.format(
            from_name=settings.DEFAULT_FROM_NAME,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_email=settings.ADMIN_EMAIL
        )
        
        # Send the email
        result = BrevoAPI.send_email(
            to_email=settings.ADMIN_EMAIL,
            to_name="TFuture Admin",
            subject=subject,
            html_content=html_content
        )
        
        if result["success"]:
            print(f"✅ Email sent successfully!")
            print(f"📧 Check your email at: {settings.ADMIN_EMAIL}")
            print(f"📝 Message ID: {result.get('message_id')}")
            return True
        else:
            print(f"❌ Email test failed: {result.get('error')}")
            print(f"Status code: {result.get('status_code')}")
            return False
        
    except Exception as e:
        print(f"❌ Email test failed with exception: {str(e)}")
        return False

def main():
    """
    Main test function
    """
    print("🔍 TFuture Brevo API Email Test")
    print("=" * 50)
    
    # Check API key configuration
    if not check_api_key():
        print("\n❌ Brevo API configuration check failed. Please fix the issues above.")
        return
    
    # Test sending email
    email_success = test_send_email()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"  API Configuration: {'✅ PASS' if check_api_key() else '❌ FAIL'}")
    print(f"  Email Sending: {'✅ PASS' if email_success else '❌ FAIL'}")
    
    if email_success:
        print("\n✅ All tests passed! Your Brevo API email setup is working correctly.")
        print("📧 If you're not receiving emails, check your spam folder.")
    else:
        print("\n❌ Some tests failed. Please check the error messages above.")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()