from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

from reminders.models import Reminder

User = get_user_model()


@shared_task
def send_reminder_emails():
    for user in User.objects.filter(is_active=True, email__isnull=False).exclude(email=''):
        reminders = Reminder.objects.filter(user=user, status='PENDING')
        if not reminders.exists():
            continue
        lines = [f'- {r.title} ({r.due_date})' for r in reminders[:10]]
        send_mail(
            subject='Terrarium Manager: напоминания',
            message='Активные напоминания:\n' + '\n'.join(lines),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
