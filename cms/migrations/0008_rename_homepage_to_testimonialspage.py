# Generated manually

from django.db import migrations, models
import django.db.models.deletion
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0007_productspage'),
        ('wagtailcore', '0095_groupsitepermission'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestimonialsPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('testimonials', wagtail.fields.StreamField([('testimonial', 5)], blank=True, use_json_field=True, block_lookup={0: ('wagtail.blocks.CharBlock', (), {'help_text': "Person's name", 'required': True}), 1: ('wagtail.blocks.CharBlock', (), {'help_text': 'Job title and company', 'required': True}), 2: ('wagtail.blocks.CharBlock', (), {'help_text': 'Short initials for avatar circle', 'max_length': 3, 'required': True}), 3: ('wagtail.blocks.TextBlock', (), {'help_text': 'Testimonial text', 'required': True}), 4: ('wagtail.images.blocks.ImageChooserBlock', (), {'help_text': 'Optional profile image', 'required': False}), 5: ('wagtail.blocks.StructBlock', [[('name', 0), ('role', 1), ('initials', 2), ('quote', 3), ('image', 4)]], {})})),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]