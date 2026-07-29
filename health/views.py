from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView

from animals.services.ownership import animals_for_user
from .forms import WeightLogForm, HealthRecordForm, SheddingLogForm
from .models import WeightLog, HealthRecord, SheddingLog


class AnimalHealthMixin(LoginRequiredMixin):
    http_method_names = ['get', 'post']

    def dispatch(self, request, *args, **kwargs):
        self.animal = get_object_or_404(animals_for_user(request.user), pk=kwargs['animal_id'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('animals:animal_detail', kwargs={'pk': self.animal.pk}) + self.success_hash

    def form_valid(self, form):
        form.instance.animal = self.animal
        if hasattr(form.instance, 'created_by'):
            form.instance.created_by = self.request.user
        messages.success(self.request, 'Сохранено.')
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            label = form.fields[field].label if field in form.fields else field
            for error in errors:
                messages.error(self.request, f'{label}: {error}')
        if form.non_field_errors():
            for error in form.non_field_errors():
                messages.error(self.request, error)
        return redirect(self.get_success_url())


class WeightLogCreateView(AnimalHealthMixin, CreateView):
    model = WeightLog
    form_class = WeightLogForm
    success_hash = '#health'


class HealthRecordCreateView(AnimalHealthMixin, CreateView):
    model = HealthRecord
    form_class = HealthRecordForm
    success_hash = '#health'


class SheddingLogCreateView(AnimalHealthMixin, CreateView):
    model = SheddingLog
    form_class = SheddingLogForm
    success_hash = '#health'
