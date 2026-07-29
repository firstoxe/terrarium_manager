from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, View

from animals.services.ownership import animals_for_user
from terrarium_manager.redirects import safe_redirect
from .forms import FeedingScheduleForm
from .models import FeedingLog, FeedingSchedule
from .services.feeding import log_feeding


class FeedingScheduleListView(LoginRequiredMixin, ListView):
    model = FeedingSchedule
    template_name = 'feeding/schedule_list.html'
    context_object_name = 'schedules'

    def get_queryset(self):
        return FeedingSchedule.objects.filter(
            animal__owner=self.request.user, is_active=True,
        ).select_related('animal', 'animal__taxonomy')


class FeedingHistoryView(LoginRequiredMixin, ListView):
    model = FeedingLog
    template_name = 'feeding/history.html'
    context_object_name = 'logs'
    paginate_by = 20

    def get_queryset(self):
        return FeedingLog.objects.filter(
            animal__owner=self.request.user,
        ).select_related('animal', 'created_by')


class FeedingScheduleCreateView(LoginRequiredMixin, CreateView):
    model = FeedingSchedule
    form_class = FeedingScheduleForm
    template_name = 'feeding/schedule_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.animal = get_object_or_404(
            animals_for_user(request.user), pk=kwargs['animal_id'],
        )
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        from animals.models import CareRequirement
        req = CareRequirement.objects.filter(taxonomy=self.animal.taxonomy).first()
        if not req:
            return initial
        details = req.catalog_details or {}
        preset = (
            (details.get('feeding_policy') or {}).get('default')
            or details.get('feeding_default')
            or {}
        )
        if preset.get('interval_days'):
            initial['interval_days'] = preset['interval_days']
        if preset.get('food_type'):
            initial['food_type'] = preset['food_type']
        if preset.get('amount'):
            initial['amount'] = preset['amount']
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['animal'] = self.animal
        return context

    def form_valid(self, form):
        form.instance.animal = self.animal
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('animals:animal_detail', kwargs={'pk': self.animal.pk})


class FeedingScheduleUpdateView(LoginRequiredMixin, UpdateView):
    model = FeedingSchedule
    form_class = FeedingScheduleForm
    template_name = 'feeding/schedule_form.html'

    def get_queryset(self):
        return FeedingSchedule.objects.filter(animal__owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy('feeding:schedule_list')


class FeedTodayView(LoginRequiredMixin, View):
    def post(self, request, animal_id):
        animal = get_object_or_404(animals_for_user(request.user), pk=animal_id)
        log_feeding(animal, request.user)
        if request.htmx:
            return HttpResponse(
                f'<span class="tm-chip is-ok">Покормлен {animal.name}</span>',
            )
        messages.success(request, f'«{animal.name}» отмечен как покормленный.')
        return safe_redirect(request, fallback='feeding:schedule_list')
