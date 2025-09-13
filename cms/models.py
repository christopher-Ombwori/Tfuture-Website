from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from modelcluster.fields import ParentalKey
from wagtail.snippets.models import register_snippet
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.search import index
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.contrib.table_block.blocks import TableBlock

# Import the Testimonial model from core app
from core.models import Testimonial


class HeroBlock(blocks.StructBlock):
    label = blocks.CharBlock(required=True, help_text="Small label above the headline")
    headline = blocks.CharBlock(required=True, help_text="Main project headline")
    tags = blocks.ListBlock(blocks.CharBlock(required=True), help_text="Tags shown next to the hero")
    hero_image = ImageChooserBlock(required=True)

    class Meta:
        icon = "title"
        label = "Hero"


class IntroBlock(blocks.StructBlock):
    subheading = blocks.CharBlock(required=False, help_text="Normal subheading (H2 size)")
    muted_subheading = blocks.CharBlock(required=False, help_text="Muted subheading (H3 size)")
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


from .seo_extension import ProjectSEOExtension

class ProjectPage(Page, ProjectSEOExtension):
    """A single project detail page with enhanced SEO for TFuture Designs brand differentiation."""

    # Used only for listing-page filtering, not displayed on detail page
    category = models.ForeignKey(
        "cms.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="projects",
        help_text="Select a category or subcategory from snippets."
    )

    # Whether this project should be shown as featured on the homepage
    is_featured = models.BooleanField(default=False, help_text="Feature this project on the homepage")
    
    # Optional Behance link for the project
    behance_link = models.URLField(max_length=255, blank=True, null=True, help_text="Optional link to the project on Behance")

    hero = StreamField([
        ("hero", HeroBlock()),
    ], use_json_field=True, blank=True, default=list)

    intro = StreamField([
        ("intro", IntroBlock()),
    ], use_json_field=True, blank=True, default=list)

    body = StreamField([
        ("heading", blocks.CharBlock(form_classname="full title")),
        ("subheading", blocks.CharBlock(help_text="Normal subheading (H2 size)")),
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
        FieldPanel("is_featured"),
        FieldPanel("behance_link"),
        FieldPanel("hero"),
        FieldPanel("intro"),
        FieldPanel("body"),
    ]
    
    # Add the SEO panels from our extension
    promote_panels = Page.promote_panels + [
        FieldPanel("seo_brand_keywords"),
        FieldPanel("seo_kenya_focus"),
        FieldPanel("seo_africa_focus"),
        FieldPanel("seo_industry_differentiator"),
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


# ==========================
# Blog models
# ==========================


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Blog categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "cms.BlogPage",
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    subpage_types = ["cms.BlogPage"]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        posts = BlogPage.objects.child_of(self).live().order_by("-first_published_at")

        # Filters
        category_slug = request.GET.get("category")
        tag_name = request.GET.get("tag")
        if category_slug:
            posts = posts.filter(category__slug=category_slug)
        if tag_name:
            posts = posts.filter(tags__name=tag_name)

        # Simple pagination
        try:
            page_number = int(request.GET.get("page", 1))
        except ValueError:
            page_number = 1
        per_page = 9
        start = (page_number - 1) * per_page
        end = start + per_page
        context["posts"] = posts[start:end]
        context["page"] = page_number
        context["has_next"] = posts.count() > end
        context["has_prev"] = start > 0
        context["categories"] = BlogCategory.objects.all()
        context["current_category"] = category_slug
        context["current_tag"] = tag_name
        return context


class BlogPage(Page, index.Indexed):
    # Preview fields
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    excerpt = models.TextField(blank=True, help_text="Short summary for listings and social.")

    # Whether this blog post should be shown as featured on the homepage
    is_featured = models.BooleanField(default=False, help_text="Feature this blog on the homepage")

    # Content
    category = models.ForeignKey(
        "cms.BlogCategory",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="blog_posts",
    )
    body = StreamField([
        ("heading", blocks.CharBlock(
            form_classname="full title",
            icon="title",
            template="cms/blocks/heading_block.html",
            help_text="Main heading (H1 size) - use sparingly for major section breaks"
        )),
        ("subheading", blocks.CharBlock(
            icon="title", 
            template="cms/blocks/subheading_block.html",
            help_text="Normal subheading (H2 size) - use for section headings"
        )),
        ("muted_subheading", blocks.CharBlock(
            icon="title", 
            template="cms/blocks/muted_subheading_block.html",
            help_text="Muted subheading (H3 size) - use for subsection headings"
        )),
        ("caption", blocks.CharBlock(
            icon="form", 
            template="cms/blocks/caption_block.html",
            help_text="Small caption text - use for image captions or small supporting text"
        )),
        ("rich_text", blocks.RichTextBlock(
            icon="doc-full",
            template="cms/blocks/rich_text_block.html",
            help_text="Main paragraph text - use for regular content"
        )),
        ("quote", blocks.BlockQuoteBlock(
            icon="openquote",
            template="cms/blocks/quote_block.html",
            help_text="Blockquote - use for testimonials or highlighting important statements"
        )),
        ("pullquote", blocks.StructBlock([
            ("quote", blocks.TextBlock(help_text="The main quote text")),
            ("attribution", blocks.CharBlock(required=False, help_text="Who said or wrote this quote")),
        ], icon="openquote", template="cms/blocks/pullquote_block.html", help_text="Styled pullquote with attribution")),
        ("image", ImageChooserBlock(
            icon="image",
            template="cms/blocks/image_block.html",
            help_text="Full width image"
        )),
        ("image_with_caption", blocks.StructBlock([
            ("image", ImageChooserBlock()),
            ("caption", blocks.CharBlock(required=False)),
        ], icon="image", template="cms/blocks/image_with_caption_block.html")),
        ("image_grid", blocks.ListBlock(blocks.StructBlock([
            ("image", ImageChooserBlock()),
            ("caption", blocks.CharBlock(required=False)),
        ]), icon="grip", template="cms/blocks/image_grid_block.html", help_text="Add 2-6 images")),
        ("video_embed", EmbedBlock(
            icon="media",
            template="cms/blocks/video_embed_block.html",
            help_text="YouTube/Vimeo link"
        )),
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
        ], icon="grip", template="cms/blocks/two_column_block.html")),
        ("stats_grid", blocks.ListBlock(blocks.StructBlock([
            ("label", blocks.CharBlock()),
            ("value", blocks.CharBlock()),
        ]), icon="list-ul", template="cms/blocks/stats_grid_block.html", help_text="Small set of key stats")),
        ("bulleted_list", blocks.ListBlock(
            blocks.CharBlock(),
            icon="list-ul",
            template="cms/blocks/bulleted_list_block.html",
            help_text="Use for unordered list items"
        )),
        ("numbered_list", blocks.ListBlock(
            blocks.CharBlock(),
            icon="list-ol",
            template="cms/blocks/numbered_list_block.html",
            help_text="Use for ordered list items"
        )),
        ("callout", blocks.StructBlock([
            ("title", blocks.CharBlock()),
            ("body", blocks.RichTextBlock()),
            ("style", blocks.ChoiceBlock(choices=[
                ("info", "Information (Blue)"),
                ("warning", "Warning (Orange)"),
                ("success", "Success (Green)"),
                ("accent", "Accent (Cyan)"),
            ], default="accent")),
        ], icon="warning", template="cms/blocks/callout_block.html")),
        ("code", blocks.TextBlock(
            icon="code",
            template="cms/blocks/code_block.html",
            help_text="Paste code snippet"
        )),
        ("table", TableBlock(
            icon="table",
            template="cms/blocks/table_block.html",
            help_text="Add a formatted table"
        )),
    ], use_json_field=True, blank=True)

    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField("title"),
        index.SearchField("excerpt"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("category"),
            FieldPanel("tags"),
        ], heading="Organization"),
        MultiFieldPanel([
            FieldPanel("featured_image"),
            FieldPanel("excerpt"),
        ], heading="Preview"),
        FieldPanel("is_featured"),
        FieldPanel("body"),
    ]

    parent_page_types = ["cms.BlogIndexPage"]
    subpage_types = []


# ==========================
# Products page
# ==========================


class ProductsPage(Page):
    """Products landing page managed in Wagtail."""

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    parent_page_types = ["wagtailcore.Page"]
    subpage_types = []
