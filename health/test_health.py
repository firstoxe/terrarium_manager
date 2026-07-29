import pytest
from datetime import timedelta

from django.utils import timezone

from animals.factories import AnimalFactory
from test_utils.factories import WeightLogFactory, HealthRecordFactory, SheddingLogFactory


@pytest.mark.django_db
def test_weight_log_str():
    log = WeightLogFactory(weight_g=55.5)
    assert '55.5' in str(log)


@pytest.mark.django_db
def test_health_record_with_next_visit():
    record = HealthRecordFactory(
        reason='Parasite check',
        next_visit_date=timezone.localdate() + timedelta(days=14),
    )
    assert record.next_visit_date is not None


@pytest.mark.django_db
def test_shedding_log_quality():
    log = SheddingLogFactory(quality='PARTIAL')
    assert log.get_quality_display() == 'Частичная'


@pytest.mark.django_db
def test_weight_in_timeline(user):
    from animals.services.timeline import build_timeline
    animal = AnimalFactory(owner=user)
    WeightLogFactory(animal=animal, weight_g=100)
    timeline = build_timeline(animal)
    assert any(e['type'] == 'weight' for e in timeline)
