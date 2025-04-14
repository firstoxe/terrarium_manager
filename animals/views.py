from datetime import timedelta

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Animal, Species, Action, Taxonomy, Morph
from .forms import AnimalForm, ActionForm, TaxonomyForm, MorphForm
from django.urls import reverse_lazy, reverse

from django_tables2 import SingleTableView
from .tables import AnimalTable, ActionTable, TaxonomyTable


class AnimalListView(LoginRequiredMixin, SingleTableView):
    model = Animal
    table_class = AnimalTable
    template_name = 'animals/animal_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Animal.objects.filter(owner=self.request.user).select_related('taxonomy', 'morph')

class AnimalDetailView(LoginRequiredMixin, DetailView):
    model = Animal
    template_name = 'animals/animal_detail.html'

    def get_queryset(self):
        return Animal.objects.filter(owner=self.request.user).select_related('taxonomy', 'morph')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actions = self.object.action_set.all()
        context['action_table'] = ActionTable(actions)
        # context['actions'] = self.object.action_set.all().order_by('-date')
        context['action_form'] = ActionForm()

        # Подсчёт затрат
        now = timezone.now()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        year_ago = now - timedelta(days=365)

        # Суммируем затраты за каждый период, исключая None
        context['costs'] = {
            'week': sum(action.cost for action in actions.filter(date__gte=week_ago) if action.cost is not None),
            'month': sum(action.cost for action in actions.filter(date__gte=month_ago) if action.cost is not None),
            'year': sum(action.cost for action in actions.filter(date__gte=year_ago) if action.cost is not None),
        }

        return context


class AnimalCreateView(LoginRequiredMixin, CreateView):
    model = Animal
    form_class = AnimalForm
    template_name = 'animals/animal_form.html'

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
        elif 'actions_submit' in request.POST:
            action_form = ActionForm(request.POST)
            if action_form.is_valid():
                action = action_form.save()
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'id': action.id,
                        'name': action.action_type,
                        'success': True
                    })
                return redirect('animals:animal_create')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'errors': action_form.errors}, status=400)
            return self.render_to_response(self.get_context_data(action_form=action_form))
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
        return Animal.objects.filter(owner=self.request.user)

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
        return Animal.objects.filter(owner=self.request.user)


class ActionCreateView(LoginRequiredMixin, CreateView):
    model = Action
    form_class = ActionForm
    template_name = 'animals/action_form.html'

    def form_valid(self, form):
        form.instance.animal = Animal.objects.get(pk=self.kwargs['animal_id'], owner=self.request.user)
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
    success_url = reverse_lazy('animals:taxonomy_list')

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


class TaxonomyListView(LoginRequiredMixin, SingleTableView):
    model = Taxonomy
    table_class = TaxonomyTable
    template_name = 'animals/taxonomy_list.html'
    paginate_by = 10


class TaxonomyUpdateView(LoginRequiredMixin, UpdateView):
    model = Taxonomy
    form_class = TaxonomyForm
    template_name = 'animals/taxonomy_form.html'
    success_url = reverse_lazy('animals:taxonomy_list')


class TaxonomyDeleteView(LoginRequiredMixin, DeleteView):
    model = Taxonomy
    template_name = 'animals/taxonomy_confirm_delete.html'
    success_url = reverse_lazy('animals:taxonomy_list')



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
