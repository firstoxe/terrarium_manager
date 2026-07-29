from django.utils import timezone

from animals.models import Action
from feeding.models import FeedingLog, FeedingSchedule


def log_feeding(animal, user, food_type=None, amount=None, notes=''):
    schedule = getattr(animal, 'feeding_schedule', None)
    food_type = food_type or (schedule.food_type if schedule else 'Корм')
    amount = amount or (schedule.amount if schedule else 1)

    action = Action.objects.create(
        animal=animal,
        action_type='FEEDING',
        description=notes or f'Кормление: {food_type}, {amount} шт.',
        cost=0,
        created_by=user,
    )
    log = FeedingLog.objects.create(
        animal=animal,
        food_type=food_type,
        amount=amount,
        notes=notes,
        created_by=user,
        action=action,
    )
    if schedule:
        schedule.last_fed = timezone.now()
        schedule.save(update_fields=['last_fed'])
    return log


def due_schedules_for_user(user):
    schedules = FeedingSchedule.objects.filter(
        animal__owner=user, is_active=True,
    ).select_related('animal', 'animal__taxonomy')
    return [s for s in schedules if s.is_due_today]


def overdue_schedules_for_user(user):
    schedules = FeedingSchedule.objects.filter(
        animal__owner=user, is_active=True,
    ).select_related('animal')
    return [s for s in schedules if s.is_overdue]
