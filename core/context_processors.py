from cms.models import ProjectIndexPage

def global_pages(request):
    our_work_page = ProjectIndexPage.objects.live().first()
    return {
        "our_work_page": our_work_page,
    }

from .models import Service

def general_inquiry(request):
    return {
        "general_inquiry": Service.objects.filter(slug="general-inquiry").first()
    }
