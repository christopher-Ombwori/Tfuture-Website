from cms.models import ProjectIndexPage, BlogIndexPage, ProductsPage, PrivacyPolicyPage, TermsOfServicePage

def global_pages(request):
    our_work_page = ProjectIndexPage.objects.live().first()
    blog_index_page = BlogIndexPage.objects.live().first()
    products_page = ProductsPage.objects.live().first()
    privacy_policy_page = PrivacyPolicyPage.objects.live().first()
    terms_of_service_page = TermsOfServicePage.objects.live().first()
    return {
        "our_work_page": our_work_page,
        "blog_index_page": blog_index_page,
        "products_page": products_page,
        "privacy_policy_page": privacy_policy_page,
        "terms_of_service_page": terms_of_service_page,
    }

from .models import Service

def general_inquiry(request):
    return {
        "general_inquiry": Service.objects.filter(slug="general-inquiry").first()
    }
