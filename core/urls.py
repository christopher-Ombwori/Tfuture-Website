from django.urls import path
from . import views

app_name = 'core'
 
urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('blog/', views.blog, name='blog'),
    path('terms/', views.terms, name='terms'),
    path('about/', views.about, name='about'),
    path('submit-service-request/', views.submit_service_request, name='submit_service_request'),
    # path('contact/', views.contact, name='contact'),
] 