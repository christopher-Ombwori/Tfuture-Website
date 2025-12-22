from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import threading

from .models import Service, ServiceRequest, Testimonial
from .brevo_api import send_service_request_emails
from .brand_discovery_emails import send_brand_discovery_emails

# Wagtail imports
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.snippets.models import register_snippet
from django.core.exceptions import ValidationError
from django import forms
from wagtail.models import Page
from cms.models import ProjectPage, BlogPage, FAQItem, BrandDiscoverySubmission


def home(request):
    services = Service.objects.filter(is_visible=True).order_by('order')

    # Fetch featured items from Wagtail (latest 4)
    featured_projects = (
        ProjectPage.objects.live().public().filter(is_featured=True).order_by('-first_published_at')[:4]
    )
    featured_blogs = (
        BlogPage.objects.live().public().filter(is_featured=True).order_by('-first_published_at')[:4]
    )
    
    # Fetch featured testimonials
    featured_testimonials = Testimonial.objects.filter(featured=True).order_by('order')

    return render(request, 'core/home.html', {
        'services': services,
        'featured_projects': featured_projects,
        'featured_blogs': featured_blogs,
        'testimonials': featured_testimonials,
        'faq_items': FAQItem.objects.all().order_by('order'),
    })


def about(request):
    return render(request, 'core/about.html')


def blog(request):
    return render(request, 'core/blog.html')


def products(request):
    return render(request, 'core/products.html')
    
def get_general_inquiry_service():
    return Service.objects.filter(slug="general-inquiry").first()

@csrf_exempt
@require_http_methods(["POST"])
def submit_service_request(request):
    try:
        data = json.loads(request.body)

        # Extract form data
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone = data.get('phone')
        service_id = data.get('service_id')
        message = data.get('message')

        # Validate required fields
        if not all([first_name, last_name, email, phone, service_id, message]):
            return JsonResponse({
                'success': False,
                'message': 'All fields are required'
            }, status=400)

        # Get the service
        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Invalid service selected'
            }, status=400)

        # Save the service request
        service_request = ServiceRequest.objects.create(
            service=service,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            message=message
        )

        # Send email notifications asynchronously (non-blocking)
        def send_emails_async():
            try:
                send_service_request_emails(service_request)
            except Exception as e:
                print(f"Email sending error: {str(e)}")
        
        # Start email sending in background thread
        email_thread = threading.Thread(target=send_emails_async)
        email_thread.daemon = True
        email_thread.start()

        return JsonResponse({
            'success': True,
            'message': "Thank you! We'll get back to you within 24 hours."
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid request data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred. Please try again.'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def submit_brand_discovery(request):
    """
    Handle Brand Discovery form submissions
    """
    try:
        data = json.loads(request.body)

        # Extract core required fields
        rep_name = data.get('rep_name')
        business_name = data.get('business_name')
        email = data.get('email')
        phone = data.get('phone')

        # Validate required fields
        if not all([rep_name, business_name, email, phone]):
            return JsonResponse({
                'success': False,
                'message': 'All required fields must be filled'
            }, status=400)

        # Extract additional responses (all other fields)
        additional_responses = {}
        required_fields = {'rep_name', 'business_name', 'email', 'phone'}
        for key, value in data.items():
            if key not in required_fields:
                additional_responses[key] = value

        # Save the brand discovery submission
        submission = BrandDiscoverySubmission.objects.create(
            rep_name=rep_name,
            business_name=business_name,
            email=email,
            phone=phone,
            additional_responses=additional_responses
        )

        # Send email notifications asynchronously (non-blocking)
        def send_emails_async():
            try:
                send_brand_discovery_emails(submission)
            except Exception as e:
                print(f"Email sending error: {str(e)}")
        
        # Start email sending in background thread
        email_thread = threading.Thread(target=send_emails_async)
        email_thread.daemon = True
        email_thread.start()

        return JsonResponse({
            'success': True,
            'message': "Thank you! We'll review your information and get back to you shortly.",
            'submission_id': submission.id
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid request data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred. Please try again.'
        }, status=500)
