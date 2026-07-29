import pytest
from django.urls import reverse

from test_utils.factories import IncubationRecordFactory


@pytest.mark.django_db
def test_incubation_list(auth_client, user):
    inc = IncubationRecordFactory(
        clutch__pair__male__owner=user,
        clutch__pair__female__owner=user,
    )
    response = auth_client.get(reverse('incubation:list'))
    assert response.status_code == 200
    assert inc.clutch.pair.male.name in response.content.decode()


@pytest.mark.django_db
def test_incubation_detail(auth_client, user):
    inc = IncubationRecordFactory(
        clutch__pair__male__owner=user,
        clutch__pair__female__owner=user,
    )
    response = auth_client.get(reverse('incubation:detail', args=[inc.pk]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_incubation_days_remaining(user):
    from datetime import timedelta
    from django.utils import timezone
    inc = IncubationRecordFactory(
        clutch__pair__male__owner=user,
        clutch__pair__female__owner=user,
        expected_hatch=timezone.localdate() + timedelta(days=10),
    )
    assert inc.days_remaining == 10


@pytest.mark.django_db
def test_cannot_view_other_users_incubation(auth_client):
    inc = IncubationRecordFactory()
    response = auth_client.get(reverse('incubation:detail', args=[inc.pk]))
    assert response.status_code == 404
