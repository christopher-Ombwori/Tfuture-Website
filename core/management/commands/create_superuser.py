from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates or updates a superuser with predefined credentials'

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'christopherombwori06@gmail.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        if not created:
            user.email = 'christopherombwori06@gmail.com'
            user.is_staff = True
            user.is_superuser = True
        
        user.set_password('kali')
        user.save()
        
        if created:
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser updated successfully')) 