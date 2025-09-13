# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0011_alter_blogpage_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectpage',
            name='seo_brand_keywords',
            field=models.CharField(blank=True, help_text='Comma-separated keywords for TFuture Designs brand differentiation', max_length=255),
        ),
        migrations.AddField(
            model_name='projectpage',
            name='seo_kenya_focus',
            field=models.CharField(blank=True, help_text='Kenya-specific keywords or phrases for local SEO', max_length=255),
        ),
        migrations.AddField(
            model_name='projectpage',
            name='seo_africa_focus',
            field=models.CharField(blank=True, help_text='Africa-specific keywords or phrases for regional SEO', max_length=255),
        ),
        migrations.AddField(
            model_name='projectpage',
            name='seo_industry_differentiator',
            field=models.CharField(blank=True, help_text='Industry-specific terms that differentiate TFuture Designs', max_length=255),
        ),
    ]