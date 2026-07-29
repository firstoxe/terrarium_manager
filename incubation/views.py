from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from .models import IncubationRecord


class IncubationListView(LoginRequiredMixin, ListView):
    model = IncubationRecord
    template_name = 'incubation/incubation_list.html'
    context_object_name = 'incubations'

    def get_queryset(self):
        return IncubationRecord.objects.filter(
            clutch__pair__male__owner=self.request.user,
        ).select_related('clutch', 'clutch__pair', 'clutch__pair__male', 'clutch__pair__female')


class IncubationDetailView(LoginRequiredMixin, DetailView):
    model = IncubationRecord
    template_name = 'incubation/incubation_detail.html'

    def get_queryset(self):
        return IncubationRecord.objects.filter(clutch__pair__male__owner=self.request.user)
