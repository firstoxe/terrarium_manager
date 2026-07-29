from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Animal, Action, Taxonomy, Morph, CareRequirement, AnimalPhoto
from .services.costs import action_costs_by_period
from .services.ownership import animals_for_user
from .services.timeline import build_timeline
from .filters import AnimalFilter
from .forms import AnimalForm, ActionForm, TaxonomyForm, MorphForm
from django.urls import reverse_lazy, reverse

from django_tables2 import SingleTableView
from .tables import AnimalTable, ActionTable


class AnimalListView(LoginRequiredMixin, SingleTableView):
    model = Animal
    table_class = AnimalTable
    template_name = 'animals/animal_list.html'
    paginate_by = 10

    def get_queryset(self):
        qs = animals_for_user(self.request.user)
        self.filterset = AnimalFilter(self.request.GET, queryset=qs)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

class AnimalDetailView(LoginRequiredMixin, DetailView):
    model = Animal
    template_name = 'animals/animal_detail.html'

    def get_queryset(self):
        return animals_for_user(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actions = self.object.action_set.all()
        context['action_table'] = ActionTable(actions)
        context['action_form'] = ActionForm()
        context['costs'] = action_costs_by_period(actions)
        context['care_requirement'] = CareRequirement.objects.filter(
            taxonomy=self.object.taxonomy,
        ).first()
        context['timeline'] = build_timeline(self.object)
        context['photos'] = self.object.photos.all()
        context['feeding_schedule'] = getattr(self.object, 'feeding_schedule', None)
        return context


class AnimalCreateView(LoginRequiredMixin, CreateView):
    model = Animal
    form_class = AnimalForm
    template_name = 'animals/animal_form.html'

    def get_initial(self):
        initial = super().get_initial()
        taxonomy_id = self.request.GET.get('taxonomy')
        if taxonomy_id:
            initial['taxonomy'] = taxonomy_id
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['taxonomy_form'] = TaxonomyForm()
        context['morph_form'] = MorphForm()
        return context

    def post(self, request, *args, **kwargs):
        if 'taxonomy_submit' in request.POST:
            taxonomy_form = TaxonomyForm(request.POST)
            if taxonomy_form.is_valid():
                taxonomy = taxonomy_form.save()
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'id': taxonomy.id,
                        'name': taxonomy.species,
                        'scientific_name': taxonomy.scientific_name,
                        'success': True
                    })
                return redirect('animals:animal_create')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'errors': taxonomy_form.errors}, status=400)
            return self.render_to_response(self.get_context_data(taxonomy_form=taxonomy_form))
        elif 'morph_submit' in request.POST:
            morph_form = MorphForm(request.POST)
            if morph_form.is_valid():
                morph = morph_form.save()
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'id': morph.id,
                        'name': morph.name,
                        'success': True
                    })
                return redirect('animals:animal_create')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'errors': morph_form.errors}, status=400)
            return self.render_to_response(self.get_context_data(morph_form=morph_form))
        return super().post(request, *args, **kwargs)


    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('animals:animal_detail', kwargs={'pk': self.object.pk})

class AnimalUpdateView(LoginRequiredMixin, UpdateView):
    model = Animal
    form_class = AnimalForm
    template_name = 'animals/animal_form.html'

    def get_queryset(self):
        return animals_for_user(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['taxonomy_form'] = TaxonomyForm()
        context['morph_form'] = MorphForm()
        return context

    def get_success_url(self):
        return reverse_lazy('animals:animal_detail', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        if 'taxonomy_submit' in request.POST:
            taxonomy_form = TaxonomyForm(request.POST)
            if taxonomy_form.is_valid():
                taxonomy = taxonomy_form.save()
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'id': taxonomy.id,
                        'name': taxonomy.species,
                        'scientific_name': taxonomy.scientific_name,
                        'success': True
                    })
                return redirect('animals:animal_update', pk=self.get_object().pk)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'errors': taxonomy_form.errors}, status=400)
            return self.render_to_response(self.get_context_data(taxonomy_form=taxonomy_form))
        elif 'morph_submit' in request.POST:
            morph_form = MorphForm(request.POST)
            if morph_form.is_valid():
                morph = morph_form.save()
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'id': morph.id,
                        'name': morph.name,
                        'success': True
                    })
                return redirect('animals:animal_update', pk=self.get_object().pk)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'errors': morph_form.errors}, status=400)
            return self.render_to_response(self.get_context_data(morph_form=morph_form))
        return super().post(request, *args, **kwargs)

class AnimalDeleteView(LoginRequiredMixin, DeleteView):
    model = Animal
    template_name = 'animals/animal_confirm_delete.html'
    success_url = reverse_lazy('animals:animal_list')

    def get_queryset(self):
        return animals_for_user(self.request.user)


class ActionCreateView(LoginRequiredMixin, CreateView):
    model = Action
    form_class = ActionForm
    template_name = 'animals/action_form.html'

    def form_valid(self, form):
        form.instance.animal = get_object_or_404(
            animals_for_user(self.request.user),
            pk=self.kwargs['animal_id'],
        )
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'action': {
                    'id': self.object.id,
                    'date': self.object.date.strftime('%d.%m.%Y %H:%M'),
                    'action_type': self.object.get_action_type_display(),
                    'description': self.object.description
                }
            })
        return response

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'errors': form.errors}, status=400)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('animals:animal_detail', kwargs={'pk': self.kwargs['animal_id']})


class TaxonomyCreateView(LoginRequiredMixin, CreateView):
    model = Taxonomy
    form_class = TaxonomyForm
    template_name = 'animals/taxonomy_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'id': self.object.id,
                'name': self.object.species,
                'scientific_name': self.object.scientific_name,
                'success': True
            })
        return response

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'errors': form.errors}, status=400)
        return super().form_invalid(form)


class TaxonomySelectView(LoginRequiredMixin, ListView):
    model = Taxonomy
    template_name = 'animals/_taxonomy_select.html'

    def get_queryset(self):
        return Taxonomy.objects.all().order_by('species')



class MorphCreateView(LoginRequiredMixin, CreateView):
    model = Morph
    form_class = MorphForm
    template_name = 'animals/morph_form.html'

    def form_valid(self, form):
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
