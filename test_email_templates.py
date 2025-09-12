#!/usr/bin/env python
"""
Test script for email templates rendering
This script tests both customer confirmation and admin notification templates
"""

import os
import sys
import django
import webbrowser
import tempfile
from pathlib import Path
from django.conf import settings
from django.template.loader import render_to_string

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TFuture.settings')
django.setup()

def test_template_rendering(template_name, context, output_name):
    """
    Test rendering of a template and open in browser
    """
    print(f"\n🧪 Testing {template_name} template rendering...")
    print("=" * 50)
    
    try:
        # Render the template
        html_content = render_to_string(template_name, context)
        
        # Create a temporary file to view the rendered template
        temp_dir = Path(tempfile.gettempdir())
        output_file = temp_dir / f"{output_name}.html"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Open in browser
        print(f"✅ Template rendered successfully!")
        print(f"📂 Saved to: {output_file}")
        print(f"🌐 Opening in browser for visual inspection...")
        webbrowser.open(output_file.as_uri())
        
        return True
        
    except Exception as e:
        print(f"❌ Template rendering failed: {str(e)}")
        return False

def test_customer_confirmation():
    """
    Test customer confirmation email template
    """
    # Sample context for customer confirmation
    context = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'service_name': 'Website Design',
        'request_id': '12345',
        'created_at': '2023-06-15 14:30:00',
    }
    
    return test_template_rendering(
        'core/emails/customer_confirmation.html',
        context,
        'customer_confirmation_test'
    )

def test_admin_notification():
    """
    Test admin notification email template
    """
    # Sample context for admin notification
    context = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'phone': '+1 (555) 123-4567',
        'service_name': 'Website Design',
        'message': 'I need a professional website for my new business. Looking for a modern design with e-commerce capabilities.',
        'created_at': '2023-06-15 14:30:00',
        'admin_url': 'http://localhost:8000/admin/core/servicerequest/12345/'
    }
    
    return test_template_rendering(
        'core/emails/admin_notification.html',
        context,
        'admin_notification_test'
    )

def main():
    """
    Main test function
    """
    print("🔍 TFuture Email Templates Test")
    print("=" * 50)
    
    # Test customer confirmation template
    customer_success = test_customer_confirmation()
    
    # Test admin notification template
    admin_success = test_admin_notification()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"  Customer Confirmation Template: {'✅ PASS' if customer_success else '❌ FAIL'}")
    print(f"  Admin Notification Template: {'✅ PASS' if admin_success else '❌ FAIL'}")
    
    if customer_success and admin_success:
        print("\n✅ All templates rendered successfully!")
        print("📧 Please check the browser windows to verify the visual appearance.")
        print("📱 For comprehensive testing, consider using an email testing service like Litmus or Email on Acid.")
    else:
        print("\n❌ Some templates failed to render. Please check the error messages above.")
    
    print("\n" + "=" * 50)
    print("📋 Email Template Testing Checklist:")
    print("  1. ✓ Verify all images and icons are displaying correctly")
    print("  2. ✓ Check that styles are properly applied")
    print("  3. ✓ Ensure responsive design works on different screen sizes")
    print("  4. ✓ Confirm all dynamic content is properly rendered")
    print("  5. ✓ Test with actual email sending via Brevo API")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()