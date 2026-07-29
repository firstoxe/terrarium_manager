from datetime import datetime, date, time

from django.utils import timezone


def _sort_key(value):
    if isinstance(value, date) and not isinstance(value, datetime):
        dt = datetime.combine(value, time.min)
        return timezone.make_aware(dt)
    return value


def build_timeline(animal):
    events = []
    for action in animal.action_set.all():
        events.append({
            'date': action.date,
            'type': 'action',
            'label': action.get_action_type_display(),
            'description': action.description,
            'cost': action.cost,
        })
    for log in animal.feeding_logs.all():
        events.append({
            'date': log.date,
            'type': 'feeding',
            'label': 'Кормление',
            'description': f'{log.food_type}, {log.amount} шт.',
            'cost': None,
        })
    for w in animal.weight_logs.all():
        events.append({
            'date': w.date,
            'type': 'weight',
            'label': 'Вес',
            'description': f'{w.weight_g} г',
            'cost': None,
        })
    for h in animal.health_records.all():
        events.append({
            'date': h.date,
            'type': 'health',
            'label': h.reason,
            'description': h.diagnosis or h.treatment,
            'cost': h.cost,
        })
    for s in animal.shedding_logs.all():
        events.append({
            'date': s.date,
            'type': 'shedding',
            'label': 'Линька',
            'description': s.get_quality_display(),
            'cost': None,
        })
    events.sort(key=lambda e: _sort_key(e['date']), reverse=True)
    return events
