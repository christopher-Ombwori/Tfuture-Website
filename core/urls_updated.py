from django.urls import path
from . import views
from .api import get_services, get_service_detail

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('blog/', views.blog, name='blog'),
    path('terms/', views.terms, name='terms'),
    path('about/', views.about, name='about'),
    # path('contact/', views.contact, name='contact'),
    path('submit-service-request/', views.submit_service_request, name='submit_service_request'),
    
    # API endpoints for services
    path('api/services/', get_services, name='api_services'),
    path('api/services/<slug:slug>/', get_service_detail, name='api_service_detail'),
]

app_name = 'core'