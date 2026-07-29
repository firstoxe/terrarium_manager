import pytest
from django.urls import reverse

from accounts.factories import UserFactory
from animals.factories import AnimalFactory, TaxonomyFactory, MorphFactory, ActionFactory
from animals.forms import AnimalForm
from animals.models import Animal, Collection
from animals.services.costs import action_costs_by_period, total_costs_for_user
from animals.services.timeline import build_timeline
from animals.services.ownership import animals_for_user, animal_for_user
from test_utils.factories import CareRequirementFactory, WeightLogFactory, HealthRecordFactory


@pytest.mark.django_db
def test_animal_list_only_shows_own_animals(auth_client, user):
    AnimalFactory(owner=user, name='Mine')
    AnimalFactory(owner=UserFactory(), name='Other')
    response = auth_client.get(reverse('animals:animal_list'))
    assert response.status_code == 200
    content = response.content.decode()
    assert 'Mine' in content
    assert 'Other' not in content


@pytest.mark.django_db
def test_animal_list_filter_by_name(auth_client, user):
    AnimalFactory(owner=user, name='Alpha')
    AnimalFactory(owner=user, name='Beta')
    response = auth_client.get(reverse('animals:animal_list'), {'name': 'Alpha'})
    content = response.content.decode()
    assert 'Alpha' in content
    assert 'Beta' not in content


@pytest.mark.django_db
def test_cannot_view_other_users_animal(auth_client):
    animal = AnimalFactory(owner=UserFactory())
    response = auth_client.get(reverse('animals:animal_detail', args=[animal.pk]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_animal_detail_shows_care_requirement(auth_client, user):
    taxonomy = TaxonomyFactory()
    CareRequirementFactory(taxonomy=taxonomy, diet='Crickets daily')
    animal = AnimalFactory(owner=user, taxonomy=taxonomy)
    response = auth_client.get(reverse('animals:animal_detail', args=[animal.pk]))
    assert response.status_code == 200
    assert 'Crickets daily' in response.content.decode()


@pytest.mark.django_db
def test_animal_detail_shows_timeline(auth_client, user):
    animal = AnimalFactory(owner=user)
    ActionFactory(animal=animal, description='Fed well')
    response = auth_client.get(reverse('animals:animal_detail', args=[animal.pk]))
    assert 'Fed well' in response.content.decode()


@pytest.mark.django_db
def test_create_animal(auth_client, user):
    taxonomy = TaxonomyFactory()
    response = auth_client.post(reverse('animals:animal_create'), {
        'name': 'Gex',
        'taxonomy': taxonomy.pk,
        'birth_date': '2020-05-01',
        'acquisition_date': '2021-01-01',
        'sex': 'M',
        'habitat': 'DESERT',
        'care_level': 'BEGINNER',
    })
    assert response.status_code == 302
    assert Animal.objects.filter(owner=user, name='Gex').exists()


@pytest.mark.django_db
def test_update_animal(auth_client, user):
    animal = AnimalFactory(owner=user, name='OldName')
    response = auth_client.post(reverse('animals:animal_update', args=[animal.pk]), {
        'name': 'NewName',
        'taxonomy': animal.taxonomy.pk,
        'birth_date': animal.birth_date.isoformat(),
        'acquisition_date': animal.acquisition_date.isoformat(),
        'sex': animal.sex,
        'habitat': animal.habitat,
        'care_level': animal.care_level,
    })
    assert response.status_code == 302
    animal.refresh_from_db()
    assert animal.name == 'NewName'


@pytest.mark.django_db
def test_delete_animal(auth_client, user):
    animal = AnimalFactory(owner=user)
    response = auth_client.post(reverse('animals:animal_delete', args=[animal.pk]))
    assert response.status_code == 302
    assert not Animal.objects.filter(pk=animal.pk).exists()


@pytest.mark.django_db
def test_morph_must_match_taxonomy():
    taxonomy = TaxonomyFactory()
    morph = MorphFactory(taxonomy=TaxonomyFactory())
    form = AnimalForm(data={
        'name': 'Test',
        'taxonomy': taxonomy.pk,
        'morph': morph.pk,
        'birth_date': '2020-01-01',
        'acquisition_date': '2021-01-01',
        'sex': 'M',
        'habitat': 'DESERT',
        'care_level': 'BEGINNER',
    })
    assert not form.is_valid()


@pytest.mark.django_db
def test_action_costs_by_period():
    animal = AnimalFactory()
    ActionFactory(animal=animal, cost=50)
    ActionFactory(animal=animal, cost=30)
    costs = action_costs_by_period(animal.action_set.all())
    assert costs['week'] == 80


@pytest.mark.django_db
def test_total_costs_for_user(user):
    animal = AnimalFactory(owner=user)
    ActionFactory(animal=animal, cost=100)
    assert total_costs_for_user(user) == 100


@pytest.mark.django_db
def test_create_action(auth_client, user):
    animal = AnimalFactory(owner=user)
    response = auth_client.post(reverse('animals:action_create', args=[animal.pk]), {
        'action_type': 'FEEDING',
        'description': 'Fed crickets',
        'cost': '25.50',
    })
    assert response.status_code == 302
    assert animal.action_set.count() == 1


@pytest.mark.django_db
def test_ownership_helpers(user):
    mine = AnimalFactory(owner=user)
    AnimalFactory(owner=UserFactory())
    assert animals_for_user(user).count() == 1
    assert animal_for_user(user, mine.pk) == mine


@pytest.mark.django_db
def test_timeline_merges_events(user):
    animal = AnimalFactory(owner=user)
    ActionFactory(animal=animal, description='Action event')
    WeightLogFactory(animal=animal, weight_g=42)
    HealthRecordFactory(animal=animal, reason='Vet visit')
    timeline = build_timeline(animal)
    assert len(timeline) == 3
    types = {e['type'] for e in timeline}
    assert types == {'action', 'weight', 'health'}


@pytest.mark.django_db
def test_collection_list(auth_client, user):
    Collection.objects.create(owner=user, name='Home Terrarium')
    response = auth_client.get(reverse('animals:collection_list'))
    assert response.status_code == 200
    assert 'Home Terrarium' in response.content.decode()
