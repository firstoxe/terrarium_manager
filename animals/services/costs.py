from datetime import timedelta

from django.db.models import Sum
from django.utils import timezone


def action_costs_by_period(actions_qs):
    now = timezone.now()
    periods = {
        'week': now - timedelta(days=7),
        'month': now - timedelta(days=30),
        'year': now - timedelta(days=365),
    }
    return {
        key: actions_qs.filter(date__gte=since).aggregate(total=Sum('cost'))['total'] or 0
        for key, since in periods.items()
    }


def total_costs_for_user(user, since=None):
    from ..models import Action

    qs = Action.objects.filter(animal__owner=user)
    if since:
        qs = qs.filter(date__gte=since)
    return qs.aggregate(total=Sum('cost'))['total'] or 0
