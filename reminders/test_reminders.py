import pytest
from datetime import timedelta

from django.core.management import call_command
from django.urls import reverse
from django.utils import timezone

from animals.factories import AnimalFactory
from reminders.models import Reminder
from reminders.services import generate_reminders_for_user
from test_utils.factories import FeedingScheduleFactory, HealthRecordFactory


@pytest.mark.django_db
def test_reminder_list(auth_client, user):
    Reminder.objects.create(
        user=user, animal=AnimalFactory(owner=user),
        reminder_type='FEEDING', title='Feed Gex',
        due_date=timezone.localdate(),
    )
    response = auth_client.get(reverse('reminders:list'))
    assert response.status_code == 200
    assert 'Feed Gex' in response.content.decode()


@pytest.mark.django_db
def test_reminder_done(auth_client, user):
    reminder = Reminder.objects.create(
        user=user, reminder_type='CUSTOM', title='Task',
        due_date=timezone.localdate(),
    )
    response = auth_client.post(reverse('reminders:done', args=[reminder.pk]))
    assert response.status_code == 302
    reminder.refresh_from_db()
    assert reminder.status == 'DONE'


@pytest.mark.django_db
def test_generate_reminders_from_feeding(user):
    animal = AnimalFactory(owner=user)
    FeedingScheduleFactory(animal=animal, interval_days=7)
    created = generate_reminders_for_user(user)
    assert created >= 1
    assert Reminder.objects.filter(user=user, reminder_type='FEEDING').exists()


@pytest.mark.django_db
def test_generate_reminders_from_vet(user):
    animal = AnimalFactory(owner=user)
    HealthRecordFactory(
        animal=animal,
        next_visit_date=timezone.localdate() + timedelta(days=2),
    )
    created = generate_reminders_for_user(user)
    assert created >= 1


@pytest.mark.django_db
def test_generate_reminders_command(user):
    animal = AnimalFactory(owner=user)
    FeedingScheduleFactory(animal=animal)
    call_command('generate_reminders')
    assert Reminder.objects.filter(user=user).exists()
