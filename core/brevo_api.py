import requests
import logging
from django.conf import settings
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)

class BrevoAPI:
    """
    Brevo API client for sending transactional emails
    """
    API_URL = "https://api.brevo.com/v3/smtp/email"
    
    @staticmethod
    def send_email(to_email, to_name, subject, html_content, from_email=None, from_name=None):
        """
        Send email using Brevo API
        """
        try:
            # Set default from email and name if not provided
            from_email = from_email or settings.DEFAULT_FROM_EMAIL
            from_name = from_name or settings.DEFAULT_FROM_NAME
            
            # Prepare API payload
            payload = {
                "sender": {
                    "name": from_name,
                    "email": from_email
                },
                "to": [
                    {
                        "email": to_email,
                        "name": to_name
                    }
                ],
                "subject": subject,
                "htmlContent": html_content
            }
            
            # Set API headers with API key
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "api-key": settings.BREVO_API_KEY
            }
            
            # Make API request
            response = requests.post(BrevoAPI.API_URL, json=payload, headers=headers)
            
            # Check if request was successful
            if response.status_code in [200, 201, 202]:
                logger.info(f"Email sent successfully to {to_email}")
                return {
                    "success": True,
                    "message_id": response.json().get("messageId"),
                    "status_code": response.status_code
                }
            else:
                logger.error(f"Failed to send email to {to_email}. Status code: {response.status_code}, Response: {response.text}")
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "error": response.text
                }
                
        except Exception as e:
            logger.error(f"Error sending email to {to_email}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

def send_service_request_confirmation(service_request):
    """
    Send confirmation email to customer who submitted a service request
    """
    try:
        # Prepare context for customer confirmation
        context = {
            'first_name': service_request.first_name,
            'last_name': service_request.last_name,
            'email': service_request.email,
            'service_name': service_request.service.name,
            'message': service_request.message,
            'request_id': service_request.id,
            'created_at': service_request.created_at,
        }
        
        # Render the email template
        html_content = render_to_string('core/emails/customer_confirmation.html', context)
        
        # Send email to customer
        subject = f"Service Request Confirmation - TFuture"
        
        result = BrevoAPI.send_email(
            to_email=service_request.email,
            to_name=f"{service_request.first_name} {service_request.last_name}",
            subject=subject,
            html_content=html_content
        )
        
        if result["success"]:
            logger.info(f"Customer confirmation sent for service request {service_request.id}")
        else:
            logger.error(f"Failed to send customer confirmation for service request {service_request.id}")
            
        return result
        
    except Exception as e:
        logger.error(f"Error sending customer confirmation: {str(e)}")
        return {"success": False, "error": str(e)}

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
            'request_id': service_request.id,
            'admin_url': f"{settings.SITE_URL}/admin/core/servicerequest/{service_request.id}/"
        }
        
        # Render the email template
        html_content = render_to_string('core/emails/admin_notification.html', context)
        
        # Send email to admin
        subject = f"New Service Request: {service_request.service.name} - {service_request.first_name} {service_request.last_name}"
        
        result = BrevoAPI.send_email(
            to_email=settings.ADMIN_EMAIL,
            to_name="TFuture Admin",
            subject=subject,
            html_content=html_content
        )
        
        if result["success"]:
            logger.info(f"Admin notification sent for service request {service_request.id}")
        else:
            logger.error(f"Failed to send admin notification for service request {service_request.id}")
            
        return result
        
    except Exception as e:
        logger.error(f"Error sending admin notification: {str(e)}")
        return {"success": False, "error": str(e)}

def send_service_request_emails(service_request):
    """
    Send both admin notification and customer confirmation emails
    Returns a dictionary with the status of each email and whether all were sent
    """
    admin_result = send_admin_notification(service_request)
    customer_result = send_service_request_confirmation(service_request)
    
    return {
        'admin_notification_sent': admin_result["success"],
        'customer_confirmation_sent': customer_result["success"],
        'all_sent': admin_result["success"] and customer_result["success"],
        'admin_result': admin_result,
        'customer_result': customer_result
    }

# ==========================
# Brand Discovery Email Functions
# ==========================

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
        subject = "Brand Discovery Inquiry Confirmation - TFuture"
        
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
