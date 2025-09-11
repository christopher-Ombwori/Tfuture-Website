from cms.models import ProjectIndexPage, BlogIndexPage, ProductsPage

def global_pages(request):
    our_work_page = ProjectIndexPage.objects.live().first()
    blog_index_page = BlogIndexPage.objects.live().first()
    products_page = ProductsPage.objects.live().first()
    return {
        "our_work_page": our_work_page,
        "blog_index_page": blog_index_page,
        "products_page": products_page,
    }

from .models import Service

def general_inquiry(request):
    return {
        "general_inquiry": Service.objects.filter(slug="general-inquiry").first()
    }
