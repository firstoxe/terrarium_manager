import factory
from datetime import timedelta
from django.utils import timezone
from accounts.factories import UserFactory
from animals.factories import AnimalFactory, TaxonomyFactory, MorphFactory
from animals.models import CareRequirement, Collection
from feeding.models import FeedingSchedule
from health.models import WeightLog, HealthRecord, SheddingLog
from incubation.models import BreedingPair, Clutch, IncubationRecord
from genetics.models import Gene, MorphGene


class CareRequirementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CareRequirement

    taxonomy = factory.SubFactory(TaxonomyFactory)
    temperature_min = 24
    temperature_max = 32
    humidity_min = 30
    humidity_max = 50
    diet = 'Insects'


class CollectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Collection

    owner = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f'Collection{n}')


class FeedingScheduleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FeedingSchedule

    animal = factory.SubFactory(AnimalFactory)
    interval_days = 7
    food_type = 'Cricket'
    amount = 5


class WeightLogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WeightLog

    animal = factory.SubFactory(AnimalFactory)
    weight_g = 50.0


class HealthRecordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HealthRecord

    animal = factory.SubFactory(AnimalFactory)
    reason = 'Checkup'
    created_by = factory.LazyAttribute(lambda o: o.animal.owner)


class SheddingLogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SheddingLog

    animal = factory.SubFactory(AnimalFactory)


class GeneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Gene

    name = factory.Sequence(lambda n: f'Gene{n}')
    inheritance_type = 'RECESSIVE'


class MorphGeneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MorphGene

    morph = factory.SubFactory(MorphFactory)
    gene = factory.SubFactory(GeneFactory)
    genotype = 'HET'


class BreedingPairFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BreedingPair

    male = factory.SubFactory(AnimalFactory, sex='M')
    female = factory.SubFactory(AnimalFactory, sex='F', owner=factory.SelfAttribute('..male.owner'))


class ClutchFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Clutch

    pair = factory.SubFactory(BreedingPairFactory)
    lay_date = factory.LazyFunction(timezone.localdate)
    egg_count = 6


class IncubationRecordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IncubationRecord

    clutch = factory.SubFactory(ClutchFactory)
    start_date = factory.LazyFunction(timezone.localdate)
    expected_hatch = factory.LazyFunction(lambda: timezone.localdate() + timedelta(days=60))
