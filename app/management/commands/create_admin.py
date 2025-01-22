from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from app.models import Role


class Command(BaseCommand):
    help = 'Create admin'

    def handle(self, *args, **kwargs):
        email = 'admin@example.com'
        password = 'Admin@123'

        admin_role, created = Role.objects.get_or_create(name='Admin')

        User = get_user_model()
        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                email=email,
                password=password,
                first_name='Admin',
                last_name='User',
            )
            self.stdout.write(self.style.SUCCESS('Admin user created successfully!'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists.'))
