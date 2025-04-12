from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Animal, Species
from .forms import AnimalForm, SpeciesForm
from django.urls import reverse_lazy, reverse

from django_tables2 import SingleTableView
from .tables import AnimalTable

class AnimalListView(LoginRequiredMixin, SingleTableView):
    model = Animal
    table_class = AnimalTable
    template_name = 'animals/animal_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Animal.objects.filter(owner=self.request.user).select_related('species')

class AnimalDetailView(LoginRequiredMixin, DetailView):
    model = Animal
    template_name = 'animals/animal_detail.html'

    def get_queryset(self):
        return Animal.objects.filter(owner=self.request.user)


class AnimalCreateView(LoginRequiredMixin, CreateView):
    model = Animal
    form_class = AnimalForm
    template_name = 'animals/animal_form.html'

    def post(self, request, *args, **kwargs):
        # Если это отправка формы вида
        if 'species_submit' in request.POST:
            return SpeciesCreateView.as_view()(request)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('animals:detail', kwargs={'pk': self.object.pk})

class AnimalUpdateView(LoginRequiredMixin, UpdateView):
    model = Animal
    form_class = AnimalForm
    template_name = 'animals/animal_form.html'


    def get_queryset(self):
        return Animal.objects.filter(owner=self.request.user)

class AnimalDeleteView(LoginRequiredMixin, DeleteView):
    model = Animal
    template_name = 'animals/animal_confirm_delete.html'
    success_url = reverse_lazy('animals:list')

    def get_queryset(self):
        return Animal.objects.filter(owner=self.request.user)


class SpeciesCreateView(LoginRequiredMixin, CreateView):
    model = Species
    fields = ['name', 'scientific_name']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)

        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'id': self.object.id,
                'name': self.object.name,
                'success': True
            })
        return response

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'errors': form.errors}, status=400)
        return super().form_invalid(form)


class SpeciesSelectView(LoginRequiredMixin, ListView):
    model = Species
    template_name = 'animals/_species_select.html'

    def get_queryset(self):
        return Species.objects.all().order_by('name')


