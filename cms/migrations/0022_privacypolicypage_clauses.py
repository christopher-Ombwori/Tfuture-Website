# Generated migration to switch PrivacyPolicyPage to clauses StreamField

from django.db import migrations
import wagtail.fields
import wagtail.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("cms", "0021_privacypolicypage"),
        ("wagtailcore", "0095_groupsitepermission"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="privacypolicypage",
            name="body",
        ),
        migrations.AddField(
            model_name="privacypolicypage",
            name="clauses",
            field=wagtail.fields.StreamField([
                ("clause", wagtail.blocks.StructBlock([
                    ("title", wagtail.blocks.CharBlock(required=True, help_text="Clause title")),
                    ("body", wagtail.blocks.RichTextBlock(required=True, help_text="Clause content")),
                ], icon="form", label="Clause")),
            ], blank=True, use_json_field=True, help_text="Add privacy policy clauses (title + content)"),
        ),
    ]
