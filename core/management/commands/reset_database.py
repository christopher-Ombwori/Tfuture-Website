from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Completely reset the database by dropping all tables and recreating them'

    def add_arguments(self, parser):
        parser.add_argument(
            '--noinput',
            action='store_true',
            help='Skip confirmation prompt',
        )

    def handle(self, *args, **options):
        if not options['noinput']:
            confirm = input("""
⚠️  WARNING: This will DELETE ALL DATA in your database!
This action cannot be undone.

Are you sure you want to continue? (yes/no): """)
            if confirm.lower() != 'yes':
                self.stdout.write(self.style.WARNING('Database reset cancelled.'))
                return

        self.stdout.write('🔄 Resetting database...')
        
        with connection.cursor() as cursor:
            # Drop all tables
            cursor.execute("""
                DO $$ DECLARE
                    r RECORD;
                BEGIN
                    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
                        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                    END LOOP;
                END $$;
            """)
            
            # Reset sequences
            cursor.execute("""
                DO $$ DECLARE
                    r RECORD;
                BEGIN
                    FOR r IN (SELECT sequence_name FROM information_schema.sequences WHERE sequence_schema = current_schema()) LOOP
                        EXECUTE 'DROP SEQUENCE IF EXISTS ' || quote_ident(r.sequence_name) || ' CASCADE';
                    END LOOP;
                END $$;
            """)

        self.stdout.write('✅ All tables dropped successfully!')
        
        # Create fresh migrations
        self.stdout.write('📝 Creating fresh migrations...')
        call_command('makemigrations', 'core')
        
        # Apply migrations
        self.stdout.write('🚀 Applying migrations...')
        call_command('migrate')
        
        # Create superuser
        self.stdout.write('👤 Creating superuser...')
        call_command('createsuperuser', interactive=False, username='admin', email='admin@example.com')
        
        # Populate services
        self.stdout.write('🔧 Populating services...')
        call_command('populate_services')
        
        self.stdout.write(self.style.SUCCESS('✅ Database completely reset and ready!'))
        self.stdout.write('📧 Admin credentials: admin / admin (change this immediately!)') 