# Migration: add TermsOfServicePage model
from django.db import migrations
import wagtail.fields
import wagtail.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("cms", "0024_alter_privacypolicypage_clauses"),
        ("wagtailcore", "0095_groupsitepermission"),
    ]

    operations = [
        migrations.CreateModel(
            name="TermsOfServicePage",
            fields=[
                ("page_ptr", wagtail.fields.models.OneToOneField(auto_created=True, on_delete=wagtail.fields.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to="wagtailcore.page")),
                ("clauses", wagtail.fields.StreamField([
                    ("clause", wagtail.blocks.StructBlock([
                        ("title", wagtail.blocks.CharBlock(required=True, help_text="Clause title")),
                        ("body", wagtail.blocks.RichTextBlock(required=True, help_text="Clause content", features=["h2", "h3", "bold", "italic", "link", "ul", "ol", "hr", "code"])),
                    ], icon="form", label="Clause")),
                ], blank=True, use_json_field=True, help_text="Add terms of service clauses (title + content)")),
                ("updates_log", wagtail.fields.StreamField([
                    ("update", wagtail.blocks.StructBlock([
                        ("at", wagtail.blocks.DateTimeBlock(required=True, help_text="Exact update timestamp")),
                        ("by", wagtail.blocks.CharBlock(required=False, help_text="Updated by (username)", max_length=255)),
                        ("note", wagtail.blocks.TextBlock(required=False, help_text="Optional note (e.g., what changed)")),
                    ], icon="date", label="Update Entry")),
                ], blank=True, use_json_field=True, help_text="Internal log of updates (backend only)")),
            ],
            options={
                "verbose_name": "Terms of Service",
                "verbose_name_plural": "Terms of Service",
            },
            bases=("wagtailcore.page",),
        ),
    ]
