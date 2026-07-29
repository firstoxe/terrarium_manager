from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from django_ratelimit.decorators import ratelimit

from animals.models import Animal, Taxonomy
from animals.services.ownership import animals_for_user
from animals.services.species_library import import_popular, list_entries
from feeding.models import FeedingSchedule


class OnboardingView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/onboarding.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.onboarding_completed and animals_for_user(request.user).exists():
            return redirect('dashboard:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        animals = animals_for_user(self.request.user)
        animal = animals.first()
        has_schedule = bool(animal and hasattr(animal, 'feeding_schedule') and animal.feeding_schedule_id)
        if animal:
            try:
                has_schedule = FeedingSchedule.objects.filter(animal=animal).exists()
            except Exception:
                has_schedule = False
        context.update({
            'step': self._current_step(animals.exists(), has_schedule),
            'popular_count': len(list_entries(kind='popular')),
            'animal': animal,
            'has_animals': animals.exists(),
            'has_schedule': has_schedule,
        })
        return context

    def _current_step(self, has_animals, has_schedule):
        if not has_animals:
            return 1
        if not has_schedule:
            return 2
        return 3

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        if action == 'skip' or action == 'finish':
            request.user.onboarding_completed = True
            request.user.save(update_fields=['onboarding_completed'])
            messages.success(request, 'Онбординг завершён — добро пожаловать!')
            return redirect('dashboard:dashboard')
        return redirect('accounts:onboarding')


@login_required
def maybe_redirect_onboarding(request):
    """Helper used by dashboard if needed."""
    if not request.user.onboarding_completed and not animals_for_user(request.user).exists():
        return redirect('accounts:onboarding')
    return None
