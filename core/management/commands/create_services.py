from django.core.management.base import BaseCommand
from core.models import Service

class Command(BaseCommand):
    help = 'Create default services for TFuture'

    def handle(self, *args, **options):
        services_data = [
            {
                'name': 'Brand Strategies & Identity Systems',
                'description': 'We build your brand from the ground up — starting with your purpose, tone, and voice. Then we bring it to life through a full visual identity: logos, colors, fonts, and clear guidelines. Every element is crafted to work across all platforms — from pitch decks and social media to banners and branded merchandise. The result? A brand that looks right, feels right, and connects deeply.',
                'short_description': 'We build your brand from the ground up — creating a cohesive visual identity that works across all platforms.',
                'icon_svg': '''<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="w-12 h-12">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.53 16.122a3 3 0 00-5.78 1.128 2.25 2.25 0 01-2.4 2.245 4.5 4.5 0 008.4-2.245c0-.399-.078-.78-.22-1.128zm0 0a15.998 15.998 0 003.388-1.62m-5.043-.025a15.994 15.994 0 011.622-3.395m3.42 3.42a15.995 15.995 0 004.764-4.648l3.876-5.814a1.151 1.151 0 00-1.597-1.597L14.146 6.32a15.996 15.996 0 00-4.649 4.763m3.42 3.42a6.776 6.776 0 00-3.42-3.42" />
                </svg>''',
                'is_featured': True,
                'order': 1,
            },
            {
                'name': 'Company Profiles & Digital Kits',
                'short_description': 'We craft compelling company profiles, brand decks, pitch documents, and press kits designed to impress clients, investors, and media.',
                'icon_svg': '''<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="w-10 h-10">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
                </svg>''',
                'is_featured': False,
                'order': 2,
            },
            {
                'name': 'Social Media Visuals',
                'short_description': 'We design daily & campaign visuals — from post templates, carousels, story frames, cover photos, to email signatures and announcement posts.',
                'icon_svg': '''<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="w-10 h-10">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.129.166 2.27.293 3.423.379.35.026.67.21.865.501L12 21l2.755-4.133a1.14 1.14 0 01.865-.501 48.172 48.172 0 003.423-.379c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0012 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018z" />
                </svg>''',
                'is_featured': False,
                'order': 3,
            },
            {
                'name': 'Event Branding',
                'short_description': 'Visuals that shape real-world experiences: stage layouts, booth design, poster placement, on-screen content, event signage, and branded merchandise.',
                'icon_svg': '''<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="w-10 h-10">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3m0 0l.5 1.5m-.5-1.5h-9.5m0 0l-.5 1.5m.75-9l3-3 2.148 2.148A12.061 12.061 0 0116.5 7.605" />
                </svg>''',
                'is_featured': False,
                'order': 4,
            },
            {
                'name': 'Real-World Rollouts',
                'short_description': 'We handle the translation of your brand into the physical world — directional signs, branded t-shirts, banners, backdrops, lanyards, staff kits, props.',
                'icon_svg': '''<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="w-10 h-10">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15.75 5.25a3 3 0 013 3m3 0a6 6 0 01-7.029 5.912c-.563-.097-1.159.026-1.563.43L10.5 17.25H8.25v2.25H6v2.25H2.25v-2.818c0-.597.237-1.17.659-1.591l6.499-6.499c.404-.404.527-1 .43-1.563A6 6 0 1121.75 8.25z" />
                </svg>''',
                'is_featured': False,
                'order': 5,
            },
        ]

        created_count = 0
        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                name=service_data['name'],
                defaults=service_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created service: {service.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Service already exists: {service.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new services!')
        ) 