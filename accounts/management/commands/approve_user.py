from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from accounts.models import User


class Command(BaseCommand):
    help = 'Approve a user account (or all staff/superusers)'

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='?', help='Username to approve')
        parser.add_argument(
            '--all-staff',
            action='store_true',
            help='Approve all staff and superuser accounts',
        )

    def handle(self, *args, **options):
        if options['all_staff']:
            count = User.objects.filter(Q(is_staff=True) | Q(is_superuser=True)).update(
                is_approved=True,
                is_active=True,
            )
            self.stdout.write(self.style.SUCCESS(f'Approved {count} staff/superuser account(s)'))
            return

        username = options.get('username')
        if not username:
            raise CommandError('Specify a username or use --all-staff')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist as exc:
            raise CommandError(f'User "{username}" not found') from exc

        user.is_approved = True
        user.is_active = True
        user.save(update_fields=['is_approved', 'is_active'])
        self.stdout.write(self.style.SUCCESS(f'Approved user "{username}"'))
