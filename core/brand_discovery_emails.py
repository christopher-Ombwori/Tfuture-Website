"""
Brand Discovery email handling functions using Brevo API
"""

import logging
from django.conf import settings
from django.template.loader import render_to_string
from .brevo_api import BrevoAPI

logger = logging.getLogger(__name__)


def send_brand_discovery_customer_confirmation(submission):
    """
    Send confirmation email to customer who submitted a brand discovery form
    """
    try:
        # Prepare context for customer confirmation
        context = {
            'rep_name': submission.rep_name,
            'business_name': submission.business_name,
            'email': submission.email,
            'phone': submission.phone,
            'submission_id': submission.id,
            'created_at': submission.created_at,
        }
        
        # Render the email template
        html_content = render_to_string('core/emails/brand_discovery_customer_confirmation.html', context)
        
        # Send email to customer
        subject = "Brand Discovery Form Submission Confirmation - TFuture"
        
        result = BrevoAPI.send_email(
            to_email=submission.email,
            to_name=submission.rep_name,
            subject=subject,
            html_content=html_content
        )
        
        if result["success"]:
            logger.info(f"Customer confirmation sent for brand discovery submission {submission.id}")
        else:
            logger.error(f"Failed to send customer confirmation for brand discovery submission {submission.id}")
            
        return result
        
    except Exception as e:
        logger.error(f"Error sending brand discovery customer confirmation: {str(e)}")
        return {"success": False, "error": str(e)}


def send_brand_discovery_admin_notification(submission):
    """
    Send notification email to admin about new brand discovery submission
    """
    try:
        # Prepare context for admin notification
        context = {
            'rep_name': submission.rep_name,
            'business_name': submission.business_name,
            'email': submission.email,
            'phone': submission.phone,
            'additional_responses': submission.additional_responses,
            'created_at': submission.created_at,
            'submission_id': submission.id,
            'admin_url': f"{settings.SITE_URL}/admin/cms/branddiscoverysubmission/{submission.id}/"
        }
        
        # Render the email template
        html_content = render_to_string('core/emails/brand_discovery_admin_notification.html', context)
        
        # Send email to admin
        subject = f"New Brand Discovery Inquiry: {submission.business_name} - {submission.rep_name}"
        
        result = BrevoAPI.send_email(
            to_email=settings.ADMIN_EMAIL,
            to_name="TFuture Admin",
            subject=subject,
            html_content=html_content
        )
        
        if result["success"]:
            logger.info(f"Admin notification sent for brand discovery submission {submission.id}")
        else:
            logger.error(f"Failed to send admin notification for brand discovery submission {submission.id}")
            
        return result
        
    except Exception as e:
        logger.error(f"Error sending brand discovery admin notification: {str(e)}")
        return {"success": False, "error": str(e)}


def send_brand_discovery_emails(submission):
    """
    Send both admin notification and customer confirmation emails for brand discovery
    Returns a dictionary with the status of each email and whether all were sent
    """
    admin_result = send_brand_discovery_admin_notification(submission)
    customer_result = send_brand_discovery_customer_confirmation(submission)
    
    return {
        'admin_notification_sent': admin_result["success"],
        'customer_confirmation_sent': customer_result["success"],
        'all_sent': admin_result["success"] and customer_result["success"],
        'admin_result': admin_result,
        'customer_result': customer_result
    }
