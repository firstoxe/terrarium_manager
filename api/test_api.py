import pytest
from django.urls import reverse

from accounts.factories import UserFactory
from animals.factories import AnimalFactory, ActionFactory, TaxonomyFactory
from animals.models import Action
from feeding.services.feeding import log_feeding


@pytest.mark.django_db
def test_api_animals_list(auth_client, user):
    AnimalFactory(owner=user, name='ApiAnimal')
    AnimalFactory(owner=UserFactory())
    response = auth_client.get('/api/v1/animals/')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['name'] == 'ApiAnimal'


@pytest.mark.django_db
def test_api_create_animal(auth_client, user):
    taxonomy = TaxonomyFactory()
    response = auth_client.post('/api/v1/animals/', {
        'name': 'NewApi',
        'taxonomy': taxonomy.pk,
        'sex': 'M',
        'birth_date': '2020-01-01',
        'habitat': 'DESERT',
        'care_level': 'BEGINNER',
    }, content_type='application/json')
    assert response.status_code == 201
    assert response.json()['name'] == 'NewApi'


@pytest.mark.django_db
def test_api_actions(auth_client, user):
    animal = AnimalFactory(owner=user)
    ActionFactory(animal=animal)
    response = auth_client.get('/api/v1/actions/')
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.django_db
def test_api_feeding_logs(auth_client, user):
    animal = AnimalFactory(owner=user)
    log_feeding(animal, user)
    response = auth_client.get('/api/v1/feeding/')
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.django_db
def test_api_requires_auth(client):
    assert client.get('/api/v1/animals/').status_code in (401, 403)


@pytest.mark.django_db
def test_api_cannot_create_action_for_foreign_animal(auth_client, user):
    foreign = AnimalFactory(owner=UserFactory())
    response = auth_client.post('/api/v1/actions/', {
        'animal': foreign.pk,
        'action_type': 'FEEDING',
        'description': 'hack',
        'cost': '0.00',
    }, content_type='application/json')
    assert response.status_code == 400
    assert Action.objects.filter(animal=foreign, description='hack').count() == 0


@pytest.mark.django_db
def test_api_create_action_for_own_animal(auth_client, user):
    animal = AnimalFactory(owner=user)
    response = auth_client.post('/api/v1/actions/', {
        'animal': animal.pk,
        'action_type': 'OBSERVATION',
        'description': 'ok',
        'cost': '1.50',
    }, content_type='application/json')
    assert response.status_code == 201
    assert response.json()['description'] == 'ok'


@pytest.mark.django_db
def test_health_endpoint(client):
    response = client.get(reverse('health'))
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'
