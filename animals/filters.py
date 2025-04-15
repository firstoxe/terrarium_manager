import django_filters
from .models import Animal


class AnimalFilter(django_filters.FilterSet):
    habitat = django_filters.ChoiceFilter(choices=Animal.HABITAT_CHOICES, empty_label="Все")
    care_level = django_filters.ChoiceFilter(choices=Animal.CARE_LEVEL_CHOICES, empty_label="Все")

    class Meta:
        model = Animal
        fields = ['habitat', 'care_level']
