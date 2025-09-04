from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from modelcluster.fields import ParentalKey
from wagtail.snippets.models import register_snippet
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class HeroBlock(blocks.StructBlock):
    label = blocks.CharBlock(required=True, help_text="Small label above the headline")
    headline = blocks.CharBlock(required=True, help_text="Main project headline")
    tags = blocks.ListBlock(blocks.CharBlock(required=True), help_text="Tags shown next to the hero")
    hero_image = ImageChooserBlock(required=True)

    class Meta:
        icon = "title"
        label = "Hero"


class IntroBlock(blocks.StructBlock):
    subheading = blocks.CharBlock(required=True, help_text="Muted subheading")
    context = blocks.RichTextBlock(required=True, help_text="Intro/context paragraph")

    class Meta:
        icon = "openquote"
        label = "Intro"


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

    # Used only for listing-page filtering, not displayed on detail page
    category = models.ForeignKey(
        "cms.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="projects",
        help_text="Select a category or subcategory from snippets."
    )

    hero = StreamField([
        ("hero", HeroBlock()),
    ], use_json_field=True, blank=True, default=list)

    intro = StreamField([
        ("intro", IntroBlock()),
    ], use_json_field=True, blank=True, default=list)

    body = StreamField([
        ("heading", blocks.CharBlock(form_classname="full title")),
        ("muted_subheading", blocks.CharBlock(help_text="Muted subheading")),
        ("rich_text", blocks.RichTextBlock()),
        ("quote", blocks.BlockQuoteBlock()),
        ("image", ImageChooserBlock()),
        ("image_with_caption", blocks.StructBlock([
            ("image", ImageChooserBlock()),
            ("caption", blocks.CharBlock(required=False)),
        ])),
        ("image_grid", blocks.ListBlock(blocks.StructBlock([
            ("image", ImageChooserBlock()),
            ("caption", blocks.CharBlock(required=False)),
        ]), help_text="Add 2-6 images")),
        ("video_embed", blocks.URLBlock(help_text="YouTube/Vimeo link")),
        ("two_column", blocks.StructBlock([
            ("left", blocks.StreamBlock([
                ("rich_text", blocks.RichTextBlock()),
                ("image", ImageChooserBlock()),
                ("quote", blocks.BlockQuoteBlock()),
                ("code", blocks.TextBlock(help_text="Code")),
            ], required=False)),
            ("right", blocks.StreamBlock([
                ("rich_text", blocks.RichTextBlock()),
                ("image", ImageChooserBlock()),
                ("quote", blocks.BlockQuoteBlock()),
                ("code", blocks.TextBlock(help_text="Code")),
            ], required=False)),
        ])),
        ("stats_grid", blocks.ListBlock(blocks.StructBlock([
            ("label", blocks.CharBlock()),
            ("value", blocks.CharBlock()),
        ]), help_text="Small set of key stats")),
        ("bulleted_list", blocks.ListBlock(blocks.CharBlock())),
        ("callout", blocks.StructBlock([
            ("title", blocks.CharBlock()),
            ("body", blocks.RichTextBlock()),
        ])),
        ("code", blocks.TextBlock(help_text="Paste code snippet")),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("category"),
        FieldPanel("hero"),
        FieldPanel("intro"),
        FieldPanel("body"),
    ]


class ProjectImage(models.Model):
    """Deprecated: previously associated gallery images (kept for legacy migrations)."""
    project = ParentalKey(
        ProjectPage,
        related_name="legacy_images",
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
