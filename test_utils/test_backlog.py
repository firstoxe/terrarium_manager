import pytest
from django.urls import reverse

from animals.factories import AnimalFactory, TaxonomyFactory
from animals.models import Collection
from health.models import WeightLog
from reminders.models import Reminder
from reminders.services import generate_reminders_for_user
from feeding.models import FeedingSchedule


@pytest.mark.django_db
def test_onboarding_redirect(auth_client, user):
    user.onboarding_completed = False
    user.save()
    response = auth_client.get(reverse('dashboard:dashboard'))
    assert response.status_code == 302
    assert response.url == reverse('accounts:onboarding')


@pytest.mark.django_db
def test_onboarding_finish(auth_client, user):
    response = auth_client.post(reverse('accounts:onboarding'), {'action': 'finish'})
    assert response.status_code == 302
    user.refresh_from_db()
    assert user.onboarding_completed is True


@pytest.mark.django_db
def test_schedule_create_prefills_from_care(auth_client, user):
    from animals.models import CareRequirement
    taxonomy = TaxonomyFactory()
    CareRequirement.objects.create(
        taxonomy=taxonomy,
        temperature_min=24, temperature_max=30,
        humidity_min=40, humidity_max=60,
        diet='insects',
        catalog_details={'feeding_policy': {'default': {
            'interval_days': 3, 'food_type': 'сверчки', 'amount': 5,
        }}},
    )
    animal = AnimalFactory(owner=user, taxonomy=taxonomy)
    response = auth_client.get(reverse('feeding:schedule_create', args=[animal.pk]))
    assert response.status_code == 200
    assert response.context['form'].initial.get('food_type') == 'сверчки'
    assert response.context['form'].initial.get('interval_days') == 3


@pytest.mark.django_db
def test_weight_create(auth_client, user):
    animal = AnimalFactory(owner=user)
    response = auth_client.post(
        reverse('health:weight_create', args=[animal.pk]),
        {'date': '2026-07-29', 'weight_g': '42.5', 'notes': ''},
    )
    assert response.status_code == 302
    assert WeightLog.objects.filter(animal=animal, weight_g=42.5).exists()


@pytest.mark.django_db
def test_collection_share_public(auth_client, user, client):
    collection = Collection.objects.create(owner=user, name='Публичная')
    collection.ensure_share_token()
    collection.is_public = True
    collection.save()
    animal = AnimalFactory(owner=user, collection=collection)
    url = reverse('animals:collection_share', args=[collection.share_token])
    response = client.get(url)
    assert response.status_code == 200
    assert animal.name.encode() in response.content


@pytest.mark.django_db
def test_collection_export(auth_client, user):
    AnimalFactory(owner=user, name='ExportAnimal')
    response = auth_client.get(reverse('animals:collection_export'))
    assert response.status_code == 200
    assert b'ExportAnimal' in response.content


@pytest.mark.django_db
def test_reminder_generate(auth_client, user):
    animal = AnimalFactory(owner=user)
    FeedingSchedule.objects.create(
        animal=animal, interval_days=1, food_type='mice', amount=1, is_active=True,
    )
    created = generate_reminders_for_user(user)
    assert created >= 1
    response = auth_client.post(reverse('reminders:generate'))
    assert response.status_code == 302
    assert Reminder.objects.filter(user=user, status='PENDING').exists()


@pytest.mark.django_db
def test_telegram_webhook(client, user):
    response = client.post(
        reverse('accounts:telegram_webhook'),
        data='{"message":{"chat":{"id":12345},"text":"/start %s"}}' % user.username,
        content_type='application/json',
    )
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.telegram_chat_id == '12345'
