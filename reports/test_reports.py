import pytest
from django.urls import reverse

from animals.factories import AnimalFactory, ActionFactory


@pytest.mark.django_db
def test_reports_page(auth_client, user):
    animal = AnimalFactory(owner=user)
    ActionFactory(animal=animal, cost=150)
    response = auth_client.get(reverse('reports:index'))
    assert response.status_code == 200
    assert '150' in response.content.decode()


@pytest.mark.django_db
def test_export_csv(auth_client, user):
    animal = AnimalFactory(owner=user, name='CSVAnimal')
    ActionFactory(animal=animal, description='Export me')
    response = auth_client.get(reverse('reports:export'))
    assert response.status_code == 200
    assert response['Content-Type'] == 'text/csv'
    content = response.content.decode()
    assert 'CSVAnimal' in content
    assert 'Export me' in content


@pytest.mark.django_db
def test_reports_requires_login(client):
    assert client.get(reverse('reports:index')).status_code == 302
