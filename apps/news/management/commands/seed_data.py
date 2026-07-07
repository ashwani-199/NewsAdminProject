from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from apps.accounts.models import User
from apps.news.models import Category, Tag, Article
from apps.core.models import WebsiteSettings


class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@newsportal.com',
                password='admin123',
                role='administrator',
                is_email_verified=True,
            )
            self.stdout.write('  Superuser created: admin / admin123')

        categories = [
            ('Politics', 'fas fa-landmark'),
            ('Technology', 'fas fa-microchip'),
            ('Business', 'fas fa-briefcase'),
            ('Sports', 'fas fa-football-ball'),
            ('Entertainment', 'fas fa-film'),
            ('Health', 'fas fa-heartbeat'),
            ('Science', 'fas fa-flask'),
            ('Education', 'fas fa-graduation-cap'),
            ('Lifestyle', 'fas fa-leaf'),
            ('World', 'fas fa-globe'),
        ]

        for name, icon in categories:
            Category.objects.get_or_create(
                name=name,
                defaults={'slug': slugify(name), 'icon': icon}
            )
        self.stdout.write(f'  Created {len(categories)} categories')

        tags = ['Breaking', 'Exclusive', 'Opinion', 'Analysis', 'Interview', 'Update']
        for tag_name in tags:
            Tag.objects.get_or_create(name=tag_name)
        self.stdout.write(f'  Created {len(tags)} tags')

        journalist, _ = User.objects.get_or_create(
            username='journalist',
            defaults={
                'email': 'journalist@newsportal.com',
                'role': 'journalist',
                'is_email_verified': True,
            }
        )
        journalist.set_password('journalist123')
        journalist.save()
        self.stdout.write('  Journalist created: journalist / journalist123')

        if not WebsiteSettings.objects.exists():
            WebsiteSettings.objects.create(
                site_name='NewsPortal',
                site_tagline='Your Trusted News Source',
                copyright_text=f'© {timezone.now().year} NewsPortal. All rights reserved.',
            )
            self.stdout.write('  Website settings created')

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
