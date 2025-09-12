"""
URL configuration for TFuture project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# TFuture/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from wagtail.contrib.sitemaps import views as wagtail_sitemaps_views


urlpatterns = [
    path('my-admin-futuristic', admin.site.urls),
    path('', include('core.urls')),
    path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/javascript')),
    path('brevo-frame.html', TemplateView.as_view(template_name='brevo-frame.html', content_type='text/html')),

    # Wagtail admin + docs
    path('admin/', include('wagtail.admin.urls')),
    path('documents/', include('wagtail.documents.urls')),
    path("sitemap.xml", wagtail_sitemaps_views.sitemap),

    # Wagtail page routing (keep last)
    path('', include('wagtail.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()