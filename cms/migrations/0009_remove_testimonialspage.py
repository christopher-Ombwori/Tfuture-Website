# Generated manually

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0008_rename_homepage_to_testimonialspage'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TestimonialsPage',
        ),
    ]