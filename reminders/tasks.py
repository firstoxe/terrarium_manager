from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Q

from reminders.models import Reminder
from reminders.services import generate_reminders_for_user

User = get_user_model()


def _send_telegram(chat_id: str, text: str) -> None:
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '') or ''
    if not token or not chat_id:
        return
    try:
        import json
        from urllib import request as urlrequest

        payload = json.dumps({'chat_id': chat_id, 'text': text}).encode('utf-8')
        req = urlrequest.Request(
            f'https://api.telegram.org/bot{token}/sendMessage',
            data=payload,
            headers={'Content-Type': 'application/json'},
            method='POST',
        )
        urlrequest.urlopen(req, timeout=10)
    except Exception:
        return


@shared_task
def generate_all_reminders():
    total = 0
    for user in User.objects.filter(is_active=True).iterator():
        total += generate_reminders_for_user(user)
    return total


@shared_task
def send_reminder_emails():
    sent = 0
    users = User.objects.filter(is_active=True).filter(
        Q(email__gt='') | Q(telegram_chat_id__gt='')
    )
    for user in users.iterator():
        reminders = Reminder.objects.filter(user=user, status='PENDING').order_by('due_date')
        if not reminders.exists():
            continue
        lines = [f'- {r.title} ({r.due_date})' for r in reminders[:15]]
        body = 'Активные напоминания:\n' + '\n'.join(lines)
        if user.email:
            send_mail(
                subject='Terrarium Manager: напоминания',
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )
        if getattr(user, 'telegram_chat_id', ''):
            _send_telegram(user.telegram_chat_id, body)
        sent += 1
    return sent
