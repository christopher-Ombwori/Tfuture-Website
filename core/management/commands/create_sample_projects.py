from django.core.management.base import BaseCommand
from core.models import Project, ProjectImage
from django.core.files import File
from pathlib import Path
import os

class Command(BaseCommand):
    help = 'Creates sample projects for the portfolio'

    def handle(self, *args, **kwargs):
        # Create projects
        projects_data = [
            {
                'title': 'Complete Brand Transformation',
                'client': 'TechStart Inc.',
                'slug': 'complete-brand-transformation',
                'industry': 'Technology',
                'category': 'brand-identity',
                'subcategory': 'full-brand',
                'description': 'End-to-end brand identity development for a tech startup, including logo design, visual identity, and brand guidelines.'
            },
            {
                'title': 'Visual System Design',
                'client': 'FinTech Solutions',
                'slug': 'visual-system-design',
                'industry': 'Finance',
                'category': 'brand-identity',
                'subcategory': 'visual-identity',
                'description': 'Comprehensive visual identity system for a fintech company, including color palette, typography, and design elements.'
            },
            {
                'title': 'Logo Collection',
                'client': 'Various Clients',
                'slug': 'logo-collection',
                'industry': 'Multiple',
                'category': 'brand-identity',
                'subcategory': 'logofolio',
                'description': 'A diverse collection of logo designs created for various industries and clients.'
            },
            {
                'title': 'Corporate Profile',
                'client': 'Global Enterprises',
                'slug': 'corporate-profile',
                'industry': 'Corporate',
                'category': 'communication-kits',
                'subcategory': 'company-profiles',
                'description': 'Professional company profile design including corporate identity elements and brand guidelines.'
            },
            {
                'title': 'Presentation Design',
                'client': 'Innovate Corp',
                'slug': 'presentation-design',
                'industry': 'Technology',
                'category': 'communication-kits',
                'subcategory': 'presentations',
                'description': 'Custom presentation templates and decks designed for corporate presentations and investor pitches.'
            },
            {
                'title': 'Internal Communications',
                'client': 'Enterprise Solutions',
                'slug': 'internal-communications',
                'industry': 'Corporate',
                'category': 'communication-kits',
                'subcategory': 'internal-coms',
                'description': 'Internal communication materials and SOPs for a large enterprise company.'
            },
            {
                'title': 'Stationery Design',
                'client': 'Creative Agency',
                'slug': 'stationery-design',
                'industry': 'Creative',
                'category': 'communication-kits',
                'subcategory': 'stationery',
                'description': 'Complete stationery package design including business cards, letterheads, and envelopes.'
            },
            {
                'title': 'Social Media Kit',
                'client': 'Digital Brand',
                'slug': 'social-media-kit',
                'industry': 'Digital',
                'category': 'communication-kits',
                'subcategory': 'social-media',
                'description': 'Comprehensive social media branding package including templates and guidelines.'
            }
        ]

        for project_data in projects_data:
            project, created = Project.objects.get_or_create(
                slug=project_data['slug'],
                defaults=project_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created project "{project.title}"'))
            else:
                self.stdout.write(self.style.WARNING(f'Project "{project.title}" already exists')) 