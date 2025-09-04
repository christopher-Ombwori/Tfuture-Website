from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from wagtail.snippets.models import register_snippet
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


@register_snippet
class Service(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = RichTextField(blank=True)
    short_description = models.CharField(max_length=300, blank=True)
    icon_svg = models.TextField(blank=True, help_text="Paste the full SVG code including <svg> tags.")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("description"),
        FieldPanel("short_description"),
        FieldPanel("icon_svg"),
        MultiFieldPanel([
            FieldPanel("is_active"),
            FieldPanel("order"),
            FieldPanel("is_featured"),
        ], heading="Display Options"),
    ]

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("service_detail", kwargs={"slug": self.slug})


@register_snippet
class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("in_progress", "In Progress"),
        ("contacted", "Contacted"),
        ("completed", "Completed"),
        ("spam", "Spam"),
        ("cancelled", "Cancelled"),
    ]

    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="requests")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    admin_notes = models.TextField(blank=True, help_text="Internal notes for this request")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel("service"),
        FieldPanel("first_name"),
        FieldPanel("last_name"),
        FieldPanel("email"),
        FieldPanel("phone"),
        FieldPanel("message"),
        FieldPanel("status"),
        FieldPanel("admin_notes"),
    ]

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.service.name} ({self.get_status_display()})"
