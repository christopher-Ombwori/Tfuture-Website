from django.urls import path
from . import views

app_name = 'core'
 
urlpatterns = [
    path('', views.home, name='home'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('products/', views.products, name='products'),
    path('terms/', views.terms, name='terms'),
    path('about/', views.about, name='about'),
    path('portfolio/<slug:slug>/', views.project_detail, name='project_detail'),
    path('submit-service-request/', views.submit_service_request, name='submit_service_request'),
    # path('contact/', views.contact, name='contact'),
] 