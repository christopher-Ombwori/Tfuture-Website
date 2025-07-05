#!/usr/bin/env python
"""
Test script for email functionality
Run this to test if your Brevo SMTP configuration is working
"""

import os
import sys
import django
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TFuture.settings')
django.setup()

def test_email_configuration():
    """Test the email configuration"""
    print("🧪 Testing Email Configuration...")
    print("=" * 50)
    
    # Check environment variables
    print("📧 Email Settings:")
    print(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"  EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")
    print(f"  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"  DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print(f"  ADMIN_EMAIL: {settings.ADMIN_EMAIL}")
    print()

def test_simple_email():
    """Test sending a simple email"""
    print("📤 Testing Simple Email...")
    
    try:
        # Create a simple test email
        subject = "🧪 Test Email - TFuture Email System"
        message = """
        <html>
        <body>
            <h2>🎉 Email Test Successful!</h2>
            <p>This is a test email from your TFuture website.</p>
            <p>If you received this email, your Brevo SMTP configuration is working perfectly!</p>
            <hr>
            <p><strong>Test Details:</strong></p>
            <ul>
                <li>SMTP Server: smtp-relay.brevo.com</li>
                <li>Port: 2525</li>
                <li>From: contact@tfuturedesigns.studio</li>
                <li>To: {admin_email}</li>
            </ul>
        </body>
        </html>
        """.format(admin_email=settings.ADMIN_EMAIL)
        
        # Send the email
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=f"TFuture <{settings.DEFAULT_FROM_EMAIL}>",
            to=[settings.ADMIN_EMAIL],
        )
        email.content_subtype = "html"
        
        # Send and check result
        result = email.send()
        print(f"✅ Email sent successfully! Result: {result}")
        print(f"📧 Check your email at: {settings.ADMIN_EMAIL}")
        
    except Exception as e:
        print(f"❌ Email test failed: {str(e)}")
        return False
    
    return True

def test_template_email():
    """Test sending an email using our templates"""
    print("\n📤 Testing Template Email...")
    
    try:
        # Create test data
        test_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'phone': '+1234567890',
            'service_name': 'Brand Strategies & Identity Systems',
            'message': 'This is a test message to verify the email templates are working correctly.',
            'created_at': django.utils.timezone.now(),
            'request_id': 12345,
            'admin_url': 'http://localhost:8000/admin/core/servicerequest/12345/'
        }
        
        # Test admin notification template
        admin_html = render_to_string('core/emails/admin_notification.html', test_data)
        
        subject = "🧪 Template Test - Admin Notification"
        
        email = EmailMessage(
            subject=subject,
            body=admin_html,
            from_email=f"TFuture <{settings.DEFAULT_FROM_EMAIL}>",
            to=[settings.ADMIN_EMAIL],
        )
        email.content_subtype = "html"
        
        result = email.send()
        print(f"✅ Admin notification template test successful! Result: {result}")
        
        # Test customer confirmation template
        customer_html = render_to_string('core/emails/customer_confirmation.html', test_data)
        
        subject = "🧪 Template Test - Customer Confirmation"
        
        email = EmailMessage(
            subject=subject,
            body=customer_html,
            from_email=f"TFuture <{settings.DEFAULT_FROM_EMAIL}>",
            to=[settings.ADMIN_EMAIL],  # Send to admin for testing
        )
        email.content_subtype = "html"
        
        result = email.send()
        print(f"✅ Customer confirmation template test successful! Result: {result}")
        
    except Exception as e:
        print(f"❌ Template email test failed: {str(e)}")
        return False
    
    return True

def main():
    """Main test function"""
    print("🪄 TFuture Email System Test")
    print("=" * 50)
    
    # Test 1: Configuration
    test_email_configuration()
    
    # Test 2: Simple email
    simple_success = test_simple_email()
    
    # Test 3: Template emails
    template_success = test_template_email()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"  Simple Email: {'✅ PASS' if simple_success else '❌ FAIL'}")
    print(f"  Template Email: {'✅ PASS' if template_success else '❌ FAIL'}")
    
    if simple_success and template_success:
        print("\n🎉 All tests passed! Your magical email system is working perfectly!")
        print("📧 Check your email at:", settings.ADMIN_EMAIL)
    else:
        print("\n⚠️  Some tests failed. Please check your configuration.")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main() 