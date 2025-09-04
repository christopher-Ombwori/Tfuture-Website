from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey
from wagtail.snippets.models import register_snippet
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


@register_snippet
class Category(models.Model):
    """Main and sub categories for projects."""
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="subcategories",
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["parent__name", "name"]

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} → {self.name}"
        return self.name


class ProjectIndexPage(Page):
    """A listing page for all projects (portfolio)."""
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    def get_context(self, request, *args, **kwargs):
        """Add child ProjectPages to context for the template."""
        context = super().get_context(request, *args, **kwargs)
        context["projects"] = ProjectPage.objects.child_of(self).live()
        context["categories"] = Category.objects.filter(parent__isnull=True)
        return context


class ProjectPage(Page):
    """A single project detail page."""

    client = models.CharField(max_length=200, blank=True)
    industry = models.CharField(max_length=200, blank=True)

    # Instead of CharField → link to Category snippet
    category = models.ForeignKey(
        "cms.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="projects",
        help_text="Select a category or subcategory from snippets."
    )

    description = RichTextField(blank=True)

    body = StreamField([
        ("heading", blocks.CharBlock(form_classname="full title")),
        ("paragraph", blocks.RichTextBlock()),
        ("image", ImageChooserBlock()),
        ("video", blocks.URLBlock(help_text="YouTube/Vimeo link")),
        ("code", blocks.TextBlock(help_text="Paste code snippet")),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("client"),
        FieldPanel("industry"),
        FieldPanel("category"),
        FieldPanel("description"),
        FieldPanel("body"),
        InlinePanel("images", label="Project Images"),
    ]


class ProjectImage(models.Model):
    """Images associated with a project."""
    project = ParentalKey(
        ProjectPage,
        related_name="images",
        on_delete=models.CASCADE,
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        related_name="+",
        on_delete=models.CASCADE,
    )
    caption = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel("image"),
        FieldPanel("caption"),
    ]

    def __str__(self):
        return self.caption or f"Image for {self.project.title}"
