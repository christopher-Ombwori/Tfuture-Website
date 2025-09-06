from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from wagtail.snippets.models import register_snippet
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, HelpPanel
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_delete
from django.dispatch import receiver

@register_snippet
class Service(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True , help_text="⚠️ For General Inquiry: slug MUST be 'general-inquiry'")
    description = RichTextField(blank=True)
    short_description = models.CharField(max_length=300, blank=True)
    icon_svg = models.TextField(blank=True, help_text="Paste the full SVG code including <svg> tags.")
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        HelpPanel(
            content=(
                "<p style='color:red; font-weight:bold;'>"
                "⚠️ Please ensure there is a <strong>General Inquiry</strong> service.<br>"
                "→ Slug must be <code>general-inquiry</code><br>"
                "→ Mark it as <strong>invisible</strong><br>"
                "→ Do NOT delete it."
                "</p>"
            ),
            heading="Important Notice",
        ),
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("description"),
        FieldPanel("short_description"),
        FieldPanel("icon_svg"),
        MultiFieldPanel([
            FieldPanel("is_visible"),
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
    
    def clean(self):
        # Prevent renaming the slug
        if self.pk:
            original = Service.objects.filter(pk=self.pk).first()
            if original and original.slug == "general-inquiry" and self.slug != "general-inquiry":
                raise ValidationError("The slug for 'General Inquiry' cannot be changed.")
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()  # ensures clean() is run
        super().save(*args, **kwargs)

@receiver(pre_delete, sender=Service)
def prevent_general_inquiry_deletion(sender, instance, **kwargs):
    if instance.slug == "general-inquiry":
        raise ValidationError("The 'General Inquiry' service cannot be deleted.")

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
    
    SOURCE_CHOICES = [
        ("website", "Website"),
        ("admin", "Admin"),
    ]

    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="requests")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES, default="website", help_text="Where this request originated from")
    admin_notes = models.TextField(blank=True, help_text="Internal notes for this request")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel("service", read_only=True),
        FieldPanel("first_name", read_only=True),
        FieldPanel("last_name", read_only=True),
        FieldPanel("email", read_only=True),
        FieldPanel("phone", read_only=True),
        FieldPanel("message", read_only=True),
        FieldPanel("status"),
        FieldPanel("admin_notes"),
    ]

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.service.name} ({self.get_status_display()})"

