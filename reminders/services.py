from datetime import timedelta

from django.utils import timezone

from feeding.models import FeedingSchedule
from health.models import HealthRecord
from reminders.models import Reminder


def generate_reminders_for_user(user):
    created = 0
    for schedule in FeedingSchedule.objects.filter(animal__owner=user, is_active=True):
        due = schedule.next_feed_date.date()
        if due <= timezone.localdate():
            _, was_created = Reminder.objects.get_or_create(
                user=user,
                animal=schedule.animal,
                reminder_type='FEEDING',
                due_date=due,
                defaults={'title': f'Кормить {schedule.animal.name}', 'source_id': schedule.pk},
            )
            if was_created:
                created += 1

    for record in HealthRecord.objects.filter(
        animal__owner=user, next_visit_date__isnull=False,
        next_visit_date__lte=timezone.localdate() + timedelta(days=7),
    ):
        _, was_created = Reminder.objects.get_or_create(
            user=user,
            animal=record.animal,
            reminder_type='VET',
            due_date=record.next_visit_date,
            defaults={'title': f'Визит: {record.animal.name} — {record.reason}', 'source_id': record.pk},
        )
        if was_created:
            created += 1
    return created
