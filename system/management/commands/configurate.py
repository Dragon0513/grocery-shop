from django.core.management.base import BaseCommand

from system.models import Role


class Command(BaseCommand):
    help = "Erstellt die vordefinierten Rollen"

    def handle(self, *args, **kwargs):
        roles = [
            {"name": "Admin", "priority": 5},
            {"name": "Moderator", "priority": 4},
            {"name": "Premium", "priority": 3},
            {"name": "Verifiziert", "priority": 2},
            {"name": "Standard", "priority": 1},
        ]

        for role_data in roles:
            role, created = Role.objects.get_or_create(
                name=role_data["name"], defaults={"priority": role_data["priority"]}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Role "{role.name}" created with level {role.priority}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Role "{role.name}" already exists')
                )
