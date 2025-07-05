#!/usr/bin/env python
"""
Detailed email diagnostic script
This will help us figure out why emails aren't being delivered
"""

import os
import sys
import django
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TFuture.settings')
django.setup()

def test_smtp_connection():
    """Test direct SMTP connection"""
    print("🔍 Testing Direct SMTP Connection...")
    print("=" * 50)
    
    try:
        # Create SMTP connection
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=10)
        print(f"✅ Connected to {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
        
        # Start TLS if required
        if settings.EMAIL_USE_TLS:
            server.starttls()
            print("✅ TLS started successfully")
        
        # Login
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        print("✅ Login successful")
        
        # Test sending a simple message
        msg = MIMEMultipart()
        msg['From'] = settings.DEFAULT_FROM_EMAIL
        msg['To'] = settings.ADMIN_EMAIL
        msg['Subject'] = "🔍 SMTP Connection Test"
        
        body = f"""
        <html>
        <body>
            <h2>SMTP Connection Test</h2>
            <p>This email was sent using direct SMTP connection to test if the issue is with Django's email backend.</p>
            <p><strong>Connection Details:</strong></p>
            <ul>
                <li>Host: {settings.EMAIL_HOST}</li>
                <li>Port: {settings.EMAIL_PORT}</li>
                <li>TLS: {settings.EMAIL_USE_TLS}</li>
                <li>SSL: {settings.EMAIL_USE_SSL}</li>
                <li>User: {settings.EMAIL_HOST_USER}</li>
            </ul>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        # Send the email
        text = msg.as_string()
        server.sendmail(settings.DEFAULT_FROM_EMAIL, settings.ADMIN_EMAIL, text)
        print("✅ Direct SMTP email sent successfully")
        
        server.quit()
        return True
        
    except Exception as e:
        print(f"❌ SMTP connection failed: {str(e)}")
        return False

def test_django_email_backend():
    """Test Django's email backend"""
    print("\n🔍 Testing Django Email Backend...")
    print("=" * 50)
    
    try:
        # Create email backend
        backend = EmailBackend(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS,
            use_ssl=settings.EMAIL_USE_SSL,
            timeout=10
        )
        
        # Test connection
        backend.open()
        print("✅ Django email backend connection successful")
        
        # Test sending
        email = EmailMessage(
            subject="🔍 Django Backend Test",
            body="<h2>Django Email Backend Test</h2><p>This email was sent using Django's email backend.</p>",
            from_email=f"TFuture <{settings.DEFAULT_FROM_EMAIL}>",
            to=[settings.ADMIN_EMAIL],
        )
        email.content_subtype = "html"
        
        result = email.send()
        print(f"✅ Django backend email sent successfully! Result: {result}")
        
        backend.close()
        return True
        
    except Exception as e:
        print(f"❌ Django email backend failed: {str(e)}")
        return False

def check_email_settings():
    """Display all email settings"""
    print("\n📧 Email Settings Check...")
    print("=" * 50)
    
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'NOT SET'}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print(f"ADMIN_EMAIL: {settings.ADMIN_EMAIL}")
    print()

def check_spam_filters():
    """Provide tips for checking spam filters"""
    print("\n📮 Spam Filter Check Tips...")
    print("=" * 50)
    print("If emails aren't arriving, check these places:")
    print("1. 📧 Check your SPAM/JUNK folder")
    print("2. 📧 Check your TRASH folder")
    print("3. 📧 Check your FILTERS in email settings")
    print("4. 📧 Check if emails are being BLOCKED by your email provider")
    print("5. 📧 Try sending to a different email address (Gmail, Outlook, etc.)")
    print()

def test_different_recipient():
    """Test sending to a different email address"""
    print("\n🧪 Testing Different Recipient...")
    print("=" * 50)
    
    # You can change this to test with a different email
    test_email = input("Enter a different email address to test (or press Enter to skip): ").strip()
    
    if test_email:
        try:
            email = EmailMessage(
                subject="🧪 Test Email - Different Recipient",
                body="<h2>Test Email</h2><p>This is a test email to a different address.</p>",
                from_email=f"TFuture <{settings.DEFAULT_FROM_EMAIL}>",
                to=[test_email],
            )
            email.content_subtype = "html"
            
            result = email.send()
            print(f"✅ Test email sent to {test_email}! Result: {result}")
            print(f"📧 Check your email at: {test_email}")
            
        except Exception as e:
            print(f"❌ Failed to send to {test_email}: {str(e)}")
    else:
        print("Skipping different recipient test.")

def main():
    """Main diagnostic function"""
    print("🔍 TFuture Email Diagnostic Tool")
    print("=" * 50)
    
    # Check settings
    check_email_settings()
    
    # Test direct SMTP
    smtp_success = test_smtp_connection()
    
    # Test Django backend
    django_success = test_django_email_backend()
    
    # Test different recipient
    test_different_recipient()
    
    # Spam filter tips
    check_spam_filters()
    
    print("\n" + "=" * 50)
    print("📊 Diagnostic Results:")
    print(f"  Direct SMTP: {'✅ PASS' if smtp_success else '❌ FAIL'}")
    print(f"  Django Backend: {'✅ PASS' if django_success else '❌ FAIL'}")
    
    if smtp_success and django_success:
        print("\n✅ Both tests passed! Emails are being sent successfully.")
        print("📧 If you're not receiving emails, check your spam folder or try a different email address.")
    else:
        print("\n❌ Some tests failed. There might be a configuration issue.")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main() 