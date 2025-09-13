from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page
from django.db import models


class ProjectSEOExtension(models.Model):
    """
    Extension for ProjectPage to add custom SEO fields focused on
    TFuture Designs brand differentiation and Kenya/Africa market.
    """
    # SEO Fields for brand differentiation
    seo_brand_keywords = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated keywords for TFuture Designs brand differentiation"
    )
    seo_kenya_focus = models.CharField(
        max_length=255,
        blank=True,
        help_text="Kenya-specific keywords or phrases for local SEO"
    )
    seo_africa_focus = models.CharField(
        max_length=255,
        blank=True,
        help_text="Africa-specific keywords or phrases for regional SEO"
    )
    seo_industry_differentiator = models.CharField(
        max_length=255,
        blank=True,
        help_text="Industry-specific terms that differentiate TFuture Designs"
    )
    
    # Panels for the admin interface
    seo_panels = [
        MultiFieldPanel([
            FieldPanel('seo_title'),
            FieldPanel('search_description'),
            FieldPanel('seo_brand_keywords'),
            FieldPanel('seo_kenya_focus'),
            FieldPanel('seo_africa_focus'),
            FieldPanel('seo_industry_differentiator'),
        ], heading="SEO & Brand Differentiation"),
    ]
    
    class Meta:
        abstract = True