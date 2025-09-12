from django.http import JsonResponse
from .models import Service


def get_services(request):
    """
    API endpoint to get all visible services.
    This allows the frontend to consume service data without changing the existing logic.
    """
    services = Service.objects.filter(is_visible=True).order_by('order')
    
    services_data = [{
        'id': service.id,
        'name': service.name,
        'slug': service.slug,
        'short_description': service.short_description,
        'icon_svg': service.icon_svg,
        'is_featured': service.is_featured,
    } for service in services]
    
    return JsonResponse({
        'services': services_data
    })


def get_service_detail(request, slug):
    """
    API endpoint to get details for a specific service.
    """
    try:
        service = Service.objects.get(slug=slug, is_visible=True)
        
        service_data = {
            'id': service.id,
            'name': service.name,
            'slug': service.slug,
            'description': service.description,
            'short_description': service.short_description,
            'icon_svg': service.icon_svg,
            'is_featured': service.is_featured,
        }
        
        return JsonResponse({
            'service': service_data
        })
    except Service.DoesNotExist:
        return JsonResponse({
            'error': 'Service not found'
        }, status=404)