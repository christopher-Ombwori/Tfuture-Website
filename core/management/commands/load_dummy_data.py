from django.core.management.base import BaseCommand
from core.models import Project, ProjectImage
from django.core.files import File
from pathlib import Path
import os

class Command(BaseCommand):
    help = 'Loads dummy data for portfolio projects'

    def handle(self, *args, **options):
        # Clear existing data
        Project.objects.all().delete()
        
        # Create projects
        projects_data = [
            {
                'title': 'TechVision Rebrand',
                'client': 'TechVision Inc.',
                'industry': 'Technology',
                'category': 'brand-identity',
                'subcategory': 'full-brand',
                'description': 'Complete brand transformation for a leading tech company, including logo design, brand guidelines, and visual identity system.',
            },
            {
                'title': 'EcoLife Communication Kit',
                'client': 'EcoLife Solutions',
                'industry': 'Environmental',
                'category': 'communication-kits',
                'subcategory': 'company-profiles',
                'description': 'Comprehensive communication kit including company profile, presentation templates, and social media assets.',
            },
            {
                'title': 'Global Tech Summit 2024',
                'client': 'TechGlobal',
                'industry': 'Technology',
                'category': 'events',
                'description': 'Complete event branding and experience design for the annual tech summit, including stage design, signage, and digital assets.',
            },
            {
                'title': 'Fashion Forward Launch',
                'client': 'StyleHub',
                'industry': 'Fashion',
                'category': 'rollouts',
                'description': 'Merchandise and rollout campaign for a new fashion brand launch, including store displays and promotional materials.',
            },
            {
                'title': 'HealthPlus Visual Identity',
                'client': 'HealthPlus Medical',
                'industry': 'Healthcare',
                'category': 'brand-identity',
                'subcategory': 'visual-identity',
                'description': 'Visual identity system for a healthcare provider, including color palette, typography, and application guidelines.',
            },
            {
                'title': 'InnovateX Social Media Kit',
                'client': 'InnovateX',
                'industry': 'Technology',
                'category': 'communication-kits',
                'subcategory': 'social-media',
                'description': 'Complete social media kit including templates, guidelines, and asset library for consistent brand presence.',
            },
        ]

        for project_data in projects_data:
            project = Project.objects.create(**project_data)
            self.stdout.write(self.style.SUCCESS(f'Created project: {project.title}'))

        self.stdout.write(self.style.SUCCESS('Successfully loaded dummy data')) 