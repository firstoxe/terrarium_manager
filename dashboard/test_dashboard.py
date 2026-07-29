import pytest
from django.urls import reverse

from accounts.factories import UserFactory
from animals.factories import AnimalFactory, ActionFactory
from test_utils.factories import FeedingScheduleFactory, HealthRecordFactory


@pytest.mark.django_db
def test_dashboard_requires_login(client):
    assert client.get(reverse('dashboard:dashboard')).status_code == 302


@pytest.mark.django_db
def test_dashboard_shows_stats(auth_client, user):
    AnimalFactory(owner=user)
    ActionFactory(animal=AnimalFactory(owner=user), cost=50)
    FeedingScheduleFactory(animal=AnimalFactory(owner=user))
    response = auth_client.get(reverse('dashboard:dashboard'))
    assert response.status_code == 200
    content = response.content.decode()
    assert 'Животных' in content


@pytest.mark.django_db
def test_dashboard_shows_upcoming_vet(auth_client, user):
    from datetime import timedelta
    from django.utils import timezone
    animal = AnimalFactory(owner=user)
    HealthRecordFactory(
        animal=animal,
        reason='Annual check',
        next_visit_date=timezone.localdate() + timedelta(days=3),
    )
    response = auth_client.get(reverse('dashboard:dashboard'))
    assert 'Annual check' in response.content.decode()
