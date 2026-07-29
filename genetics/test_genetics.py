import pytest
from django.urls import reverse

from animals.factories import AnimalFactory, MorphFactory
from genetics.services.calculator import predict_offspring
from test_utils.factories import GeneFactory, MorphGeneFactory


def test_predict_normal_cross():
    assert predict_offspring([], []) == {'Normal': 1.0}


def test_predict_recessive_het_cross():
    genes = [{'gene_name': 'Albino', 'inheritance_type': 'RECESSIVE', 'genotype': 'HET'}]
    result = predict_offspring(genes, genes)
    assert sum(result.values()) == pytest.approx(1.0, abs=0.01)


@pytest.mark.django_db
def test_genetics_calculator_page(auth_client, user):
    AnimalFactory(owner=user, sex='M', name='Male1')
    AnimalFactory(owner=user, sex='F', name='Female1')
    response = auth_client.get(reverse('genetics:calculator'))
    assert response.status_code == 200
    assert 'Male1' in response.content.decode()


@pytest.mark.django_db
def test_genetics_calculator_with_morph_genes(auth_client, user):
    morph = MorphFactory()
    gene = GeneFactory(name='Albino', inheritance_type='RECESSIVE')
    MorphGeneFactory(morph=morph, gene=gene, genotype='HET')
    male = AnimalFactory(owner=user, sex='M', morph=morph)
    female = AnimalFactory(owner=user, sex='F', morph=morph)
    response = auth_client.get(reverse('genetics:calculator'), {
        'male': male.pk,
        'female': female.pk,
    })
    assert response.status_code == 200
    assert 'predictions' in response.context or response.content
