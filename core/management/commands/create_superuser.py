from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates or updates a superuser with predefined credentials'

    def handle(self, *args, **options):
        # Delete existing admin user if it exists
        User.objects.filter(username='admin').delete()
        
        # Create new superuser
        user = User.objects.create_superuser(
            username='admin',
            email='christopherombwori06@gmail.com',
            password='kali'
        )
        
        # Print user details for debugging
        self.stdout.write(self.style.SUCCESS(f'User details:'))
        self.stdout.write(f'Username: {user.username}')
        self.stdout.write(f'Email: {user.email}')
        self.stdout.write(f'Is staff: {user.is_staff}')
        self.stdout.write(f'Is superuser: {user.is_superuser}')
        self.stdout.write(f'Is active: {user.is_active}')
        
        self.stdout.write(self.style.SUCCESS('Superuser created successfully')) 