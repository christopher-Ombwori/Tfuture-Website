from cms.models import ProjectIndexPage

def global_pages(request):
    our_work_page = ProjectIndexPage.objects.live().first()
    return {
        "our_work_page": our_work_page,
    }
