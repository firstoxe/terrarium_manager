import django_filters
from django import forms
from django.db.models import Q

from .models import Animal


class AnimalFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Кличка',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Поиск по кличке'}),
    )
    species = django_filters.CharFilter(
        method='filter_species',
        label='Вид',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Эублефар, Python…',
        }),
    )
    sex = django_filters.ChoiceFilter(
        choices=Animal.SEX_CHOICES,
        label='Пол',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    habitat = django_filters.ChoiceFilter(
        choices=Animal.HABITAT_CHOICES,
        label='Среда',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    care_level = django_filters.ChoiceFilter(
        choices=Animal.CARE_LEVEL_CHOICES,
        label='Сложность',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = Animal
        fields = ['name', 'species', 'sex', 'habitat', 'care_level']

    def filter_species(self, queryset, name, value):
        value = (value or '').strip()
        if not value:
            return queryset
        return queryset.filter(
            Q(taxonomy__scientific_name__icontains=value)
            | Q(taxonomy__common_name__icontains=value)
            | Q(taxonomy__species__icontains=value)
            | Q(taxonomy__genus__icontains=value)
        )
