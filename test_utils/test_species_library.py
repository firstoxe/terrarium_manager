import pytest
from django.core.management import call_command
from django.urls import reverse

from animals.models import Taxonomy, CareRequirement, Morph
from animals.services.species_library import (
    get_entry,
    import_entry,
    is_imported,
    list_entries,
    search_entries,
)


@pytest.mark.django_db
def test_seed_species_command():
    call_command('seed_species')
    assert Taxonomy.objects.filter(library_id='eublepharis-macularius').exists()
    assert CareRequirement.objects.count() >= len(list_entries(kind='popular'))


@pytest.mark.django_db
def test_seed_species_idempotent():
    call_command('seed_species')
    count = Taxonomy.objects.count()
    morph_count = Morph.objects.count()
    call_command('seed_species')
    assert Taxonomy.objects.count() == count
    assert Morph.objects.count() == morph_count


@pytest.mark.django_db
def test_import_single_entry():
    assert not is_imported('python-regius')
    taxonomy = import_entry('python-regius')
    assert taxonomy.library_id == 'python-regius'
    assert taxonomy.common_name == 'Королевский питон'
    assert CareRequirement.objects.filter(taxonomy=taxonomy).exists()
    assert Morph.objects.filter(taxonomy=taxonomy).count() >= 5
    assert is_imported('python-regius')


@pytest.mark.django_db
def test_import_entry_idempotent():
    import_entry('eublepharis-macularius')
    count = Morph.objects.filter(taxonomy__library_id='eublepharis-macularius').count()
    import_entry('eublepharis-macularius')
    assert Morph.objects.filter(taxonomy__library_id='eublepharis-macularius').count() == count


def test_search_entries():
    results = search_entries(query='эублефар')
    assert any(e['id'] == 'eublepharis-macularius' for e in results)


def test_search_entries_care_level_and_popular():
    beginners = search_entries(care_level='BEGINNER', kind='popular')
    assert beginners
    assert all(e.get('care_level', '').upper() == 'BEGINNER' for e in beginners)


@pytest.mark.django_db
def test_species_library_filters(auth_client):
    response = auth_client.get(
        reverse('animals:species_library'),
        {'scope': 'popular', 'care_level': 'BEGINNER'},
    )
    assert response.status_code == 200
    assert response.context['scope'] == 'popular'
    assert response.context['care_level'] == 'BEGINNER'
    assert all(e.get('care_level', '').upper() == 'BEGINNER' for e in response.context['entries'])


@pytest.mark.django_db
def test_species_library_import_and_create_redirect(auth_client):
    response = auth_client.post(
        reverse('animals:species_library_import', args=['pantherophis-guttatus']),
        {'create_animal': '1'},
    )
    assert response.status_code == 302
    taxonomy = Taxonomy.objects.get(library_id='pantherophis-guttatus')
    assert f'taxonomy={taxonomy.pk}' in response.url


@pytest.mark.django_db
def test_seed_species_import_full_catalog():
    call_command('seed_species', '--all')
    assert Taxonomy.objects.count() >= len(list_entries(kind='catalog'))


def test_get_entry_unknown():
    assert get_entry('nonexistent') is None


@pytest.mark.django_db
def test_species_library_view(auth_client):
    response = auth_client.get(reverse('animals:species_library'))
    assert response.status_code == 200
    assert b'\xd0\xad\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb5\xd1\x84\xd0\xb0\xd1\x80' in response.content or b'Eublepharis' in response.content


@pytest.mark.django_db
def test_species_library_import_view(auth_client):
    response = auth_client.post(reverse('animals:species_library_import', args=['unknown-species']))
    assert response.status_code == 302

    response = auth_client.post(reverse('animals:species_library_import', args=['pantherophis-guttatus']))
    assert response.status_code == 302
    assert Taxonomy.objects.filter(library_id='pantherophis-guttatus').exists()
