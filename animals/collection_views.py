import csv

from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView

from animals.models import Animal, Collection


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class CollectionListView(LoginRequiredMixin, ListView):
    model = Collection
    template_name = 'animals/collection_list.html'
    context_object_name = 'collections'

    def get_queryset(self):
        return Collection.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CollectionForm()
        return context


class CollectionCreateView(LoginRequiredMixin, CreateView):
    model = Collection
    form_class = CollectionForm
    success_url = reverse_lazy('animals:collection_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Коллекция создана.')
        return super().form_valid(form)


class CollectionEnableShareView(LoginRequiredMixin, View):
    def post(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk, owner=request.user)
        collection.ensure_share_token()
        collection.is_public = True
        collection.save(update_fields=['is_public', 'share_token'])
        messages.success(request, 'Публичная ссылка включена.')
        return redirect('animals:collection_list')


class CollectionDisableShareView(LoginRequiredMixin, View):
    def post(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk, owner=request.user)
        collection.is_public = False
        collection.save(update_fields=['is_public'])
        messages.success(request, 'Публичная ссылка выключена.')
        return redirect('animals:collection_list')


class PublicCollectionView(TemplateView):
    template_name = 'animals/collection_public.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collection = get_object_or_404(
            Collection, share_token=kwargs['token'], is_public=True,
        )
        context['collection'] = collection
        context['animals'] = Animal.objects.filter(
            owner=collection.owner, collection=collection,
        ).select_related('taxonomy', 'morph')
        return context


class CollectionExportView(LoginRequiredMixin, View):
    def get(self, request):
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="animals.csv"'
        writer = csv.writer(response)
        writer.writerow(['name', 'taxonomy', 'morph', 'sex', 'care_level'])
        for animal in Animal.objects.filter(owner=request.user).select_related('taxonomy', 'morph'):
            writer.writerow([
                animal.name,
                animal.taxonomy.scientific_name if animal.taxonomy else '',
                animal.morph.name if animal.morph else '',
                animal.sex,
                animal.care_level,
            ])
        return response
