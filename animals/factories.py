import factory
from accounts.factories import UserFactory
from animals.models import Taxonomy, Morph, Animal, Action


class TaxonomyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Taxonomy

    class_name = 'Reptilia'
    order = 'Squamata'
    family = 'Gekkonidae'
    genus = 'Eublepharis'
    species = factory.Sequence(lambda n: f'species{n}')
    scientific_name = factory.LazyAttribute(lambda o: f'{o.genus} {o.species}')


class MorphFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Morph

    taxonomy = factory.SubFactory(TaxonomyFactory)
    name = factory.Sequence(lambda n: f'morph{n}')


class AnimalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Animal

    owner = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f'Animal{n}')
    taxonomy = factory.SubFactory(TaxonomyFactory)
    birth_date = factory.Faker('date_of_birth')
    sex = 'U'
    habitat = 'DESERT'
    care_level = 'BEGINNER'


class ActionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Action

    animal = factory.SubFactory(AnimalFactory)
    action_type = 'FEEDING'
    description = 'Test action'
    cost = 100
    created_by = factory.LazyAttribute(lambda o: o.animal.owner)
