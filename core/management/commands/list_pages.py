# myapp/management/commands/list_pages.py
from django.core.management.base import BaseCommand
from wagtail.models import Page

class Command(BaseCommand):
    help = "List all Wagtail pages"

    def handle(self, *args, **options):
        for p in Page.objects.all().order_by('path'):
            self.stdout.write(f"{p.id} | {p.title} | {p.path}")
