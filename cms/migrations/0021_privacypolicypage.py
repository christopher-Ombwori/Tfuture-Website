# Generated migration for PrivacyPolicyPage model

import wagtail.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0020_remove_branddiscoverypage_form_questions_and_more'),
        ('wagtailcore', '0095_groupsitepermission'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivacyPolicyPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.fields.RichTextField(help_text='Privacy policy content')),
            ],
            options={
                'verbose_name': 'Privacy Policy',
                'verbose_name_plural': 'Privacy Policies',
            },
            bases=('wagtailcore.page',),
        ),
    ]
