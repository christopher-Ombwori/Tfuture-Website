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

from wagtail.snippets.models import register_snippet


@register_snippet
class FAQItem(models.Model):
    """Frequently Asked Question item editable in Wagtail."""
    question = models.CharField(max_length=255)
    answer = RichTextField()
    order = models.PositiveIntegerField(default=0)

    panels = [
        FieldPanel("question"),
        FieldPanel("answer"),
        FieldPanel("order"),
    ]

    class Meta:
        ordering = ["order", "question"]
        verbose_name = "FAQ Item"
        verbose_name_plural = "FAQ Items"

    def __str__(self):
        return self.question


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

# Premium presentation blocks (move outside ProjectPage for import order)
class KPIBlock(blocks.StructBlock):
    value = blocks.CharBlock(help_text="e.g., 32% or 2.4x")
    label = blocks.CharBlock(help_text="Short label: Conversion lift, Time-to-approve, etc.")
    description = blocks.TextBlock(required=False, help_text="Optional supporting line")

    class Meta:
        icon = "tick"
        template = "cms/blocks/kpi_block.html"
        label = "KPI"

# Lightweight section separator block
class SectionSeparatorBlock(blocks.StructBlock):
    style = blocks.ChoiceBlock(
        choices=[
            ("line", "Line Divider"),
            ("space", "Whitespace"),
            ("dots", "Dotted Divider"),
        ],
        default="line",
        help_text="Choose separator style"
    )

    class Meta:
        icon = "horizontalrule"
        template = "cms/blocks/section_separator_block.html"
        label = "Section Separator"

class TimelineItemBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    description = blocks.RichTextBlock(required=False)
    date = blocks.CharBlock(required=False, help_text="Optional date or phase label")

    class Meta:
        icon = "time"
        label = "Timeline Item"

class TimelineBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    items = blocks.ListBlock(TimelineItemBlock(), min_num=2)

    class Meta:
        icon = "date"
        template = "cms/blocks/timeline_block.html"
        label = "Timeline"

class BeforeAfterBlock(blocks.StructBlock):
    before = ImageChooserBlock()
    after = ImageChooserBlock()
    caption = blocks.CharBlock(required=False)
    start_position = blocks.IntegerBlock(default=50, help_text="Start position (0-100)")

    class Meta:
        icon = "image"
        template = "cms/blocks/before_after_block.html"
        label = "Before / After"

class CTABlock(blocks.StructBlock):
    title = blocks.CharBlock()
    body = blocks.RichTextBlock(required=False)
    button_label = blocks.CharBlock(default="Contact Us")
    button_url = blocks.URLBlock(required=False, help_text="If blank, opens contact modal")
    style = blocks.ChoiceBlock(choices=[
        ("accent", "Accent"),
        ("info", "Information"),
        ("success", "Success"),
        ("warning", "Warning"),
    ], default="accent")

    class Meta:
        icon = "site"
        template = "cms/blocks/cta_block.html"
        label = "CTA Panel"


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

    show_hero_image = models.BooleanField(
        default=True,
        help_text="Show the hero image on the project detail page (still used for thumbnails and meta images).",
    )

    hero = StreamField([
        ("hero", HeroBlock()),
    ], use_json_field=True, blank=True, default=list)

    intro = StreamField([
        ("intro", IntroBlock()),
    ], use_json_field=True, blank=True, default=list)

    # Define all allowed blocks for reuse
    project_body_blocks = [
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
            help_text="Small caption text - use for image captions or small supporting text",
            required=False
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
        ("video_embed", blocks.URLBlock(help_text="YouTube/Vimeo link")),
        ("video_embed_rich", EmbedBlock(
            icon="media",
            template="cms/blocks/video_embed_block.html",
            help_text="YouTube/Vimeo link (auto-embed)"
        )),
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
        ("section_separator", SectionSeparatorBlock()),
        ("kpi", KPIBlock()),
        ("kpi_list", blocks.ListBlock(KPIBlock(), icon="tick", template="cms/blocks/kpi_list_block.html", help_text="List of KPIs (1-6)")),
        ("before_after", BeforeAfterBlock()),
        ("timeline", TimelineBlock()),
        ("cta", CTABlock()),
        # Do NOT include "two_column" inside itself to avoid recursion
    ]

    body = StreamField(project_body_blocks + [
        ("two_column", blocks.StructBlock([
            ("left", blocks.StreamBlock(project_body_blocks, required=False)),
            ("right", blocks.StreamBlock(project_body_blocks, required=False)),
        ], icon="grip", template="cms/blocks/two_column_block.html")),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("category"),
        FieldPanel("is_featured"),
        FieldPanel("behance_link"),
        FieldPanel("show_hero_image"),
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
        blank=False,
        on_delete=models.PROTECT,
        related_name="+",
        help_text="Required - used for previews and social sharing"
    )
    show_featured_image = models.BooleanField(
        default=True,
        help_text="Display featured image on the blog page (always shown in previews)"
    )

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
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("category"),
            FieldPanel("tags"),
        ], heading="Organization"),
        MultiFieldPanel([
            FieldPanel("featured_image"),
            FieldPanel("show_featured_image"),
        ], heading="Featured Image"),
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

# ==========================
# Brand Discovery Form
# ==========================

class FormQuestionBlock(blocks.StructBlock):
    """Base structure for form questions with type-specific rendering"""
    label = blocks.CharBlock(
        required=True,
        help_text="Question label (e.g., 'What is your company size?')"
    )
    field_type = blocks.ChoiceBlock(
        choices=[
            ("text", "Short Text"),
            ("textarea", "Long Text"),
            ("email", "Email"),
            ("phone", "Phone Number"),
            ("number", "Number"),
            ("dropdown", "Dropdown"),
            ("checkbox", "Checkbox"),
        ],
        help_text="Select the input type for this question"
    )
    required = blocks.BooleanBlock(
        required=False,
        default=True,
        help_text="Is this field required?"
    )
    help_text = blocks.CharBlock(
        required=False,
        blank=True,
        help_text="Optional helper text below the label"
    )
    # For dropdown and checkbox: comma-separated options
    options = blocks.CharBlock(
        required=False,
        blank=True,
        help_text="For dropdown/checkbox: comma-separated options (e.g., 'Option 1, Option 2, Option 3')"
    )

    class Meta:
        icon = "form"
        label = "Form Question"


class FormSectionBlock(blocks.StructBlock):
    """A section containing multiple form questions"""
    section_title = blocks.CharBlock(
        required=True,
        help_text="Title for this section (e.g., 'Detailed Overview')"
    )
    section_description = blocks.CharBlock(
        required=False,
        blank=True,
        help_text="Optional description text for the section"
    )
    questions = blocks.ListBlock(
        FormQuestionBlock(),
        help_text="Add questions for this section"
    )

    class Meta:
        icon = "folder-open-1"
        label = "Form Section"


class BrandDiscoveryPage(Page):
    """
    Dynamic brand discovery form page managed in Wagtail.
    Allows adding custom form sections with questions that users can fill out.
    """
    
    intro = RichTextField(
        blank=True,
        help_text="Introduction text to display at the top of the form"
    )
    
    # Dynamic form sections
    form_sections = StreamField(
        [("section", FormSectionBlock())],
        blank=True,
        use_json_field=True,
        help_text="Add form sections with questions. Reorder as needed."
    )
    
    # Post-submission message
    thank_you_message = RichTextField(
        blank=True,
        default="<p>Thank you for your inquiry! We'll review your information and get back to you shortly.</p>",
        help_text="Message shown after successful form submission"
    )
    
    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("form_sections"),
        FieldPanel("thank_you_message"),
    ]
    
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = []
    
    template = "cms/brand_discovery_page.html"
    
    def get_form_sections_list(self):
        """Return form sections as a list for easy access"""
        return [block.value for block in self.form_sections]


class BrandDiscoverySubmission(models.Model):
    """
    Stores submissions from the Brand Discovery form.
    Flexible to handle any combination of questions.
    """
    
    # Core required fields
    rep_name = models.CharField(max_length=200, help_text="Name of business representative")
    business_name = models.CharField(max_length=200, help_text="Name of the business")
    email = models.EmailField(help_text="Email for confirmation")
    phone = models.CharField(max_length=30, help_text="Phone number")
    
    # Flexible field for additional responses (stored as JSON)
    additional_responses = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional form responses stored as JSON"
    )
    
    # Meta
    status = models.CharField(
        max_length=20,
        choices=[
            ("new", "New"),
            ("reviewed", "Reviewed"),
            ("in_progress", "In Progress"),
            ("completed", "Completed"),
        ],
        default="new",
        help_text="Status of this inquiry"
    )
    admin_notes = models.TextField(
        blank=True,
        help_text="Internal notes for this submission"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    panels = [
        FieldPanel("rep_name", read_only=True),
        FieldPanel("business_name", read_only=True),
        FieldPanel("email", read_only=True),
        FieldPanel("phone", read_only=True),
        FieldPanel("status"),
        FieldPanel("admin_notes"),
    ]
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Brand Discovery Submission"
        verbose_name_plural = "Brand Discovery Submissions"
    
    def __str__(self):
        return f"{self.business_name} - {self.rep_name} ({self.get_status_display()})"


class PrivacyPolicyPage(Page):
    """
    Privacy Policy page composed of structured clauses.
    The page header/title is fixed in the template; editors add clauses only.
    """

    description = RichTextField(
        blank=True,
        help_text="Brief description shown below the title (optional)"
    )

    clauses = StreamField(
        [
            (
                "clause",
                blocks.StructBlock(
                    [
                        ("title", blocks.CharBlock(required=True, help_text="Clause title")),
                        (
                            "body",
                            blocks.RichTextBlock(
                                required=True,
                                help_text="Clause content",
                                features=[
                                    "h2",
                                    "h3",
                                    "bold",
                                    "italic",
                                    "link",
                                    "ul",
                                    "ol",
                                    "hr",
                                    "code",
                                ],
                            ),
                        ),
                    ],
                    icon="form",
                    label="Clause",
                ),
            )
        ],
        blank=True,
        use_json_field=True,
        help_text="Add privacy policy clauses (title + content)",
    )

    updates_log = StreamField(
        [
            (
                "update",
                blocks.StructBlock(
                    [
                        ("at", blocks.DateTimeBlock(required=True, help_text="Exact update timestamp")),
                        ("by", blocks.CharBlock(required=False, help_text="Updated by (username)", max_length=255)),
                        ("note", blocks.TextBlock(required=False, help_text="Optional note (e.g., what changed)")),
                    ],
                    icon="date",
                    label="Update Entry",
                ),
            )
        ],
        blank=True,
        use_json_field=True,
        help_text="Internal log of updates (backend only)",
    )

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        FieldPanel("clauses"),
        FieldPanel("updates_log", read_only=True),
    ]

    parent_page_types = ["wagtailcore.Page"]
    subpage_types = []

    template = "cms/privacy_policy_page.html"

    class Meta:
        verbose_name = "Privacy Policy"
        verbose_name_plural = "Privacy Policies"


class TermsOfServicePage(Page):
    """
    Terms of Service page composed of structured clauses.
    The page header/title is fixed in the template; editors add clauses only.
    """

    description = RichTextField(
        blank=True,
        help_text="Brief description shown below the title (optional)"
    )

    clauses = StreamField(
        [
            (
                "clause",
                blocks.StructBlock(
                    [
                        ("title", blocks.CharBlock(required=True, help_text="Clause title")),
                        (
                            "body",
                            blocks.RichTextBlock(
                                required=True,
                                help_text="Clause content",
                                features=[
                                    "h2",
                                    "h3",
                                    "bold",
                                    "italic",
                                    "link",
                                    "ul",
                                    "ol",
                                    "hr",
                                    "code",
                                ],
                            ),
                        ),
                    ],
                    icon="form",
                    label="Clause",
                ),
            )
        ],
        blank=True,
        use_json_field=True,
        help_text="Add terms of service clauses (title + content)",
    )

    updates_log = StreamField(
        [
            (
                "update",
                blocks.StructBlock(
                    [
                        ("at", blocks.DateTimeBlock(required=True, help_text="Exact update timestamp")),
                        ("by", blocks.CharBlock(required=False, help_text="Updated by (username)", max_length=255)),
                        ("note", blocks.TextBlock(required=False, help_text="Optional note (e.g., what changed)")),
                    ],
                    icon="date",
                    label="Update Entry",
                ),
            )
        ],
        blank=True,
        use_json_field=True,
        help_text="Internal log of updates (backend only)",
    )

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        FieldPanel("clauses"),
        FieldPanel("updates_log", read_only=True),
    ]

    parent_page_types = ["wagtailcore.Page"]
    subpage_types = []

    template = "cms/terms_of_service_page.html"

    class Meta:
        verbose_name = "Terms of Service"
        verbose_name_plural = "Terms of Service"