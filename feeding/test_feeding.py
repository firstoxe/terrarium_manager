import pytest
from django.urls import reverse

from accounts.factories import UserFactory
from animals.factories import AnimalFactory, ActionFactory
from feeding.models import FeedingSchedule
from feeding.services.feeding import log_feeding, due_schedules_for_user, overdue_schedules_for_user
from test_utils.factories import FeedingScheduleFactory


@pytest.mark.django_db
def test_log_feeding_creates_action(user):
    animal = AnimalFactory(owner=user)
    FeedingScheduleFactory(animal=animal, food_type='Cricket', interval_days=7)
    log = log_feeding(animal, user)
    assert log.action is not None
    assert log.action.action_type == 'FEEDING'
    animal.feeding_schedule.refresh_from_db()
    assert animal.feeding_schedule.last_fed is not None


@pytest.mark.django_db
def test_feeding_schedule_list(auth_client, user):
    animal = AnimalFactory(owner=user)
    FeedingScheduleFactory(animal=animal, food_type='Cricket', interval_days=3)
    response = auth_client.get(reverse('feeding:schedule_list'))
    assert response.status_code == 200
    assert animal.name in response.content.decode()


@pytest.mark.django_db
def test_feeding_history(auth_client, user):
    animal = AnimalFactory(owner=user)
    log_feeding(animal, user, food_type='Mealworm')
    response = auth_client.get(reverse('feeding:history'))
    assert response.status_code == 200
    assert 'Mealworm' in response.content.decode()


@pytest.mark.django_db
def test_feed_today(auth_client, user):
    animal = AnimalFactory(owner=user)
    FeedingScheduleFactory(animal=animal)
    response = auth_client.post(reverse('feeding:feed_today', args=[animal.pk]))
    assert response.status_code == 302
    assert animal.feeding_logs.count() == 1


@pytest.mark.django_db
def test_create_feeding_schedule(auth_client, user):
    animal = AnimalFactory(owner=user)
    response = auth_client.post(reverse('feeding:schedule_create', args=[animal.pk]), {
        'interval_days': 5,
        'food_type': 'Roach',
        'amount': 3,
        'is_active': True,
    })
    assert response.status_code == 302
    assert FeedingSchedule.objects.filter(animal=animal).exists()


@pytest.mark.django_db
def test_due_schedules_without_last_fed(user):
    animal = AnimalFactory(owner=user)
    FeedingScheduleFactory(animal=animal, food_type='Cricket', interval_days=7)
    due = due_schedules_for_user(user)
    assert len(due) == 1


@pytest.mark.django_db
def test_overdue_after_interval(user):
    from django.utils import timezone
    from datetime import timedelta
    animal = AnimalFactory(owner=user)
    schedule = FeedingScheduleFactory(animal=animal, interval_days=1)
    schedule.last_fed = timezone.now() - timedelta(days=3)
    schedule.save()
    overdue = overdue_schedules_for_user(user)
    assert len(overdue) == 1
