from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import TemplateView

from animals.models import Action
from animals.services.costs import total_costs_for_user
from animals.services.ownership import animals_for_user
from feeding.models import FeedingLog
from feeding.services.feeding import due_schedules_for_user, overdue_schedules_for_user
from health.models import HealthRecord
from reminders.models import Reminder


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if (
            request.user.is_authenticated
            and not request.user.onboarding_completed
            and not animals_for_user(request.user).exists()
        ):
            return redirect('accounts:onboarding')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        month_ago = timezone.now() - timedelta(days=30)
        pending = Reminder.objects.filter(
            user=user, status='PENDING',
        ).select_related('animal').order_by('due_date')[:8]

        context.update({
            'total_animals': animals_for_user(user).count(),
            'last_feeding': FeedingLog.objects.filter(animal__owner=user).select_related('animal').first(),
            'animals_due_today': due_schedules_for_user(user),
            'overdue_feedings': overdue_schedules_for_user(user),
            'recent_actions': Action.objects.filter(
                animal__owner=user,
            ).select_related('animal').order_by('-date')[:5],
            'monthly_costs': total_costs_for_user(user, since=month_ago),
            'upcoming_vet': HealthRecord.objects.filter(
                animal__owner=user,
                next_visit_date__isnull=False,
                next_visit_date__gte=timezone.now().date(),
            ).select_related('animal').order_by('next_visit_date')[:5],
            'pending_reminders': pending,
            'pending_reminders_count': Reminder.objects.filter(user=user, status='PENDING').count(),
            'show_onboarding_cta': (
                not user.onboarding_completed and animals_for_user(user).exists()
            ),
        })
        return context
