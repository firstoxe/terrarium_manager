from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from animals.services.ownership import animals_for_user
from animals.services.species_library import list_entries
from feeding.models import FeedingSchedule


class OnboardingView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/onboarding.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        animals = animals_for_user(self.request.user)
        animal = animals.first()
        has_schedule = False
        if animal:
            has_schedule = FeedingSchedule.objects.filter(animal=animal).exists()
        context.update({
            'step': self._current_step(animals.exists(), has_schedule),
            'popular_count': len(list_entries(kind='popular')),
            'animal': animal,
            'has_animals': animals.exists(),
            'has_schedule': has_schedule,
            'revisit': self.request.user.onboarding_completed,
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
        if action in ('skip', 'finish'):
            request.user.onboarding_completed = True
            request.user.save(update_fields=['onboarding_completed'])
            messages.success(request, 'Онбординг завершён — добро пожаловать!')
            return redirect('dashboard:dashboard')
        return redirect('accounts:onboarding')
