from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from .services.species_library import (
    get_entry,
    import_entry,
    list_entries,
    search_entries,
)

SEX_POLICY_LABELS = {
    'single_only': 'только по одной особи',
    'female_group_only': 'группа самок допустима',
    'same_size_only': 'только одинакового размера',
    'watch_aggression': 'следить за агрессией',
}


class SpeciesLibraryListView(LoginRequiredMixin, ListView):
    template_name = 'animals/species_library.html'
    context_object_name = 'entries'

    def get_queryset(self):
        scope = self.request.GET.get('scope', 'catalog')
        kind = 'popular' if scope == 'popular' else 'catalog'
        return search_entries(
            query=self.request.GET.get('q', ''),
            tag=self.request.GET.get('tag', ''),
            kind=kind,
            care_level=self.request.GET.get('care_level', ''),
        )

    def get_context_data(self, **kwargs):
        from .models import Taxonomy

        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['tag'] = self.request.GET.get('tag', '')
        context['care_level'] = self.request.GET.get('care_level', '')
        context['scope'] = self.request.GET.get('scope', 'catalog')
        entries = list(context['entries'])
        entry_ids = [entry['id'] for entry in entries]
        taxonomy_by_library_id = {
            tax.library_id: tax.pk
            for tax in Taxonomy.objects.filter(library_id__in=entry_ids).only('pk', 'library_id')
            if tax.library_id
        }
        for entry in entries:
            entry['taxonomy_pk'] = taxonomy_by_library_id.get(entry['id'])
            entry['is_imported'] = entry['id'] in taxonomy_by_library_id
        context['entries'] = entries
        context['catalog_total'] = len(list_entries(kind='catalog'))
        context['popular_total'] = len(list_entries(kind='popular'))
        context['sex_policy_labels'] = SEX_POLICY_LABELS
        context['can_bulk_import'] = self.request.user.is_staff
        return context


class SpeciesLibraryBulkImportView(LoginRequiredMixin, View):
    def post(self, request):
        if not request.user.is_staff:
            messages.error(request, 'Массовый импорт доступен только персоналу.')
            return redirect('animals:species_library')
        from .services.species_library import import_popular
        count = import_popular()
        messages.success(request, f'Импортировано популярных видов: {count}.')
        return redirect(f"{reverse('animals:species_library')}?scope=popular")


class SpeciesLibraryImportView(LoginRequiredMixin, View):
    def post(self, request, library_id):
        try:
            taxonomy = import_entry(library_id)
        except ValueError:
            messages.error(request, 'Вид не найден в справочнике.')
            return redirect('animals:species_library')

        entry = get_entry(library_id)
        name = entry['common_name'] if entry else taxonomy.species
        messages.success(request, f'«{name}» добавлен в базу. Можно создать животное.')

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'taxonomy_id': taxonomy.id,
                'scientific_name': taxonomy.scientific_name,
                'common_name': taxonomy.common_name,
            })

        if request.POST.get('create_animal'):
            return redirect(f"{reverse('animals:animal_create')}?taxonomy={taxonomy.pk}")

        next_url = request.POST.get('next') or request.GET.get('next')
        if next_url:
            return redirect(next_url)
        return redirect('animals:species_library')
