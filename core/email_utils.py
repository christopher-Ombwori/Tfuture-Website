from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import logging

logger = logging.getLogger(__name__)

def send_email_via_smtp(to_email, subject, html_content, from_email=None, from_name=None):
    """
    Send email using Brevo SMTP
    """
    try:
        # Create email message
        email = EmailMessage(
            subject=subject,
            body=html_content,
            from_email=f"{from_name or settings.DEFAULT_FROM_NAME} <{from_email or settings.DEFAULT_FROM_EMAIL}>",
            to=[to_email],
        )
        email.content_subtype = "html"  # Main content is now text/html
        
        # Send the email
        email.send()
        logger.info(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending email to {to_email}: {e}")
        return False

def send_admin_notification(service_request):
    """
    Send notification email to admin about new service request
    """
    try:
        # Prepare context for admin notification
        context = {
            'first_name': service_request.first_name,
            'last_name': service_request.last_name,
            'email': service_request.email,
            'phone': service_request.phone,
            'service_name': service_request.service.name,
            'message': service_request.message,
            'created_at': service_request.created_at,
            'admin_url': f"{settings.SITE_URL}/admin/core/servicerequest/{service_request.id}/"
        }
        
        # Render the email template
        html_content = render_to_string('core/emails/admin_notification.html', context)
        
        # Send email to admin
        subject = f"New Service Request: {service_request.service.name} - {service_request.first_name} {service_request.last_name}"
        
        success = send_email_via_smtp(
            to_email=settings.ADMIN_EMAIL,
            subject=subject,
            html_content=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            from_name=settings.DEFAULT_FROM_NAME
        )
        
        if success:
            logger.info(f"Admin notification sent for service request {service_request.id}")
        else:
            logger.error(f"Failed to send admin notification for service request {service_request.id}")
            
        return success
        
    except Exception as e:
        logger.error(f"Error sending admin notification: {e}")
        return False

def send_customer_confirmation(service_request):
    """
    Send confirmation email to customer
    """
    try:
        # Prepare context for customer confirmation
        context = {
            'first_name': service_request.first_name,
            'last_name': service_request.last_name,
            'email': service_request.email,
            'service_name': service_request.service.name,
            'request_id': service_request.id,
            'created_at': service_request.created_at,
        }
        
        # Render the email template
        html_content = render_to_string('core/emails/customer_confirmation.html', context)
        
        # Send email to customer
        subject = f"Service Request Confirmation - TFuture"
        
        success = send_email_via_smtp(
            to_email=service_request.email,
            subject=subject,
            html_content=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            from_name=settings.DEFAULT_FROM_NAME
        )
        
        if success:
            logger.info(f"Customer confirmation sent for service request {service_request.id}")
        else:
            logger.error(f"Failed to send customer confirmation for service request {service_request.id}")
            
        return success
        
    except Exception as e:
        logger.error(f"Error sending customer confirmation: {e}")
        return False

def send_service_request_emails(service_request):
    """
    Send both admin notification and customer confirmation emails
    """
    admin_sent = send_admin_notification(service_request)
    customer_sent = send_customer_confirmation(service_request)
    
    return {
        'admin_notification_sent': admin_sent,
        'customer_confirmation_sent': customer_sent,
        'all_sent': admin_sent and customer_sent
    } 