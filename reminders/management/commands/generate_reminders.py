from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from reminders.services import generate_reminders_for_user

User = get_user_model()


class Command(BaseCommand):
    help = 'Generate reminders from feeding schedules and vet visits'

    def handle(self, *args, **options):
        total = 0
        for user in User.objects.filter(is_active=True):
            total += generate_reminders_for_user(user)
        self.stdout.write(self.style.SUCCESS(f'Created {total} reminders'))
