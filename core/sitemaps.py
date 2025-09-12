from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Service, Testimonial
from wagtail.models import Page
from wagtail.contrib.sitemaps.sitemap_generator import Sitemap as WagtailSitemap

class ServiceSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        # Only include visible services
        return Service.objects.filter(is_visible=True)

    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        # Since we don't have a direct URL for services in the current setup,
        # we'll use a URL pattern that makes sense for the site structure
        # This should be updated to match your actual URL structure
        return f'/services/{obj.slug}/'
        # Alternatively, if services are shown on the home page with anchors:
        # return f'/#service-{obj.slug}'

class StaticViewSitemap(Sitemap):
    priority = 0.6
    changefreq = "weekly"

    def items(self):
        # Return list of url names for views that don't use models
        return ['core:home', 'core:about', 'core:terms']

    def location(self, item):
        return reverse(item)


class WagtailPageSitemap(Sitemap):
    priority = 0.8
    changefreq = "always"
    
    def items(self):
        # Get all live pages excluding root
        return Page.objects.live().public().order_by('path').specific()
    
    def lastmod(self, obj):
        # Use the latest revision date
        return obj.last_published_at
    
    def location(self, obj):
        # Use the page's URL
        return obj.get_url()
    
    def _get_wagtail_sitemap(self):
        # Helper method to access Wagtail's sitemap if needed
        return WagtailSitemap()