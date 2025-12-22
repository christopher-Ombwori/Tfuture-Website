# Migration: add updates_log to PrivacyPolicyPage
from django.db import migrations
import wagtail.fields
import wagtail.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("cms", "0022_privacypolicypage_clauses"),
        ("wagtailcore", "0095_groupsitepermission"),
    ]

    operations = [
        migrations.AddField(
            model_name="privacypolicypage",
            name="updates_log",
            field=wagtail.fields.StreamField([
                ("update", wagtail.blocks.StructBlock([
                    ("at", wagtail.blocks.DateTimeBlock(required=True, help_text="Exact update timestamp")),
                    ("by", wagtail.blocks.CharBlock(required=False, help_text="Updated by (username)", max_length=255)),
                    ("note", wagtail.blocks.TextBlock(required=False, help_text="Optional note (e.g., what changed)")),
                ], icon="date", label="Update Entry")),
            ], blank=True, use_json_field=True, help_text="Internal log of updates (backend only)"),
        ),
    ]
