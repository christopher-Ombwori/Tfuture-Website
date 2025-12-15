# Generated manually

from django.db import migrations, models
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0017_remove_projectindexpage_hero_tiles'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('answer', wagtail.fields.RichTextField()),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'FAQ Item',
                'verbose_name_plural': 'FAQ Items',
                'ordering': ['order', 'question'],
            },
        ),
    ]
