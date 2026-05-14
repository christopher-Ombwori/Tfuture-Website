from django.core.management.base import BaseCommand
from django.utils.text import slugify
from wagtail.models import Page
from wagtail.images.models import Image
from cms.models import BlogIndexPage, BlogPage, BlogCategory, BlogPageTag
from taggit.models import Tag
import os


class Command(BaseCommand):
    help = "Create sample blog posts with different content styles"

    def handle(self, *args, **options):
        # Get or create categories
        strategy_cat, _ = BlogCategory.objects.get_or_create(
            name="Brand Strategy",
            defaults={"slug": "brand-strategy"}
        )
        design_cat, _ = BlogCategory.objects.get_or_create(
            name="Design Insights",
            defaults={"slug": "design-insights"}
        )
        case_study_cat, _ = BlogCategory.objects.get_or_create(
            name="Case Study",
            defaults={"slug": "case-study"}
        )

        # Get blog index page
        try:
            blog_index = BlogIndexPage.objects.first()
        except:
            self.stdout.write(self.style.ERROR("BlogIndexPage not found. Please create it first."))
            return

        # Get a featured image - use the first available image
        try:
            # Try to find a suitable image, fallback to first available
            featured_image = Image.objects.filter(title__icontains="Asset_10").first() or Image.objects.first()
        except:
            self.stdout.write(self.style.WARNING("Could not find images. Using first available image."))
            featured_image = Image.objects.first()

        if not featured_image:
            self.stdout.write(self.style.ERROR("No images found in media folder. Please upload images first."))
            return

        # Sample Blog 1: Strategy-Focused
        blog1 = BlogPage(
            title="Building a Cohesive Brand Identity: A Strategic Approach",
            slug="building-cohesive-brand-identity",
            featured_image=featured_image,
            show_featured_image=True,
            category=strategy_cat,
            intro="Learn how to create a unified visual language that resonates with your target audience and sets your brand apart in today's competitive market.",
            live=True,
        )
        blog1_body = [
            ("heading", "The Foundation of Strong Branding"),
            ("rich_text", "A cohesive brand identity goes far beyond just a logo. It encompasses your color palette, typography, imagery style, tone of voice, and every interaction your audience has with your brand. When all these elements work in harmony, they create a powerful first impression and build lasting trust."),
            ("subheading", "Why Consistency Matters"),
            ("rich_text", "Consistency is the cornerstone of effective branding. When customers see your brand repeatedly across different touchpoints—whether it's your website, social media, packaging, or in-person interactions—it reinforces recognition and builds credibility. Studies show that consistent branding can increase revenue by up to 23%."),
            ("quote", "Your brand is what people say about you when you're not in the room. - Jeff Bezos"),
            ("subheading", "Key Elements of Brand Identity"),
            ("bulleted_list", [
                "Logo Design: Your visual mark and primary identifier",
                "Color Palette: Evokes emotions and ensures instant recognition",
                "Typography: Communicates personality and professionalism",
                "Imagery Style: Consistent visual language across all media",
                "Voice & Tone: How you communicate with your audience",
                "Brand Guidelines: Documentation ensuring consistency"
            ]),
            ("subheading", "Getting Started with Your Brand Strategy"),
            ("rich_text", "Begin by defining your brand values, mission, and unique value proposition. Understand your target audience deeply—their pain points, aspirations, and preferences. Then, craft your brand identity around these insights. Remember, a strong brand strategy is not something you build in a day; it's an evolving process that requires research, creativity, and consistency."),
            ("callout", {
                "title": "Pro Tip",
                "body": "Create a comprehensive brand guide document that outlines all visual and verbal elements of your brand. This ensures consistency across your entire organization and any external partners.",
                "style": "info"
            }),
        ]
        blog1.body = blog1_body
        blog1_page = blog_index.add_child(instance=blog1)
        blog1_page.save_revision().publish()
        self.stdout.write(self.style.SUCCESS(f"✓ Created: {blog1.title}"))

        # Sample Blog 2: Design-Focused with Images
        blog2 = BlogPage(
            title="Color Psychology in Brand Design: Choosing Your Palette",
            slug="color-psychology-brand-design",
            featured_image=featured_image,
            show_featured_image=True,
            category=design_cat,
            intro="Colors aren't just aesthetically pleasing—they're psychological triggers that influence how people perceive your brand. Discover how to choose the perfect color palette that aligns with your brand values.",
            live=True,
        )
        blog2_body = [
            ("heading", "The Power of Color Psychology"),
            ("rich_text", "Every color carries psychological weight and cultural significance. Red evokes urgency and passion, blue conveys trust and stability, green represents growth and health, while yellow communicates optimism and energy. When you understand these associations, you can strategically choose colors that align with your brand personality and resonate with your target audience."),
            ("image", featured_image),
            ("caption", "Color psychology plays a crucial role in brand recognition and customer perception"),
            ("subheading", "Understanding Color Perception"),
            ("rich_text", "Research shows that up to 90% of snap judgments about products are based on color alone. This doesn't mean you need dozens of colors—in fact, the most successful brands typically use a focused palette of 2-4 primary colors with complementary accents."),
            ("stats_grid", [
                {"label": "Color Recognition", "value": "80%"},
                {"label": "Market Share Impact", "value": "65%"},
                {"label": "Emotional Association", "value": "85%"},
                {"label": "Consumer Confidence", "value": "90%"},
            ]),
            ("subheading", "Building Your Brand Color System"),
            ("rich_text", "Start with one dominant color that best represents your brand values. Add a secondary color for contrast and visual hierarchy. Include neutrals (white, gray, black) for balance and readability. Finally, choose accent colors to highlight important elements and create visual interest."),
            ("callout", {
                "title": "Color Selection Framework",
                "body": "Consider your industry, target demographic, competitor colors, cultural meanings, and accessibility standards when selecting your brand palette. Test your colors in different contexts—print, digital, backgrounds—before finalizing.",
                "style": "success"
            }),
        ]
        blog2.body = blog2_body
        blog2_page = blog_index.add_child(instance=blog2)
        blog2_page.save_revision().publish()
        self.stdout.write(self.style.SUCCESS(f"✓ Created: {blog2.title}"))

        # Sample Blog 3: Case Study with Multiple Blocks
        blog3 = BlogPage(
            title="Case Study: How TechVenture Rebranded and Increased Market Share by 40%",
            slug="techventure-rebrand-case-study",
            featured_image=featured_image,
            show_featured_image=True,
            category=case_study_cat,
            intro="See how a strategic rebrand transformed TechVenture from a struggling startup into a market leader. This case study reveals the challenges, solutions, and impressive results.",
            is_featured=True,
            live=True,
        )
        blog3_body = [
            ("heading", "The Challenge: Low Market Visibility"),
            ("rich_text", "TechVenture, a B2B SaaS company, was struggling with brand recognition despite having a solid product. Their existing brand identity felt dated, and they were losing deals to competitors with stronger visual identities. They approached us to help them reposition their brand in the market."),
            ("subheading", "Discovery & Strategy Phase"),
            ("rich_text", "We conducted in-depth interviews with their target audience, analyzed competitor brands, and assessed their current market position. The findings revealed that while TechVenture was seen as technically competent, they appeared corporate and unapproachable—exactly the opposite of what modern tech buyers wanted."),
            ("heading", "Our Solution: A Modern, Approachable Brand"),
            ("rich_text", "We developed a completely new brand identity featuring:"),
            ("bulleted_list", [
                "A dynamic, geometric logo that conveys innovation and movement",
                "A bold color palette mixing deep navy with vibrant teal accents",
                "Modern, sans-serif typography for clarity and professionalism",
                "Custom illustration style to humanize the brand",
                "Comprehensive brand guidelines for consistent application"
            ]),
            ("subheading", "Implementation & Results"),
            ("rich_text", "The rebrand was rolled out across all touchpoints: website, marketing materials, product interface, and office environment. The results exceeded expectations."),
            ("stats_grid", [
                {"label": "Website Traffic Increase", "value": "+67%"},
                {"label": "Market Share Growth", "value": "+40%"},
                {"label": "Brand Recognition", "value": "+85%"},
                {"label": "Sales Growth", "value": "+52%"},
            ]),
            ("callout", {
                "title": "Key Takeaway",
                "body": "A strategic rebrand isn't just about making things look nice—it's about positioning your company in the hearts and minds of your target audience. When done right, it can drive significant business growth.",
                "style": "accent"
            }),
            ("subheading", "The Numbers Don't Lie"),
            ("rich_text", "Within 6 months of launch, TechVenture saw a 67% increase in website traffic, a 52% increase in qualified leads, and closed deals 30% faster. More importantly, their NPS score improved from 32 to 58, indicating significantly higher customer satisfaction and loyalty."),
            ("rich_text", "This case study demonstrates the tangible ROI of strategic branding. A strong, cohesive brand identity isn't a luxury—it's a business necessity in today's competitive landscape."),
        ]
        blog3.body = blog3_body
        blog3_page = blog_index.add_child(instance=blog3)
        blog3_page.save_revision().publish()
        self.stdout.write(self.style.SUCCESS(f"✓ Created: {blog3.title}"))

        # Sample Blog 4: Tips & Tricks
        blog4 = BlogPage(
            title="10 Typography Tips Every Brand Designer Should Know",
            slug="typography-tips-brand-designers",
            featured_image=featured_image,
            show_featured_image=True,
            category=design_cat,
            intro="Typography is often overlooked, but it's one of the most powerful elements of brand design. Master these 10 tips to elevate your brand's visual impact.",
            live=True,
        )
        blog4_body = [
            ("heading", "Typography: The Art and Science"),
            ("rich_text", "While visuals grab attention, typography establishes personality and guides the reading experience. Good typography is often invisible—you notice how readable and elegant it feels, but not necessarily the specific typeface. Bad typography, however, screams for attention, usually negatively."),
            ("numbered_list", [
                "Choose typefaces with purpose: Serif fonts feel traditional, sans-serifs feel modern, and script fonts feel elegant or playful",
                "Limit your font choices: Use 2-3 typefaces maximum. One for headlines, one for body text, possibly one for accents",
                "Ensure readability: Large enough font sizes, adequate line spacing (1.5-1.6 for body text), and sufficient contrast",
                "Create visual hierarchy: Use size, weight, and color to guide readers through content",
                "Mind the whitespace: Typography is as much about space around text as the text itself",
                "Test across devices: What looks good on desktop might not work on mobile",
                "Consider accessibility: Sufficient contrast ratios and readable font sizes aid users with visual impairments",
                "Align intentionally: Left, right, center, and justified alignment each create different feelings",
                "Use kerning and tracking: Adjust spacing between letters for a more polished look",
                "Keep it consistent: Use your typography system throughout all brand touchpoints"
            ]),
            ("callout", {
                "title": "Practical Exercise",
                "body": "Pick your favorite website or brand. Analyze their typography choices. What typefaces do they use? How do they create hierarchy? What emotions does it evoke? This practice trains your eye for quality typography.",
                "style": "info"
            }),
        ]
        blog4.body = blog4_body
        blog4_page = blog_index.add_child(instance=blog4)
        blog4_page.save_revision().publish()
        self.stdout.write(self.style.SUCCESS(f"✓ Created: {blog4.title}"))

        self.stdout.write(
            self.style.SUCCESS("\n✅ All sample blogs created successfully! Visit the blog admin to view them.") 
        )
