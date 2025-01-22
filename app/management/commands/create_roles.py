from django.core.management.base import BaseCommand
from app.models import Role


class Command(BaseCommand):
    help = 'Create roles'

    def handle(self, *args, **kwargs):
        roles = [
            {'name': 'Admin', 'description': 'Has full access to manage content and users.'},
            {'name': 'Author', 'description': 'Can create and manage their own content.'},
        ]

        for role_data in roles:
            role, created = Role.objects.get_or_create(**role_data)
            if created:
                self.stdout.write(f"Role '{role.name}' created.")
            else:
                self.stdout.write(f"Role '{role.name}' already exists.")
